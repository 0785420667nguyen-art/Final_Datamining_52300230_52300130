# 📊 DATA FOLDER

Thư mục này chứa tất cả dữ liệu và kết quả phân tích.

## 📁 Files

### 1. **youtube_raw_data.csv**
- **Mô tả:** Dữ liệu thô từ YouTube API
- **Số lượng:** 88,969 bình luận
- **Cột:**
  - `movie_name`: Tên phim
  - `release_year`: Năm phát hành
  - `review_text`: Nội dung bình luận gốc
  - `author`: Tên tác giả
  - `likes`: Số lượt thích
  - `published_at`: Thời gian đăng

### 2. **youtube_clean_data.csv**
- **Mô tả:** Dữ liệu sau khi làm sạch
- **Đã loại bỏ:**
  - URLs, mentions, hashtags
  - Ký tự đặc biệt
  - Bình luận rỗng/trùng lặp
- **Cột thêm:**
  - `cleaned_text`: Văn bản đã làm sạch
  - `original_length`: Độ dài gốc
  - `cleaned_length`: Độ dài sau làm sạch
  - `reduction_percent`: Tỷ lệ giảm

### 3. **youtube_labeled_data.csv**
- **Mô tả:** Dữ liệu đã gán nhãn cảm xúc
- **Cột thêm:**
  - `sentiment_score`: Điểm cảm xúc (-1 đến 1)
  - `subjectivity`: Độ chủ quan (0 đến 1)
  - `sentiment_label`: Nhãn (Positive/Negative/Neutral)
  - `confidence_level`: Độ tin cậy (High/Medium/Low)
  - `sentiment_description`: Mô tả chi tiết

### 4. **distribution.png**
- **Mô tả:** Biểu đồ phân bố nhãn cảm xúc
- **Bao gồm:**
  - Biểu đồ cột
  - Biểu đồ tròn

### 5. **analysis.png**
- **Mô tả:** Biểu đồ phân tích chi tiết
- **Bao gồm:**
  - Độ dài vs Cảm xúc
  - Box plot điểm cảm xúc
  - Độ dài trung bình theo nhãn
  - Likes vs Cảm xúc

## 📊 Thống kê

- **Tổng bình luận:** 88,969
- **Phân bố:**
  - 😊 Positive: 25,696 (28.9%)
  - 😐 Neutral: 51,378 (57.7%)
  - 😞 Negative: 11,895 (13.4%)

## 🔗 Nguồn

- **Video:** Avengers: Endgame Official Trailer
- **Link:** https://www.youtube.com/watch?v=TcMBFSGVi1c
- **Phương pháp:** YouTube Data API v3
