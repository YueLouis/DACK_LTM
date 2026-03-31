# Bang Phan Cong Nhiem Vu (3 Thanh Vien)

| Thanh vien | Vai tro | Nhiem vu chi tiet (Actionable) | File chiu trach nhiem |
|---|---|---|---|
| TV 1 (Lead) | System Architect | Xay dung Orchestrator, quan ly Shared Memory, xu ly loi API/timeout, dieu phoi luong chay giua 3 agent | `multiagent_pentest/orchestrator.py`, `multiagent_pentest/shared_memory.py`, `main.py` |
| TV 2 | Security Tooling | Ket noi Nmap, toi uu tham so scan (`-F -sV`, co the mo rong `-sC`, `-A` cho lab hop phap), data cleaning truoc khi dua cho AI | `multiagent_pentest/agents/scout_agent.py` |
| TV 3 | Prompt Engineer | Thiet ke va tinh chinh prompt cho Analyst/Writer, danh gia chat luong output giua cac prompt version, tong hop bang Prompt Evaluation | `multiagent_pentest/agents/analyst_agent.py`, `multiagent_pentest/agents/writer_agent.py` |

## Definition of Done tung thanh vien

1. TV 1
- Chay `python main.py --target <target>` thanh cong.
- Luu duoc file report `.md` va memory `.json`.
- Co fallback khi loi OpenAI/network.

1. TV 2
- Xuat duoc `raw_scan_data` hop le (host, port, service, version).
- Loai bo gia tri rong/khong hop le trong tien xu ly.
- Co so sanh ket qua scan profile co ban va scan profile mo rong (trong moi truong lab).

1. TV 3
- Co it nhat 2 phien ban prompt (`v1_markdown`, `v2_json_schema`).
- Co bang danh gia prompt (do dai, do ro rang, kha nang parse).
- Co ket luan prompt nao su dung de nop bai.
