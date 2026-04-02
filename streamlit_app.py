import json
from pathlib import Path
from typing import Any, Dict, List

import streamlit as st

from multiagent_pentest import PentestOrchestrator


def _safe_read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        return f"Unable to load file: {exc}"


def _severity_counts(findings: List[Dict[str, Any]]) -> Dict[str, int]:
    counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for item in findings:
        sev = str(item.get("severity", "")).capitalize()
        if sev in counts:
            counts[sev] += 1
    return counts


def _list_recent_runs(base_dir: Path) -> List[str]:
    if not base_dir.exists():
        return []
    runs = [p.name for p in base_dir.iterdir() if p.is_dir() and p.name != "latest"]
    runs.sort(reverse=True)
    return runs[:8]


def _load_run_outputs(base_dir: Path, run_name: str) -> Dict[str, str]:
    run_dir = base_dir / run_name
    if not run_dir.exists() or not run_dir.is_dir():
        return {}

    md_files = sorted(run_dir.glob("pentest_report_*.md"), reverse=True)
    json_files = sorted(run_dir.glob("pentest_memory_*.json"), reverse=True)

    if not md_files or not json_files:
        return {}

    return {"markdown": str(md_files[0]), "memory_json": str(json_files[0])}


def _render_findings_table(findings: List[Dict[str, Any]]) -> None:
    if not findings:
        st.info("No structured findings available for this run.")
        return

    key_cols = [
        "asset",
        "service_version",
        "risk",
        "severity",
        "cve_hint",
        "cve_verification_status",
        "confidence",
        "verification_status",
        "evidence_strength",
    ]
    rows: List[Dict[str, Any]] = []
    for item in findings:
        row = {k: item.get(k, "") for k in key_cols}
        rows.append(row)
    st.dataframe(rows, width="stretch", hide_index=True)


