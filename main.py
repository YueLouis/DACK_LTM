import argparse
import sys

from multiagent_pentest import PentestOrchestrator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Context-Aware Multi-Agent System for Web Vulnerability Assessment using LLMs"
    )
    parser.add_argument("--target", type=str, help="Target URL/IP hợp pháp để kiểm thử")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="Tên model OpenAI")
    parser.add_argument("--output-dir", type=str, default="reports", help="Thư mục lưu báo cáo")
    return parser.parse_args()


def configure_stdio() -> None:
    """Use UTF-8 for console I/O to avoid Windows code page encoding errors."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")


if __name__ == "__main__":
    configure_stdio()
    args = parse_args()
    target = args.target or input("Nhập target URL/IP (ví dụ scanme.nmap.org): ").strip()

    if not target:
        raise ValueError("Target không được để trống.")

    system = PentestOrchestrator(target=target, model=args.model, output_dir=args.output_dir)
    system.run_safe()
    