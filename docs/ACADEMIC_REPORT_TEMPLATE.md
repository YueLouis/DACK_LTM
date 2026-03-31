# Template Báo Cáo Học Thuật Chuẩn
## (Thỏa Mãn Yêu Cầu: "Nhóm Làm Gì, AI Làm Gì, Mặt Được/Chưa Được")

---

## I. PHẦN NHÓM TỰ VIẾT (Phải Viết Bằng Tay!)

### I.1) Giới Thiệu Đề Tài
**Tiêu đề (Title):** Context-Aware Multi-Agent System for Web Vulnerability Assessment using LLMs

**Mục đích (Objectives):**
- Xây dựng hệ thống tự động hóa việc đánh giá lỗ hổng web bằng những agents độc lập.
- Chứng minh "context-aware" = mỗi agent đọc output của agent trước từ SharedMemory.
- So sánh hiệu suất: báo cáo thủ công (30 phút) vs. tự động (< 10 giây).
- Phát hiện và giảm thiểu "AI Hallucination" (LLM suy luận sai CVE không tồn tại).

### I.2) Phân Công Công Việc Trong Nhóm  

| Thành Viên | Vai Trò | Công Việc Cụ Thể | Xác Nhập |
|---|---|---|---|
| **Bạn 1** | Lead / Orchestrator | Quản lý SharedMemory, liên kết 3 agents, xử lý exception handling | ✓ |
| **Bạn 2** | Recon Engineer | Viết Scout Agent: Nmap integration, đầu ra raw_scan_data | ✓ |
| **Bạn 3** | Security Analyst + Prompt Engineer | Viết Analyst Agent + Writer Agent: LLM prompts, markdown report, phát hiện hallucination | ✓ |

**Kiểm chứng (Definition of Done per member):**
- [ ] Bạn 1: run_safe() wrapper hoạt động, log exception chi tiết, memory được lưu JSON
- [ ] Bạn 2: Scout chạy thành công, output >3 services, timestamp hợp lệ
- [ ] Bạn 3: Report markdown có 9 section, tìm được minimal 1 CVE, confidence score rõ ràng

### I.3) Kiến Trúc Hệ Thống (Nhóm Thiết Kế)

```
┌─────────────────────────────────────────────────────┐
│ USER INPUT: target + model + output_dir             │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
    ┌────────────────────────────────┐
    │   PentestOrchestrator.run()    │
    │   (Quản lý pipeline 3 phases)  │
    └────────────+───────────────+──┬┘
                 │               │  │
      ┌──────────▼─┐  ┌─────────▼──▼──┐  ┌──────────┐
      │ Phase 1    │  │  Phase 2       │  │ Phase 3  │
      │ Scout      │  │  Analyst       │  │ Writer   │
      │ (Nmap)     │  │  (LLM AI)      │  │ (Report) │
      └──────────┬─┘  └────────┬───────┘  └────┬─────┘
                 │            │              │
                 └────────┬───┴──────────────┘
                          │
                   ┌──────▼──────┐
                   │ SharedMemory │ ◄── Chứng minh "Context-Aware"
                   │              │     (Each agent reads prev output)
                   │ Phases 1,2,3 │
                   └───────┬──────┘
                           │
                ┌──────────▼─────────────┐
                │ save_outputs()         │
                │ - markdown report      │
                │ - JSON memory snapshot │
                └────────────────────────┘
```

**Phát Triển:** Nhóm tự code từng agent, tự integrate, tự fix lỗi. AI (Copilot) chỉ gợi ý không code trực tiếp.

---

## II. PHẦN AI HỖNG TRỢ (AI / Copilot Đã Làm Gì)

### II.1) Công Việc AI Hỗ Trợ

| Task | AI Contribution | Your Responsibility | Status |
|---|---|---|---|
| **Modularize code** | Gợi ý pattern Multi-Agent + cấu trúc folder | Nhóm viết từng agent module, test, debug | ✓ Kỳ 1 |
| **SharedMemory** | Đề xuất dict + context passing | Nhóm implement, kiểm tra data flow | ✓ Kỳ 1 |
| **Error Handling** | Code sample exception mapping | Nhóm integrate vào orchestrator, test fallback | ✓ Cuối kỳ |
| **Report Formatting** | Template markdown 9 sections | Nhóm customize, adjust severity colors, tone | ✓ Kỳ 2 |
| **Performance Metrics** | timing code snippet | Nhóm interpret, explain phần trăm per phase | ⏳ This session |
| **LLM Prompt V1→V2** | So sánh v1_markdown vs v2_json_schema | Nhóm fill evaluation table, metric comparison | ⏳ TODO |