st.set_page_config(page_title="Multi-Agent Web Vulnerability Assessment", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap');
html, body, [class*="css"]  { font-family: 'Manrope', sans-serif; }
:root {
    --bg-soft: #f8fafc;
    --panel: #ffffff;
    --line: #d9e2ec;
    --text: #1f2937;
    --muted: #6b7280;
    --brand: #0b6e4f;
    --brand-2: #1f8a70;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 15% 15%, #f1f5f9 0%, #ffffff 45%);
}
.hero {
    padding: 1.1rem 1.2rem;
    border-radius: 16px;
    background: linear-gradient(120deg, #0b6e4f 0%, #1f8a70 100%);
    color: #f8f9fa;
    border: 1px solid #10684d;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
}
.hero p { color: #e7f5ef; }
[data-testid="stSidebar"] {
    background: #f2f6f4;
    border-right: 1px solid var(--line);
}
.footer {
    margin-top: 1.2rem;
    padding: 0.8rem 1rem;
    border-radius: 12px;
    background: #f3f7f6;
    border: 1px solid var(--line);
    color: var(--muted);
    font-size: 0.95rem;
}
div[data-testid="stMetric"] {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 0.35rem 0.5rem;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero">
  <h2 style="margin:0;">Context-Aware Multi-Agent Web Vulnerability Assessment</h2>
  <p style="margin:.4rem 0 0 0;">Scout -> Analyst -> Verifier -> Writer</p>
</div>
""",
    unsafe_allow_html=True,
)

reports_dir = Path("reports")

with st.sidebar:
    st.header("Run Settings")
    target = st.text_input("Target URL/IP", value="http://example.com")
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"], index=0)
    output_dir = st.text_input("Output Folder", value="reports")
    run_now = st.button("Run Assessment", type="primary", width="stretch")

    st.divider()
    st.subheader("Recent Runs")
    output_base_dir = Path(output_dir)
    recent_runs = _list_recent_runs(output_base_dir)
    if not recent_runs:
        st.caption("No previous runs yet.")
    else:
        for run_name in recent_runs:
            if st.button(run_name, key=f"open_run_{run_name}", width="stretch"):
                loaded = _load_run_outputs(output_base_dir, run_name)
                if loaded:
                    st.session_state.outputs = loaded
                    st.session_state.selected_run = run_name
                    st.success(f"Loaded run: {run_name}")
                else:
                    st.warning(f"Run {run_name} does not contain complete artifacts.")

if "outputs" not in st.session_state:
    st.session_state.outputs = None
if "selected_run" not in st.session_state:
    st.session_state.selected_run = ""

if run_now:
    if not target.strip():
        st.error("Target cannot be empty.")
    else:
        with st.status("Executing 4-agent pipeline...", expanded=True) as status:
            try:
                st.write("Phase 1/4 Scout: reconnaissance")
                st.write("Phase 2/4 Analyst: context-aware risk analysis")
                st.write("Phase 3/4 Verifier: evidence and CVE validation")
                st.write("Phase 4/4 Writer: professional report generation")
                orchestrator = PentestOrchestrator(target=target.strip(), model=model, output_dir=output_dir)
                outputs = orchestrator.run_safe()
                st.session_state.outputs = outputs
                st.session_state.selected_run = Path(outputs["markdown"]).parent.name
                status.update(label="Assessment completed", state="complete")
            except Exception as exc:
                status.update(label="Assessment failed", state="error")
                st.error(f"Execution error: {exc}")

outputs = st.session_state.outputs

if outputs:
    md_path = Path(outputs["markdown"])
    mem_path = Path(outputs["memory_json"])
    report_text = _safe_read_text(md_path)
    memory_data = _safe_read_json(mem_path)

    assessment = memory_data.get("phase_2_assessment", {})
    verification = memory_data.get("phase_3_verification", {})
    structured = assessment.get("structured", {}) if isinstance(assessment, dict) else {}
    findings = structured.get("findings", []) if isinstance(structured, dict) else []
    perf = memory_data.get("performance_metrics", {})

    active_run = st.session_state.selected_run or md_path.parent.name
    st.markdown(f"### Run Overview: {active_run}")

    counts = _severity_counts(findings)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Critical", counts["Critical"])
    c2.metric("High", counts["High"])
    c3.metric("Medium", counts["Medium"])
    c4.metric("Low", counts["Low"])

    st.subheader("Verification Overview")
    v1, v2, v3, v4 = st.columns(4)
    v1.metric("Verified", verification.get("verified_count", 0))
    v2.metric("Partial", verification.get("partial_count", 0))
    v3.metric("Hypothesis", verification.get("hypothesis_count", 0))
    v4.metric("Total Findings", verification.get("total_findings", len(findings)))

    st.subheader("Performance")
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Phase 1", f"{perf.get('phase_1_duration_sec', 0)}s")
    p2.metric("Phase 2", f"{perf.get('phase_2_duration_sec', 0)}s")
    p3.metric("Phase 3", f"{perf.get('phase_3_duration_sec', 0)}s")
    p4.metric("Phase 4", f"{perf.get('phase_4_duration_sec', 0)}s")

    tab_findings, tab_report, tab_artifacts = st.tabs(["Findings", "Report", "Artifacts"])

    with tab_findings:
        st.subheader("Findings Table")
        _render_findings_table(findings)

    with tab_report:
        st.subheader("Generated Markdown Report")
        st.download_button(
            label="Download Report (.md)",
            data=report_text,
            file_name=md_path.name,
            mime="text/markdown",
        )
        st.markdown(report_text)

    with tab_artifacts:
        st.markdown("#### Artifact Files")
        st.write(f"- Markdown: {outputs['markdown']}")
        st.write(f"- Memory JSON: {outputs['memory_json']}")
        execution_log = str(md_path.parent / md_path.name.replace("pentest_report_", "pentest_execution_").replace(".md", ".log"))
        st.write(f"- Execution Log (same run folder): {execution_log}")

    st.markdown(
        """
<div class="footer">
  Built for academic demo: Context-Aware Multi-Agent Web Vulnerability Assessment using LLMs.<br>
  Security notice: Only test targets you are authorized to assess.
</div>
""",
        unsafe_allow_html=True,
    )
else:
    st.info("Run an assessment from the sidebar to display findings and report.")
