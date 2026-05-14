# Sentiment Analysis - YouTube API

## Dự án phân tích cảm xúc bình luận YouTube

**Sinh viên thực hiện:**
- Đỗ Tài Khải Nguyên (MSSV: 52300230)
- Tống Phương Nam (MSSV: 52300130)

**GitHub:** https://github.com/0785420667nguyen-art/Final_Datamining_52300230_52300130

---

## 🚀 Cách chạy

### 1. Clone repository

```bash
git clone https://github.com/0785420667nguyen-art/Final_Datamining_52300230_52300130.git
cd Final_Datamining_52300230_52300130
```

### 2. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 3. Chạy toàn bộ dự án (Thu thập + Phân tích)

```bash
cd source
python sentiment_analysis.py
```

Hoặc:

```bash
cd source
run.bat
```

**Thời gian:** 30-50 phút  
**Kết quả:** 
- 3 file CSV trong folder `data/` (dữ liệu thô, sạch, đã gán nhãn)
- 2 file PNG trong folder `data/` (biểu đồ phân bố và phân tích)

---

### 4. Chạy Web App 🌐

```bash
cd source
python app.py
```

Hoặc:

```bash
cd source
run_app.bat
```

Sau đó mở trình duyệt và truy cập: **http://localhost:5000**

**Tính năng Web App:**
- ✅ Giao diện web thân thiện
- ✅ Phân tích cảm xúc real-time
- ✅ Hiển thị kết quả chi tiết với emoji
- ✅ Lưu lịch sử phân tích
- ✅ Thống kê tổng quan
- ✅ Responsive design (mobile-friendly)

---

## 📁 Cấu trúc dự án

```
Final_Datamining_52300230_52300130/
├── data/                      # Dữ liệu và kết quả
│   ├── youtube_raw_data.csv       # Dữ liệu thô
│   ├── youtube_clean_data.csv     # Dữ liệu sạch
│   ├── youtube_labeled_data.csv   # Dữ liệu đã gán nhãn
│   ├── distribution.png           # Biểu đồ phân bố
│   └── analysis.png               # Biểu đồ phân tích
├── source/                    # Source code
│   ├── sentiment_analysis.py      # Code chính (6 bước)
│   ├── app.py                     # Web App
│   ├── get_examples.py            # Script lấy ví dụ
│   ├── templates/                 # HTML templates
│   │   └── index.html            # Giao diện web
│   ├── run.bat                    # Chạy dự án chính
│   └── run_app.bat                # Chạy Web App
├── history/                   # Lịch sử phân tích (tự động tạo)
│   └── analysis_history.csv
├── 52300230/                  # Báo cáo LaTeX
│   ├── main.tex
│   ├── tailieuthamkhao.bib
│   ├── chuongs/
│   ├── image/
│   └── Template/
├── requirements.txt           # Thư viện cần thiết
└── README.md                  # Hướng dẫn
```

---

## 📊 Kết quả

- **Nguồn dữ liệu:** YouTube API - Video Avengers: Endgame
- **Link video:** https://www.youtube.com/watch?v=TcMBFSGVi1c
- **Tổng số bình luận:** 88,969
- **Phân bố:**
  - 😊 Positive: 25,696 (28.9%)
  - 😐 Neutral: 51,378 (57.7%)
  - 😞 Negative: 11,895 (13.4%)

---

## 🔧 Yêu cầu

**Thư viện:**
- pandas
- numpy
- matplotlib
- seaborn
- textblob
- google-api-python-client
- flask

**Cài đặt:**
```bash
pip install -r requirements.txt
```

---

## 📝 Báo cáo LaTeX

Để compile báo cáo:

```bash
cd 52300230
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

---

## 📞 Liên hệ

**Sinh viên thực hiện:**
- Đỗ Tài Khải Nguyên (MSSV: 52300230)
- Tống Phương Nam (MSSV: 52300130)

**Ngày:** 12/05/2026

**GitHub:** https://github.com/0785420667nguyen-art/Final_Datamining_52300230_52300130