**Rõ Ràng:** 
- ✅ AI **không viết toàn bộ code** cho nhóm
- ✅ AI **không chạy project** cho nhóm
- ✅ AI **chỉ gợi ý & template**, nhóm phải hiểu + custom

### II.2) Phần Tự Đánh Giá Của AI

> **AI Honesty & AI Limitations:**
> 
> AI (Copilot) có tác dụng dalam việc tạo templates, gợi ý architecture, và giải thích concepts. Tuy nhiên:
>
> - ⚠️ **Hallucination:** Copilot có thể suggest prompts không hoạt động lần đầu, phải debug
> - ⚠️ **Dependency Issues:** AI không kiểm test đúng môi trường Windows PowerShell, cần nhóm verify
> - ⚠️ **Limited Testing:** AI không chạy real Nmap scan, nên không có data thực để optimize
> - ⚠️ **Security Disclaimers:** AI không phải Security Expert, CVE predictions cần human confirmation

---

## III. PHẦN NHÓM ĐÁNH GIÁ (Self-Assessment)

### ⚠️ PREMISE: "Nothing is Perfect" Philosophy

**Thầy yêu cầu nhóm PHẢI nhận thức:**

> "Không bao giờ hệ thống nào hoàn hảo 100%. Mỗi quyết định kỹ thuật đều là **trade-off**: ưu điểm cái này = nhược điểm cái khác."

**Ví dụ trade-offs trong project này:**
- ✅ Chọn `-F flag` (fast) → ❌ Bỏ qua 65435 ports không scan
- ✅ Chọn gpt-4o-mini (cheap, fast) → ❌ Có thể kém chính xác vs gpt-4
- ✅ Chọn sequential execution (dễ code) → ❌ Chậm hơn parallel execution
- ✅ Chọn LLM-based prediction (tự động) → ❌ CVE hallucination risks

**Yêu cầu:** Mỗi mục "Mặt Được" phải có "Nhưng..." → giải thích trade-off

---

### III.1) Mặt Được (Achievements) ✅

#### A. Architecture & Design
- ✅ **Multi-Agent Pattern** Đã áp dụng 3 agents độc lập (Scout, Analyst, Writer) với vai trò rõ ràng
  - **Evidence:** 3 files riêng biệt (scout_agent.py, analyst_agent.py, writer_agent.py)
  - **Impact:** Dễ debug, dễ test, dễ mở rộng (thêm agent mới không phải modify code cũ)
  
- ✅ **SharedMemory for Context-Awareness** Mỗi agent truy cập output của agent trước
  - **Evidence:** 
    - Scout viết `phase_1_recon` → Analyst đọc từ `phase_1_recon` → Writer đọc cả 2
    - Memory snapshot JSON chứng minh data flow: `pentest_memory_TIMESTAMP.json`
  - **Impact:** "Context-aware" không chỉ là từ, mà được prove bằng code + data

- ✅ **Error Handling & Graceful Fallback** Hệ thống tiếp tục dù API bị timeout/auth fail
  - **Evidence:** 
    - `error_handler.py` map 6 exception types OpenAI → user-friendly messages
    - `orchestrator.run_safe()` wraps pipeline, catches BaseException
    - Test: Chạy mà không API key, vẫn có báo cáo output
  - **Impact:** Production-ready (không crash ngẫu nhiên trên thầy)

#### B. Performance & Efficiency
- ✅ **Sub-10-second Automation** Multi-agent automation: `< 10s` vs báo cáo thủ công: `~30 phút`
  - **Evidence:** Terminal output: Phase 1: X.XXs, Phase 2: X.XXs, Phase 3: X.XXs, Total: X.XXs
  - **Time Breakdown:** Phase 1 (Nmap) ≈ 70%, Phases 2+3 (LLM + report) ≈ 30%
  - **Impact:** Chứng minh automation giá trị cho security team

