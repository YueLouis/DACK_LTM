# Hướng Dẫn Chạy Trên Windows

## 1) Chuẩn bị môi trường

1. Mở terminal tại thư mục project (nơi có file main.py).
1. Cài dependencies:

```powershell
pip install -r requirements.txt
```

1. Tạo file .env trong thư mục gốc và thêm API key:

```env
OPENAI_API_KEY=your_key_here
```

1. Kiểm tra Nmap:

```powershell
nmap --version
```

## 2) Chạy bằng CLI

Nhập tay target:

```powershell
python main.py
```

Truyền target qua tham số:

```powershell
python main.py --target scanme.nmap.org
```

## 3) Chạy bằng Web UI

```powershell
python -m streamlit run streamlit_app.py
```

Mở trình duyệt:

```text
http://localhost:8000
```

## 4) Kiểm tra output

Mỗi run thành công tạo 3 artifact:

1. pentest_report_YYYYMMDD_HHMMSS.md
2. pentest_memory_YYYYMMDD_HHMMSS.json
3. pentest_execution_YYYYMMDD_HHMMSS.log

Các file nằm trong reports/YYYYMMDD_HHMMSS, đồng thời có snapshot mới nhất tại reports/latest.

## 5) Troubleshooting nhanh

1. Lỗi OPENAI_API_KEY: kiểm tra file .env và tên biến OPENAI_API_KEY.
2. Timeout API: hệ thống có fallback local, báo cáo sẽ ghi rõ source fallback.
3. Nmap không chạy: cài Nmap và thêm vào PATH.

## 6) Lưu ý đạo đức

Hệ thống này phục vụ học tập/nghiên cứu theo hướng phòng thủ.

Chỉ quét trên môi trường lab hoặc hệ thống bạn có quyền kiểm thử hợp lệ.
