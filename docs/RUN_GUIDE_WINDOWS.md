# Huong Dan Chay Tren Windows

## Buoc 1: Mo terminal trong thu muc project

Di chuyen vao thu muc chua `main.py`.

## Buoc 2: Cai dependencies

```powershell
pip install -r requirements.txt
```

## Buoc 3: Cau hinh API key

1. Copy `.env.example` thanh `.env`
2. Dien gia tri `OPENAI_API_KEY`

## Buoc 4: Chay chuong trinh

### Cach A - Nhap tay target

```powershell
python main.py
```

### Cach B - Truyen target qua tham so

```powershell
python main.py --target scanme.nmap.org
```

## Buoc 5: Kiem tra output

Sau khi chay xong, xem 2 file trong thu muc `reports/`:

- `pentest_report_YYYYMMDD_HHMMSS.md`
- `pentest_memory_YYYYMMDD_HHMMSS.json`

## Troubleshooting nhanh

- Loi `OPENAI_API_KEY`: kiem tra file `.env`.
- Loi timeout API: he thong co fallback, van tao report.
- Nmap khong chay: cai Nmap va kiem tra lenh `nmap --version`.

## Luu y dao duc

Chi quet he thong ban so huu hoac co giay phep kiem thu hop le.