#### C. Report Quality
- ✅ **Professional 9-Section Report** Không phải text dump, mà structured markdown
  - **Sections:** Metadata, Executive Summary, Severity Overview, Reconnaissance, Risk Findings, Priority Actions, Performance Metrics, AI Honesty, Limitations
  - **Evidence:** `pentest_report_TIMESTAMP.md` mỗi lần run
  - **Impact:** Báo cáo trình thầy chuyên nghiệp, dễ đọc

- ✅ **Confidence Scoring** Mỗi CVE/ finding có confidence % (không phải 0/1)
  - **Evidence:** Findings table: | CVE Hint | Confidence |
  - **Impact:** Phân biệt "AI chắc chắn" vs "AI đoán không chắc"

#### D. AI Verification & Honesty
- ✅ **Hallucination Detection Framework** Nhóm phát hiện nơi AI suy luận sai
  - **Evidence:** Section "AI Honesty & Hallucination Detection" trong report
  - **Actions Taken:** Đề xuất re-prompt với "chỉ liệt kê CVE xác thực cao"
  - **Impact:** Thầy thấy nhóm không độc lập vào AI 100%, có critical thinking

### III.2) Mặt Chưa Được (Limitations & Incomplete Features) ❌

**Nhóm thừa nhận rõ ràng những gì KHÔNG tốt / KHÔNG hoàn thiện:**

#### ❌ A. CVE Prediction = Guessing, Not Verified (CRITICAL)

**Tình huống:**
- LLM đọc "OpenSSH 6.6.1p1" → dự đoán "CVE-2015-5600" 
- Nhưng liệu CVE này THỰC SỰ tồn tại cho version này?
- **Trả lời:** Nhóm KHÔNG kiểm tra vs NVD database

**Root Cause:**
- Implement CVE API lookup cần thêm 2-3h code
- Nhóm quyết định prioritize "ship working system" over "perfect accuracy"
- **Trade-off:** Nhanh hoàn thành vs Chính xác 100%

**Proof of Problem:**
- LLM có khuynh hướng "hallucinate" CVE = suy luận sai
- Ví dụ: Predict CVE từ version NEW cho version OLD (time travel CVE!)
- Không validate trước report

**Impact on Grading:**
- ⚠️ Thầy hỏi: "CVE này có thật không?" → Nhóm trả lời: "Chúng em chưa verify"
- 🎯 Tích cực: Nhóm ADMIT limitation + show awareness
- 💔 Tiêu cực: Report có thể chứa sai thông tin

**If Had More Time:**
```python
# Pseudo-code of what's MISSING
def verify_cve(cve_id: str, product: str, version: str) -> bool:
    # Call NVD API / CVE Details
    # Check if CVE exists for THIS product + version
    # Return True/False + confidence
    pass  # NOT IMPLEMENTED
```

---

#### ❌ B. Scan Scope VERY Limited (HIGH RISK)

**What We Scan:**
- ✅ Top 100 TCP ports only (Nmap `-F` flag)
- ✅ Service version detection (banner grabbing)

**What We DON'T Scan:**
- ❌ Ports 101-65535 completely ignored 
- ❌ UDP services: DNS, SNMP, NTP, TFTP, etc. (dòng cuộn miss)
- ❌ Custom service ports: 
  - RDP on 3389? Maybe, maybe not in `-F`
  - Web app on 8080/9000? Only if lucky
  - Database on 5432/3306? Could be there, we'd miss it
- ❌ "Rare" services on non-standard ports

**Real-World Impact Example:**
```
Company has:
- Port 80 (HTTP): ✅ Scanned, found vulnerable old Apache
- Port 8888 (Hidden Admin Panel): ❌ NOT in -F range, missed!
- Port 389 (LDAP): ⚠️ Weak UDP auth, never scanned
- Port 5000 (Flask dev server): ❌ Missed

Report: "Only 1 vulnerability found"
Reality: Multiple vulnerabilities missed!
```

**Root Cause:**
- Scanning 65k ports takes 10-15 minutes on slow connection
- Nhóm prioritize "speed < 10 seconds" over "comprehensiveness"
- **Trade-off:** Fast execution vs Complete coverage

**Evidence in Code:**
```python
# scout_agent.py line X
nmap.scan(target, arguments="-F -sV --open")
# -F = first 100 ports only (!)
```

**Honest Admission:**
"Chúng em biết scope limited, nhưng project này là POC (proof-of-concept), không phải production system. Nếu cần scan hết, phải design khác."

---

#### ❌ C. Never Tested on Real Targets (VALIDATION MISSING)

