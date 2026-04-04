# Related Work và Ghi chú Bảo vệ

## 1) Related Work

Hệ thống multi-agent đã được ứng dụng rộng rãi trong các bài toán phức tạp, đặc biệt từ khi Large Language Models (LLMs) phát triển mạnh. Các framework như LangGraph, AutoGen và CrewAI cung cấp cơ chế điều phối nhiều agent với vai trò chuyên biệt và luồng nhiệm vụ rõ ràng.

Trong lĩnh vực an ninh web, các chuẩn như OWASP Top 10 và OWASP Web Security Testing Guide (WSTG) mô tả các nhóm lỗ hổng phổ biến và cách kiểm thử. Bên cạnh đó, Penetration Testing Execution Standard (PTES) đưa ra quy trình có cấu trúc gồm reconnaissance, analysis và reporting.

Đề tài này kết hợp các ý tưởng trên bằng một hệ thống context-aware multi-agent để mô phỏng quy trình đánh giá lỗ hổng web và tận dụng khả năng suy luận của LLM.

## 2) Tài liệu tham chiếu có thể trích dẫn

1. LangGraph: orchestration và stateful workflow cho multi-agent.
2. AutoGen: cơ chế hội thoại và cộng tác giữa các agent.
3. CrewAI: mô hình role-based agent và task delegation.
4. OWASP Top 10: nhóm rủi ro bảo mật web phổ biến.
5. OWASP WSTG: phương pháp luận kiểm thử bảo mật web.
6. PTES: quy trình penetration test có cấu trúc.
7. NIST Cybersecurity Framework: khung tư duy theo vòng đời bảo mật.

## 3) Ánh xạ đề tài với đề bài môn học

1. Phase 1 - Reconnaissance: Scout Agent.
2. Phase 2 - Vulnerability Assessment: Analyst Agent + Verifier Agent.
3. Phase 3 - Report: Writer Agent.

## 4) Mẫu mở đầu khi bảo vệ

"Nhóm em xây dựng một hệ thống multi-agent có nhận thức ngữ cảnh để đánh giá bảo mật web. Các agent phối hợp theo chuỗi Scout -> Analyst -> Verifier -> Writer, giúp thu thập dữ liệu, phân tích rủi ro, xác minh kết quả và sinh báo cáo tự động có bằng chứng minh bạch."

## 5) Câu hỏi thầy có thể hỏi và ý trả lời ngắn

1. Vì sao không dùng 1 agent duy nhất?

- Vì tách nhiệm vụ theo phase giúp dễ kiểm soát chất lượng, giảm overclaim và dễ bảo trì.

1. Context-aware thể hiện ở đâu?

- Mỗi phase đọc/ghi SharedMemory, agent sau dùng lại ngữ cảnh của phase trước để suy luận.

1. LLM được dùng ở đâu?

- Dùng trong Analyst để mở rộng lập luận rủi ro và trong Writer để tạo narrative ngắn gọn.

1. Tools nào do nhóm tự làm, tools nào AI gợi ý?

- Tự làm: kiến trúc pipeline, orchestrator, luồng SharedMemory, rule logic chính, giao diện Streamlit.
- AI hỗ trợ: tinh chỉnh prompt, wording báo cáo, một số gợi ý cải tiến UI.

1. Hạn chế lớn nhất hiện tại là gì?

- Chưa phải production scanner; CVE verification phụ thuộc NVD API/network.

1. Làm sao chứng minh kết quả minh bạch?

- Mỗi run có đầy đủ report + memory + execution log; source fallback/lỗi API được ghi rõ.

## 6) Giới hạn cần nói trung thực

1. Chưa phải production security scanner.
2. CVE verification phụ thuộc NVD API và kết nối mạng.
3. Phạm vi kiểm thử giới hạn trong lab hoặc hệ thống có quyền hợp lệ.
4. Tập trung vào assessment và reporting, không đi sâu khai thác tấn công.
