# 💻 SOURCE FOLDER

Thư mục này chứa tất cả source code của dự án.

## 📁 Files

### 1. **sentiment_analysis.py**
- **Mô tả:** Code chính của dự án
- **Chức năng:**
  - Bước 1: Thu thập dữ liệu từ YouTube API
  - Bước 2: Chuẩn hóa dữ liệu (làm sạch)
  - Bước 3: Gán nhãn cảm xúc (TextBlob)
  - Bước 4: Trực quan hóa (biểu đồ)
  - Bước 5: Phân tích sâu
  - Bước 6: Demo ứng dụng (tương tác)

**Cách chạy:**
```bash
python sentiment_analysis.py
```
hoặc
```bash
run.bat
```

---

### 2. **app.py**
- **Mô tả:** Flask Web Application
- **Tính năng:**
  - Phân tích cảm xúc real-time
  - Lưu lịch sử phân tích
  - Thống kê tổng quan
  - Giao diện web đẹp
- **API Endpoints:**
  - `GET /` - Trang chủ
  - `POST /analyze` - Phân tích cảm xúc
  - `GET /history` - Lịch sử phân tích
  - `GET /stats` - Thống kê

**Cách chạy:**
```bash
python app.py
```
hoặc
```bash
run_app.bat
```

Sau đó truy cập: http://localhost:5000

---

### 3. **get_examples.py**
- **Mô tả:** Script lấy ví dụ từ dữ liệu
- **Chức năng:**
  - Lấy 1 ví dụ Positive
  - Lấy 1 ví dụ Negative
  - Lấy 1 ví dụ Neutral
  - Hiển thị thống kê

**Cách chạy:**
```bash
python get_examples.py
```

---

### 4. **templates/index.html**
- **Mô tả:** Giao diện web cho Flask app
- **Công nghệ:**
  - HTML5
  - CSS3 (Bootstrap 5)
  - JavaScript (Vanilla JS)
  - Font Awesome icons
- **Tính năng:**
  - Responsive design
  - Real-time analysis
  - Beautiful UI with gradient
  - Animation effects

---

### 5. **run.bat**
- **Mô tả:** Batch file chạy dự án chính
- **Chức năng:**
  - Kiểm tra Python
  - Kiểm tra thư viện
  - Chạy sentiment_analysis.py

---

### 6. **run_app.bat**
- **Mô tả:** Batch file chạy web app
- **Chức năng:**
  - Kiểm tra Python
  - Kiểm tra Flask
  - Chạy app.py

---

## 🚀 Hướng dẫn sử dụng

### Chạy dự án chính (Thu thập + Phân tích):
```bash
cd source
python sentiment_analysis.py
```

### Chạy Web App:
```bash
cd source
python app.py
```

### Lấy ví dụ từ dữ liệu:
```bash
cd source
python get_examples.py
```

---

## 📦 Thư viện cần thiết

```
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
google-api-python-client>=2.0.0
textblob>=0.15.0
flask>=2.3.0
```

Cài đặt:
```bash
pip install -r ../requirements.txt
```

---

## 🎯 Lưu ý

- **sentiment_analysis.py:** Chạy toàn bộ pipeline (30-50 phút)
- **app.py:** Web app để demo nhanh (chỉ phân tích 1 comment)
- **get_examples.py:** Xem ví dụ từ dữ liệu đã phân tích

---

**Sinh viên thực hiện:**
- Đỗ Tài Khải Nguyên (MSSV: 52300230)
- Tống Phương Nam (MSSV: 52300130)