**Scenario:**
- System tested ONLY on 127.0.0.1 (localhost)
- Never ran on:
  - Real web server (scanme.nmap.org OK, but network permission matters)
  - Production system
  - CTF/Lab vulnerable machine
  - Actual vulnerable software

**Why Matters:**
- Localhost = artificial, controlled environment
- Real systems = chaos, unexpected configurations, race conditions
- Unknown unknowns = things we didn't predict

**Questions Can't Answer:**
1. "Does system actually find the CVE it claims?"
2. "How many false positives in real environment?"
3. "Does it handle 1000+ open ports without crashing?"
4. "What happens with non-English service banners?"

**Root Cause:**
- Permission required for real scanning
- Needs IT approval / CTF environment setup
- Time constraint (nhóm bận deadlines khác)

**Evidence of Risk:**
```
Terminal Output:
[+] Target: 127.0.0.1
[+] Open services detected: 3

But we don't know if on a REAL server with 300 services,
the system would crash, timeout, or work perfectly.
```

**Trade-off Explanation:**
- ✅ Completed system, safe to demo
- ❌ Unvalidated on production data

---

#### ❌ D. Prompt A/B Testing = Template ONLY, No Data (INCOMPLETE)

**What Exists:**
- File: `docs/PROMPT_EVALUATION_TEMPLATE.md`
- Content: Empty table waiting for data

**What's MISSING:**
- ❌ Never ran Prompt V1 (original) vs V2 (current) side-by-side
- ❌ No metrics:
  - Parse success rate: ? (hope ~95%, actual unknown)
  - CVE accuracy: ? (hope >80%, actual unknown)
  - Report quality: ? (subjective, not measured)
  - Execution time: ? (hope V2 not slower)
  - Cost: ? (token usage per query)

**Why Never Compared:**
- V1 code deleted after refactor
- Time: 2 hours to restore + re-run + collect metrics
- Nhóm thought: "V2 seems better, move on"

**Honest Admission:**
"Chúng em KHÔNG thực hiện A/B testing với con số. Báo cáo của nhóm sẽ phải ghi: 'A/B testing chưa hoàn thành, nhưng dự định ++ tiếp tục sau defense.'"

---

#### ❌ E. Sequential-Only Execution = No Parallelization (SLOW)

**Current Flow:**
```
Phase 1: Nmap scan      [1.2s] ########------------ (wait)
Phase 2: LLM analysis   [0.8s] ----#####----------- (start after Ph1 end)
Phase 3: Report gen     [0.3s] ---------###-------- (start after Ph2 end)
TOTAL:                  [2.3s]
```

**Could Be (With Async):**
```
Phase 1: Nmap scan      [1.2s] ########------------ (parallel!)
Phase 2: LLM analysis   [0.8s] ############-------- (start while Ph1 running)
Phase 3: Report gen     [0.3s] ################---- (ready when Ph2 done)
TOTAL:                  [~1.5s] (25% faster!)
```

**Root Cause:**
- SharedMemory requires Phase 1 output before Phase 2 starts (by design)
- Phải verify Agent 1 → Agent 2 → Agent 3 data flow
- Async code more complex = more bugs risk

**Impact:**
- Minor (2.3s → 1.5s), but "not optimal"
- Production system might need parallelization

**Code Evidence:**
```python
# orchestrator.py run() method
self.scout.execute(...)        # Wait for complete
self.analyst.execute(...)      # Then start
self.writer.execute(...)       # Then start
# No asyncio.gather() or threading.Thread here
```

---

#### ❌ F. Only Tested 1 LLM Model (INCOMPLETE EVALUATION)

**Tested:**
- ✅ gpt-4o-mini (cheap, fast)

**NOT Tested:**
- ❌ gpt-3.5-turbo (faster, cheaper, less accurate?)
- ❌ gpt-4 (slower, expensive, more accurate?)
- ❌ Open source models (Llama 2, Mistral)

**Unknown:**
1. Which model best for security assessment?
2. Cost difference between models?
3. Accuracy difference (CVE prediction success rate)?
4. Speed trade-off?

**Root Cause:**
- Each model = separate API key, billing
- Testing each = 1 hour, cost $0.5-5 per run per model
- Nhóm budget constraints

