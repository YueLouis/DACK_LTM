# Bao Cao Nop Thay - Checklist Chi Tiet

## 1) Kien truc Multi-Agent

- Ly do chia 3 Agent: Thu thap -> Phan tich -> Trinh bay.
- So do workflow co Shared Memory o giua.
- Vai tro tung agent va du lieu dau vao/dau ra.

## 2) Co che Context-Aware

- Minh chung Agent 2 doc du lieu tu `phase_1_recon`.
- Minh chung Agent 3 doc du lieu tu `phase_1_recon` + `phase_2_assessment`.
- Dinh kem file memory JSON khi chay that (`reports/pentest_memory_*.json`).

## 3) Prompt va Evaluation

- Liet ke it nhat 2 prompt version.
- So sanh ket qua theo tieu chi:
  - Do dung cau truc
  - Do ngan gon
  - Do de parse (JSON/Markdown)
  - Do huu dung cho bao cao
- Neu output qua dai/lan man: them rang buoc schema JSON.

## 4) Tools Origin (AI-gen vs Nhom viet)

- AI-gen: phan duoc AI de xuat/ho tro tao khung prompt hoac parse.
- Nhom viet: Orchestrator, Shared Memory, flow dieu phoi, xu ly fallback, tich hop Nmap.
- Ghi ro phan nao nhom sua lai sau khi AI de xuat.

## 5) Danh gia ky thuat

- Doi chieu du doan AI voi banner/version thuc te tu Nmap.
- Neu co CVE hint: doi chieu nguon tham khao cong khai (NVD/CVE Details).
- Neu khong khop: ghi nguyen nhan va cach giam false positive.

## 6) Gioi han va huong mo rong

- Gioi han: phu thuoc banner grabbing, co the bi sai CVE mapping.
- Huong mo rong:
  - Bo sung service fingerprinting sau hon trong lab hop phap.
  - Chuan hoa output JSON cho dashboard.
  - Xuat PDF tu Markdown.

## 7) Phu luc can nop

- Screenshot log chay terminal.
- File report `.md`.
- File shared memory `.json`.
- Bang prompt evaluation.