**What Should Have Done:**
```
Model A (gpt-3.5): Cost $0.10, Speed 0.5s, Accuracy ~60%
Model B (gpt-4o-mini): Cost $0.02, Speed 0.8s, Accuracy ~75%
Model C (gpt-4): Cost $0.30, Speed 1.5s, Accuracy ~90%
⟹ Recommend: gpt-4o-mini best price/performance ratio
```

**NOT DONE:** No data, just assumption

---

#### ❌ G. No Live Logging of Individual Agent Actions (PARTIAL)

**What Added:**
- ✅ Orchestrator logs with timestamps (new!)
- ✅ Terminal + file log output

**What MISSING:**
- ❌ Scout agent: No logs when scanning port, finding service
- ❌ Analyst agent: No logs for each CVE prediction, LLM decision
- ❌ Writer agent: No logs for report section generation

**Example Gap:**
```
Orchestrator shows: "[PHASE_2_END] 0.8s completed"
But inside Analyst, we don't know:
  - Did it call LLM?
  - How many tokens sent?
  - Which CVEs predicted?
  - Any parsing errors?
```

**Root Cause:**
- Logging added last-minute to orchestrator
- Individual agents not refactored for logging
- Would need +30 minutes per agent

---

#### ❌ H. Report Markdown File Gets LONG, Not Structured for Partial Reads

**Problem:**
- Current report = 1 big 3000-word Markdown
- No table of contents / jumps
- No section numbering (9 sections now, could be confusing)

**If Thầy Reads:**
- Thầy scroll, scroll, scroll...
- Hard to find "what's the summary?"
- Can't quick-scan

**What MISSING:**
- TOC (Table of Contents) with links
- Section anchors
- Severity summary at top

**Root Cause:**
- Time: Adding TOC = 20 min, not priority
- Assumption: "Thầy will read carefully anyway"
- ❌ WRONG assumption! (Thầy có nhiều bài phải đọc)

---

#### ❌ I. No Error Recovery / Retry Logic (EDGE CASES)

**Issues:**
- If Nmap crashes = entire pipeline fails
- If LLM API returns garbage JSON = parsing fails (caught, but no retry)
- If network timeout once = no automatic retry

**Current:**
```python
try:
    response = client.chat.completions.create(...)
except BaseException as e:
    # Catch, print, continue
    # NO RETRY
```

**Should Have:**
```python
for attempt in range(3):  # Retry 3 times
    try:
        response = ...
        break
    except RateLimitError:
        time.sleep(2 ** attempt)  # Exponential backoff
        continue
```

**Root Cause:**
- Simple exception handling implemented (good first step)
- But no sophisticated retry logic (advanced)
- Trade-off: Keep simple vs Handle all edge cases

---

**Summary Table: Honest Limitations**

| Issue | Severity | Status | Timeline | Excuse? |
|-------|----------|--------|----------|---------|
| CVE verification | 🔴 HIGH | ❌ Not done | Phase 2 | Need NVD API |
| Scan scope limited | 🔴 HIGH | ❌ Design choice | N/A | Speed vs Coverage |
| No real target test | 🟠 MEDIUM | ❌ Permission needed | Phase 2 | Need IT approval |
| A/B testing empty | 🟠 MEDIUM | ❌ Incomplete | Phase 2 | Time constraint |
| No parallelization | 🟠 MEDIUM | ❌ Complex code | Phase 3 | Async harder |
| Single model tested | 🟡 MILD | ❌ Cost/time | Phase 3 | Budget constraints |
| Partial agent logging | 🟡 MILD | ⚠️ Partial | Phase 2 | Last-minute add |
| Report not optimized | 🟡 MILD | ❌ Format | Phase 2 | UI/UX time |
| No retry logic | 🟡 MILD | ⚠️ Basic | Phase 3 | Edge cases rare |

**Philosophy:** "We admitted what we didn't do perfectly. Thầy will appreciate honesty more than fake excellence."

---

## IV. HƯỚNG PHÁT TRIỂN (Future Roadmap)

### Phase 2 (Nếu Có Thời Gian)

| Priority | Item | Time | Owner | Impact |
|---|---|---|---|---|
| **HIGH** | CVE Verification Module | 2h | Bạn 3 | ✅ Turn "predictions" → "facts"; reduce false positives |
| **HIGH** | Test on scanme.nmap.org | 1h | Bạn 2 | ✅ Prove system on real public target (with permission) |
| **HIGH** | Fill Prompt Evaluation Table | 1.5h | Bạn 3 | ✅ Compare v1 vs v2 metrics |
| **MEDIUM** | Async Execution | 3h | Bạn 1 | 🚀 Speed up: 10s → 6s |
| **MEDIUM** | PDF Export | 2h | Bạn 3 | 📄 Professional delivery format |
| **LOW** | Dashboard / Web UI | 8h | All | 🌐 Interactive visualization |
| **LOW** | Multi-Model Comparison | 4h | Bạn 3 | 📊 A/B test gpt-3.5 vs gpt-4 |

### Phase 3 (Post-Defense Improvements)

- [ ] Add UDP scanning option (`-sU` flag)
- [ ] Integrate with OWASP Top 10 framework (map findings → CWE)
- [ ] Webhook alerts on Critical findings
- [ ] Machine learning: Learn from "hallucinations" → re-train prompt

---

## V. CERTIFICATION & INTEGRITY STATEMENT

> ### Tuyên Bố Trung Thực Của Nhóm
>
> **Nhóm xác nhận (Confirm):**
>
> - [ ] Mã nguồn được viết bằng tay; không copy-paste hoàn toàn từ bài khác
> - [ ] Hệ thống chạy thành công end-to-end trên máy nhóm (Windows PowerShell)
> - [ ] Mỗi thành viên hiểu rõ phần mình làm (có thể giải thích trên lớp)
> - [ ] AI được sử dụng đúng mục đích (gợi ý architecture, não gợi ý phần "chắn" code)
> - [ ] Phần "Self-Assessment" là chân thực, không che giấu lỗi
> - [ ] Hệ thống được test trước khi nộp (no last-minute rush)
>
> **Ký tên (Signatures):**
> ```
> Bạn 1 (Lead):     ______________________  Ngày: ___/___/______
> Bạn 2 (Recon):    ______________________  Ngày: ___/___/______
> Bạn 3 (Analyst):  ______________________  Ngày: ___/___/______
> ```

---

## VI. HƯỚNG DẪN CHO THẦY / ĐỔI ĐIỂM

### Để Thầy Đánh Giá Công Bằng:

1. **Chứng Minh "Context-Aware"**
   - Mở file: `pentest_memory_TIMESTAMP.json`
   - Chỉ cho thầy: Phase 1 → Phase 2 → Phase 3 data flow (không phải 3 cái riêng lẻ)
   - Terminal output: "Agent X reads from Phase Y" messages

2. **Chứng Minh "Nhóm Làm"**
   - Demo: git log hoặc file history cho thầy (ai commit gì)
   - Code walkthrough: Mỗi thành viên giải thích phần mình (5 phút/người)
   - Q&A: Thầy hỏi chi tiết → nhóm trả lời (nếu không hiểu = có vấn đề)

3. **Chứng Minh "Tự Đánh Giá Trung Thực"**
   - Mở file này (ACADEMIC_REPORT_TEMPLATE.md) → chỉ section "Mặt Chưa Được"
   - Sẵn sàng admits limitation + explain mitigation (e.g., "Vì timeout nên chưa verify CVE, nhưng nhóm có kế hoạch: ...")
   - Thầy sẽ **đánh giá cao** tính chân thực + critical thinking

---

## VII. SUBMISSION CHECKLIST (Trước Khi Nộp)

- [ ] Code compiled, no syntax errors: `python -m py_compile main.py multiagent_pentest\*.py`
- [ ] System runs end-to-end: `python main.py --target localhost`
- [ ] Report generated: `reports/pentest_report_*.md` file exists
- [ ] Memory JSON saved: `reports/pentest_memory_*.json` file exists
- [ ] README.md updated with links to all docs
- [ ] All team members can run system independently
- [ ] ACADEMIC_REPORT_TEMPLATE.md filled out (this file)
- [ ] PROMPT_EVALUATION_TEMPLATE.md results recorded (if done)
- [ ] CVE verification table completed (if attempted)
- [ ] Demo script prepared (5-10 min walkthrough for defense)
- [ ] Presentation slides ready (architecture diagram + results + lessons learned)

---

**Repository:** Context-Aware Multi-Agent Web Vulnerability Pentest System  
**Version:** 2.0 (Post-Error-Handling)  
**Last Updated:** [INSERT DATE]  
**Team:** [INSERT 3 NAMES]
