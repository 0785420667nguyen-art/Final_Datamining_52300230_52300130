"""
ĐỒ ÁN: PHÂN LỚP SENTIMENT ANALYSIS VỚI YOUTUBE API

Sinh viên thực hiện:
1. Đỗ Tài Khải Nguyên (MSSV: 52300230)
2. Tống Phương Nam
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from googleapiclient.discovery import build
from textblob import TextBlob
import warnings
warnings.filterwarnings('ignore')

# Cấu hình
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Danh sách API Keys dự phòng
API_KEYS = [
    "AIzaSyAwl8P6AGV2IaN8iiuE1hYTLjbscsPEV40",
    "AIzaSyAXmuDIotZZvlMnFzeTNbxkw94BEoyWLxc",
    "AIzaSyC0cAOa2f9mB-2gMWJQuQ3fr36JHutqF-k",
    "AIzaSyAJKK2Kjl3I0ESP5O4IZ1B7wSYeMqgfspQ"
]

# Thông tin video
VIDEO_INFO = {
    "video_id": "TcMBFSGVi1c",
    "movie_name": "Avengers: Endgame",
    "release_year": 2019
}

# Màu sắc cho biểu đồ
COLORS = {'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': '#95a5a6'}


# ============================================================================
# BƯỚC 1: THU THẬP DỮ LIỆU
# ============================================================================

def get_youtube_comments(video_info, api_keys, target_count=100000):
    """
    Thu thập bình luận từ YouTube API với hệ thống dự phòng
    
    Args:
        video_info: Dictionary chứa thông tin video (video_id, movie_name, release_year)
        api_keys: Danh sách API keys dự phòng
        target_count: Số lượng bình luận mục tiêu
    
    Returns:
        DataFrame chứa dữ liệu bình luận
    """
    all_comments = []
    next_page_token = None
    current_api_index = 0
    
    print(f"\n{'='*70}")
    print(f"🔄 BƯỚC 1: THU THẬP DỮ LIỆU")
    print(f"{'='*70}")
    print(f"🎬 Phim: {video_info['movie_name']} ({video_info['release_year']})")
    print(f"🎯 Mục tiêu: {target_count:,} bình luận")
    print(f"📌 Có {len(api_keys)} API keys dự phòng\n")
    
    youtube = build('youtube', 'v3', developerKey=api_keys[current_api_index])
    print(f"🔑 Đang sử dụng API key #{current_api_index + 1}")
    
    while len(all_comments) < target_count:
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_info['video_id'],
                maxResults=100,
                pageToken=next_page_token,
                textFormat="plainText"
            )
            response = request.execute()
            
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                all_comments.append({
                    'movie_name': video_info['movie_name'],
                    'release_year': video_info['release_year'],
                    'review_text': comment['textDisplay'],
                    'author': comment['authorDisplayName'],
                    'likes': comment['likeCount'],
                    'published_at': comment['publishedAt']
                })
            
            if len(all_comments) % 5000 == 0:
                print(f"  ✓ Đã thu thập: {len(all_comments):,}")
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
                
        except Exception as e:
            error_msg = str(e)
            
            # Kiểm tra nếu là lỗi quota
            if 'quota' in error_msg.lower() or 'limit' in error_msg.lower():
                current_api_index += 1
                
                if current_api_index < len(api_keys):
                    print(f"\n⚠️  API key #{current_api_index} hết quota")
                    print(f"🔄 Chuyển sang API key #{current_api_index + 1}...\n")
                    youtube = build('youtube', 'v3', developerKey=api_keys[current_api_index])
                    continue
                else:
                    print(f"\n❌ Tất cả API keys đã hết quota!")
                    print(f"📊 Đã thu thập được: {len(all_comments):,} bình luận")
                    break
            else:
                print(f"❌ Lỗi: {e}")
                break
    
    df = pd.DataFrame(all_comments)
    print(f"\n✅ Hoàn tất! Tổng: {len(df):,} bình luận")
    print(f"🔑 Đã sử dụng {current_api_index + 1}/{len(api_keys)} API keys")
    
    return df


# ============================================================================
# BƯỚC 2: CHUẨN HÓA DỮ LIỆU (CHI TIẾT)
# ============================================================================

def clean_text_detailed(text):
    """
    Làm sạch văn bản với các bước chi tiết
    
    Returns:
        tuple: (cleaned_text, cleaning_stats)
    """
    if not isinstance(text, str):
        return "", {}
    
    original_text = text
    stats = {
        'original_length': len(text),
        'urls_removed': 0,
        'mentions_removed': 0,
        'special_chars_removed': 0,
        'extra_spaces_removed': 0
    }
    
    # Bước 1: Loại bỏ URL
    urls = re.findall(r'http\S+|www\S+|https\S+', text)
    stats['urls_removed'] = len(urls)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Bước 2: Loại bỏ mention (@username)
    mentions = re.findall(r'@\w+', text)
    stats['mentions_removed'] = len(mentions)
    text = re.sub(r'@\w+', '', text)
    
    # Bước 3: Loại bỏ hashtags
    text = re.sub(r'#\w+', '', text)
    
    # Bước 4: Loại bỏ số điện thoại và email
    text = re.sub(r'\S+@\S+', '', text)  # Email
    text = re.sub(r'\d{10,}', '', text)  # Số điện thoại
    
    # Bước 5: Loại bỏ ký tự đặc biệt (giữ lại chữ, số, dấu câu cơ bản)
    before_special = len(text)
    text = re.sub(r'[^\w\s.,!?]', '', text)
    stats['special_chars_removed'] = before_special - len(text)
    
    # Bước 6: Loại bỏ số (nếu muốn)
    # text = re.sub(r'\d+', '', text)
    
    # Bước 7: Chuẩn hóa khoảng trắng
    before_spaces = len(text)
    text = re.sub(r'\s+', ' ', text).strip()
    stats['extra_spaces_removed'] = before_spaces - len(text)
    
    # Bước 8: Chuyển về chữ thường
    text = text.lower()
    
    stats['final_length'] = len(text)
    stats['reduction_percent'] = ((stats['original_length'] - stats['final_length']) / stats['original_length'] * 100) if stats['original_length'] > 0 else 0
    
    return text, stats


def normalize_data(df):
    """Chuẩn hóa dữ liệu với thống kê chi tiết"""
    print(f"\n{'='*70}")
    print(f"🧹 BƯỚC 2: CHUẨN HÓA DỮ LIỆU (CHI TIẾT)")
    print(f"{'='*70}")
    
    df_clean = df.copy()
    
    # Thống kê tổng hợp
    total_stats = {
        'urls_removed': 0,
        'mentions_removed': 0,
        'special_chars_removed': 0,
        'extra_spaces_removed': 0
    }
    
    print("\n🔄 Đang xử lý từng bình luận...")
    cleaned_texts = []
    cleaning_details = []
    
    for idx, text in enumerate(df_clean['review_text']):
        cleaned, stats = clean_text_detailed(text)
        cleaned_texts.append(cleaned)
        cleaning_details.append(stats)
        
        # Cập nhật thống kê tổng
        for key in total_stats:
            total_stats[key] += stats.get(key, 0)
        
        # Hiển thị tiến trình
        if (idx + 1) % 10000 == 0:
            print(f"  ✓ Đã xử lý: {idx + 1:,}/{len(df_clean):,}")
    
    df_clean['cleaned_text'] = cleaned_texts
    
    # Loại bỏ bình luận rỗng hoặc quá ngắn
    print("\n🔍 Đang lọc bình luận...")
    before_count = len(df_clean)
    
    # Loại bỏ bình luận rỗng
    df_clean = df_clean[df_clean['cleaned_text'].str.len() > 0]
    empty_removed = before_count - len(df_clean)
    
    # Loại bỏ bình luận quá ngắn (< 3 ký tự)
    before_short = len(df_clean)
    df_clean = df_clean[df_clean['cleaned_text'].str.len() >= 3]
    short_removed = before_short - len(df_clean)
    
    # Loại bỏ duplicate
    before_dup = len(df_clean)
    df_clean = df_clean.drop_duplicates(subset=['cleaned_text'])
    dup_removed = before_dup - len(df_clean)
    
    df_clean = df_clean.reset_index(drop=True)
    
    # Tính toán độ dài
    df_clean['original_length'] = df['review_text'].str.len()
    df_clean['cleaned_length'] = df_clean['cleaned_text'].str.len()
    df_clean['reduction_percent'] = ((df_clean['original_length'] - df_clean['cleaned_length']) / df_clean['original_length'] * 100).round(2)
    
    # Hiển thị kết quả chi tiết
    print(f"\n{'='*70}")
    print(f"✅ HOÀN TẤT CHUẨN HÓA!")
    print(f"{'='*70}")
    
    print(f"\n📊 Thống kê làm sạch:")
    print(f"   🔗 URLs đã loại bỏ: {total_stats['urls_removed']:,}")
    print(f"   👤 Mentions đã loại bỏ: {total_stats['mentions_removed']:,}")
    print(f"   ✂️  Ký tự đặc biệt đã loại bỏ: {total_stats['special_chars_removed']:,}")
    print(f"   ␣  Khoảng trắng thừa đã loại bỏ: {total_stats['extra_spaces_removed']:,}")
    
    print(f"\n📊 Thống kê lọc:")
    print(f"   🗑️  Bình luận rỗng: {empty_removed:,}")
    print(f"   📏 Bình luận quá ngắn (< 3 ký tự): {short_removed:,}")
    print(f"   🔄 Bình luận trùng lặp: {dup_removed:,}")
    
    print(f"\n📊 Kết quả:")
    print(f"   📥 Trước: {before_count:,} bình luận")
    print(f"   📤 Sau: {len(df_clean):,} bình luận")
    print(f"   ❌ Đã loại bỏ: {before_count - len(df_clean):,} ({(before_count - len(df_clean))/before_count*100:.2f}%)")
    
    print(f"\n📊 Độ dài văn bản:")
    print(f"   📏 Độ dài TB trước: {df_clean['original_length'].mean():.0f} ký tự")
    print(f"   📏 Độ dài TB sau: {df_clean['cleaned_length'].mean():.0f} ký tự")
    print(f"   📉 Giảm TB: {df_clean['reduction_percent'].mean():.1f}%")
    
    # Hiển thị ví dụ
    print(f"\n📝 Ví dụ chuẩn hóa (3 mẫu ngẫu nhiên):")
    samples = df_clean.sample(n=min(3, len(df_clean)))
    for idx, row in samples.iterrows():
        print(f"\n   {'─'*66}")
        print(f"   Trước ({row['original_length']} ký tự):")
        print(f"   {df.loc[idx, 'review_text'][:100]}...")
        print(f"\n   Sau ({row['cleaned_length']} ký tự, giảm {row['reduction_percent']:.1f}%):")
        print(f"   {row['cleaned_text'][:100]}...")
    
    return df_clean


# ============================================================================
# BƯỚC 3: GÁN NHÃN DỮ LIỆU (CHI TIẾT)
# ============================================================================

def get_sentiment_score(text):
    """Tính điểm cảm xúc sử dụng TextBlob"""
    try:
        blob = TextBlob(text)
        return blob.sentiment.polarity, blob.sentiment.subjectivity
    except:
        return 0.0, 0.0


def classify_sentiment_detailed(score, threshold=0.05):
    """
    Phân loại cảm xúc chi tiết
    
    Args:
        score: Điểm polarity (-1 đến 1)
        threshold: Ngưỡng phân loại
    
    Returns:
        tuple: (label, confidence, description)
    """
    if score > threshold:
        if score > 0.5:
            return 'Positive', 'High', 'Rất tích cực'
        elif score > 0.2:
            return 'Positive', 'Medium', 'Tích cực'
        else:
            return 'Positive', 'Low', 'Hơi tích cực'
    elif score < -threshold:
        if score < -0.5:
            return 'Negative', 'High', 'Rất tiêu cực'
        elif score < -0.2:
            return 'Negative', 'Medium', 'Tiêu cực'
        else:
            return 'Negative', 'Low', 'Hơi tiêu cực'
    else:
        return 'Neutral', 'Medium', 'Trung lập'


def label_data(df, sample_size=None):
    """Gán nhãn cảm xúc với thông tin chi tiết"""
    print(f"\n{'='*70}")
    print(f"🏷️  BƯỚC 3: GÁN NHÃN DỮ LIỆU (CHI TIẾT)")
    print(f"{'='*70}")
    
    # Lấy mẫu nếu dữ liệu quá lớn (chỉ khi có sample_size)
    if sample_size and len(df) > sample_size:
        print(f"📊 Dữ liệu lớn ({len(df):,}), lấy mẫu {sample_size:,} để xử lý nhanh hơn")
        df_labeled = df.sample(n=sample_size, random_state=42).copy()
    else:
        print(f"📊 Xử lý toàn bộ {len(df):,} bình luận")
        df_labeled = df.copy()
    
    print(f"\n🔄 Đang phân tích cảm xúc...")
    print(f"   ⏳ Quá trình này có thể mất vài phút...\n")
    
    # Phân tích từng bình luận
    sentiment_scores = []
    subjectivity_scores = []
    sentiment_labels = []
    confidence_levels = []
    descriptions = []
    
    for idx, text in enumerate(df_labeled['cleaned_text']):
        # Tính điểm
        polarity, subjectivity = get_sentiment_score(text)
        sentiment_scores.append(polarity)
        subjectivity_scores.append(subjectivity)
        
        # Phân loại
        label, confidence, description = classify_sentiment_detailed(polarity)
        sentiment_labels.append(label)
        confidence_levels.append(confidence)
        descriptions.append(description)
        
        # Hiển thị tiến trình
        if (idx + 1) % 1000 == 0:
            print(f"  ✓ Đã phân tích: {idx + 1:,}/{len(df_labeled):,}")
    
    # Thêm các cột mới
    df_labeled['sentiment_score'] = sentiment_scores
    df_labeled['subjectivity'] = subjectivity_scores
    df_labeled['sentiment_label'] = sentiment_labels
    df_labeled['confidence_level'] = confidence_levels
    df_labeled['sentiment_description'] = descriptions
    
    # Thống kê chi tiết
    print(f"\n{'='*70}")
    print(f"✅ HOÀN TẤT GÁN NHÃN!")
    print(f"{'='*70}")
    
    print(f"\n📊 Phân bố nhãn cảm xúc:")
    label_dist = df_labeled['sentiment_label'].value_counts()
    for label, count in label_dist.items():
        pct = (count / len(df_labeled)) * 100
        emoji = {'Positive': '😊', 'Negative': '😞', 'Neutral': '😐'}[label]
        print(f"   {emoji} {label:8s}: {count:6,} ({pct:5.1f}%)")
    
    print(f"\n📊 Phân bố độ tin cậy:")
    conf_dist = df_labeled['confidence_level'].value_counts()
    for conf, count in conf_dist.items():
        pct = (count / len(df_labeled)) * 100
        print(f"   • {conf:6s}: {count:6,} ({pct:5.1f}%)")
    
    print(f"\n📊 Thống kê điểm cảm xúc (Polarity):")
    print(f"   📈 Trung bình: {df_labeled['sentiment_score'].mean():6.3f}")
    print(f"   📊 Độ lệch chuẩn: {df_labeled['sentiment_score'].std():6.3f}")
    print(f"   📉 Min: {df_labeled['sentiment_score'].min():6.3f}")
    print(f"   📈 Max: {df_labeled['sentiment_score'].max():6.3f}")
    print(f"   📊 Median: {df_labeled['sentiment_score'].median():6.3f}")
    
    print(f"\n📊 Thống kê độ chủ quan (Subjectivity):")
    print(f"   📈 Trung bình: {df_labeled['subjectivity'].mean():6.3f}")
    print(f"   📊 Độ lệch chuẩn: {df_labeled['subjectivity'].std():6.3f}")
    
    # Phân tích theo nhãn
    print(f"\n📊 Điểm TB theo nhãn:")
    for label in ['Positive', 'Negative', 'Neutral']:
        if label in label_dist.index:
            subset = df_labeled[df_labeled['sentiment_label'] == label]
            avg_score = subset['sentiment_score'].mean()
            avg_subj = subset['subjectivity'].mean()
            emoji = {'Positive': '😊', 'Negative': '😞', 'Neutral': '😐'}[label]
            print(f"   {emoji} {label:8s}: Score={avg_score:6.3f}, Subjectivity={avg_subj:6.3f}")
    
    # Hiển thị ví dụ
    print(f"\n📝 Ví dụ phân loại:")
    
    for label in ['Positive', 'Negative', 'Neutral']:
        if label in label_dist.index:
            sample = df_labeled[df_labeled['sentiment_label'] == label].nlargest(1, 'sentiment_score' if label == 'Positive' else 'sentiment_score')
            if len(sample) > 0:
                row = sample.iloc[0]
                emoji = {'Positive': '😊', 'Negative': '😞', 'Neutral': '😐'}[label]
                print(f"\n   {emoji} {label} (Score: {row['sentiment_score']:.3f}, {row['confidence_level']} confidence):")
                print(f"      {row['cleaned_text'][:100]}...")
    
    return df_labeled


# ============================================================================
# BƯỚC 4: TRỰC QUAN HÓA
# ============================================================================

def visualize_distribution(df):
    """Trực quan hóa phân bố nhãn"""
    print(f"\n{'='*70}")
    print(f"📊 BƯỚC 4: TRỰC QUAN HÓA")
    print(f"{'='*70}")
    
    try:
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        label_counts = df['sentiment_label'].value_counts()
        label_colors = [COLORS[label] for label in label_counts.index]
        
        # Biểu đồ cột
        axes[0].bar(label_counts.index, label_counts.values, color=label_colors, alpha=0.7, edgecolor='black')
        axes[0].set_title('Phân bố nhãn cảm xúc', fontsize=14, fontweight='bold')
        axes[0].set_ylabel('Số lượng')
        axes[0].grid(axis='y', alpha=0.3)
        
        for i, (label, count) in enumerate(label_counts.items()):
            axes[0].text(i, count, f'{count:,}\n({count/len(df)*100:.1f}%)', 
                        ha='center', va='bottom', fontweight='bold')
        
        # Biểu đồ tròn
        axes[1].pie(label_counts.values, labels=label_counts.index, autopct='%1.1f%%',
                   colors=label_colors, startangle=90)
        axes[1].set_title('Tỷ lệ phân bố', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('distribution.png', dpi=300, bbox_inches='tight')
        print("✅ Đã lưu biểu đồ: distribution.png")
        plt.close()  # Đóng figure để tránh lỗi
        print("✅ Hoàn tất bước 4.1")
    except Exception as e:
        print(f"⚠️  Lỗi khi vẽ biểu đồ phân bố: {e}")
        print("   Tiếp tục với bước tiếp theo...")


def visualize_analysis(df):
    """Phân tích mối quan hệ các đặc trưng"""
    try:
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Độ dài vs Cảm xúc
        for label in ['Positive', 'Negative', 'Neutral']:
            data = df[df['sentiment_label'] == label]
            axes[0, 0].scatter(data['cleaned_length'], data['sentiment_score'], 
                              alpha=0.5, label=label, color=COLORS[label], s=20)
        axes[0, 0].axhline(0, color='red', linestyle='--', alpha=0.5)
        axes[0, 0].set_xlabel('Độ dài (ký tự)')
        axes[0, 0].set_ylabel('Điểm cảm xúc')
        axes[0, 0].set_title('Độ dài vs Cảm xúc')
        axes[0, 0].legend()
        axes[0, 0].grid(alpha=0.3)
        
        # 2. Box plot
        df.boxplot(column='sentiment_score', by='sentiment_label', ax=axes[0, 1])
        axes[0, 1].set_title('Phân bố điểm theo nhãn')
        axes[0, 1].set_xlabel('Nhãn')
        axes[0, 1].set_ylabel('Điểm cảm xúc')
        
        # 3. Độ dài TB
        avg_length = df.groupby('sentiment_label')['cleaned_length'].mean().sort_values()
        axes[1, 0].barh(avg_length.index, avg_length.values, 
                       color=[COLORS[label] for label in avg_length.index], alpha=0.7, edgecolor='black')
        axes[1, 0].set_xlabel('Độ dài TB (ký tự)')
        axes[1, 0].set_title('Độ dài TB theo nhãn')
        axes[1, 0].grid(axis='x', alpha=0.3)
        for i, v in enumerate(avg_length.values):
            axes[1, 0].text(v, i, f' {v:.0f}', va='center', fontweight='bold')
        
        # 4. Likes vs Cảm xúc
        for label in ['Positive', 'Negative', 'Neutral']:
            data = df[df['sentiment_label'] == label]
            axes[1, 1].scatter(data['likes'] + 1, data['sentiment_score'], 
                              alpha=0.5, label=label, color=COLORS[label], s=20)
        axes[1, 1].set_xlabel('Likes')
        axes[1, 1].set_ylabel('Điểm cảm xúc')
        axes[1, 1].set_title('Likes vs Cảm xúc')
        axes[1, 1].set_xscale('log')
        axes[1, 1].legend()
        axes[1, 1].grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('analysis.png', dpi=300, bbox_inches='tight')
        print("✅ Đã lưu biểu đồ: analysis.png")
        plt.close()  # Đóng figure để tránh lỗi
        print("✅ Hoàn tất bước 4.2")
    except Exception as e:
        print(f"⚠️  Lỗi khi vẽ biểu đồ phân tích: {e}")
        print("   Tiếp tục với bước tiếp theo...")


# ============================================================================
# BƯỚC 5: PHÂN TÍCH SÂU
# ============================================================================

def deep_analysis(df):
    """Phân tích sâu kết quả"""
    print(f"\n{'='*70}")
    print(f"🔬 BƯỚC 5: PHÂN TÍCH SÂU")
    print(f"{'='*70}")
    
    # Thống kê tổng hợp
    summary = df.groupby('sentiment_label').agg({
        'sentiment_score': ['mean', 'std', 'min', 'max'],
        'cleaned_length': ['mean', 'std'],
        'likes': ['sum', 'mean', 'median']
    }).round(3)
    
    print("\n📊 Thống kê tổng hợp:")
    print(summary)
    
    # Top bình luận
    print(f"\n🔝 Top 3 tích cực nhất:")
    for idx, row in df.nlargest(3, 'sentiment_score').iterrows():
        print(f"   Score: {row['sentiment_score']:.3f} | {row['cleaned_text'][:80]}...")
    
    print(f"\n🔻 Top 3 tiêu cực nhất:")
    for idx, row in df.nsmallest(3, 'sentiment_score').iterrows():
        print(f"   Score: {row['sentiment_score']:.3f} | {row['cleaned_text'][:80]}...")
    
    # Ma trận tương quan
    print(f"\n📈 Ma trận tương quan:")
    corr = df[['sentiment_score', 'cleaned_length', 'likes']].corr()
    print(corr)


# ============================================================================
# BƯỚC 6: ỨNG DỤNG DEMO
# ============================================================================

def analyze_sentiment_demo(text):
    """Phân tích cảm xúc cho văn bản mới"""
    cleaned, stats = clean_text_detailed(text)
    polarity, subjectivity = get_sentiment_score(cleaned)
    label, confidence, description = classify_sentiment_detailed(polarity)
    emoji = {'Positive': '😊', 'Negative': '😞', 'Neutral': '😐'}[label]
    
    print(f"\n{'='*70}")
    print(f"📝 Văn bản gốc:")
    print(f"   {text}")
    print(f"\n🧹 Văn bản đã làm sạch:")
    print(f"   {cleaned}")
    print(f"\n📊 Thống kê làm sạch:")
    print(f"   • Độ dài: {stats['original_length']} → {stats['final_length']} ký tự")
    print(f"   • Giảm: {stats['reduction_percent']:.1f}%")
    print(f"   • URLs loại bỏ: {stats['urls_removed']}")
    print(f"   • Mentions loại bỏ: {stats['mentions_removed']}")
    print(f"\n🎯 Kết quả phân tích:")
    print(f"   {emoji} Nhãn: {label}")
    print(f"   📊 Mô tả: {description}")
    print(f"   🎚️  Độ tin cậy: {confidence}")
    print(f"   📈 Điểm cảm xúc: {polarity:.3f}")
    print(f"   📊 Độ chủ quan: {subjectivity:.3f}")
    print(f"{'='*70}")


def demo_application():
    """Demo ứng dụng"""
    print(f"\n{'='*70}")
    print(f"🎬 BƯỚC 6: ỨNG DỤNG DEMO")
    print(f"{'='*70}")
    
    # Phần 1: Test với 5 mẫu có sẵn
    test_texts = [
        "This movie is absolutely amazing! Best film ever!",
        "Terrible movie, waste of time.",
        "It was okay, nothing special.",
        "I love this so much! Can't wait to watch it again!",
        "Worst experience ever. Very disappointed."
    ]
    
    print("\n🧪 PHẦN 1: Test với 5 mẫu văn bản có sẵn:\n")
    for i, text in enumerate(test_texts, 1):
        print(f"\n{'─'*70}")
        print(f"Mẫu {i}/5:")
        analyze_sentiment_demo(text)
    
    # Phần 2: Cho phép người dùng tự nhập
    print(f"\n{'='*70}")
    print(f"🎯 PHẦN 2: TỰ NHẬP VĂN BẢN ĐỂ PHÂN TÍCH")
    print(f"{'='*70}")
    print("\n💡 Bạn có thể nhập bất kỳ văn bản tiếng Anh nào để phân tích cảm xúc.")
    print("   Nhập 'quit', 'exit', hoặc 'q' để bỏ qua phần này.\n")
    
    while True:
        try:
            print(f"{'─'*70}")
            user_input = input("📝 Nhập văn bản của bạn (hoặc 'quit' để thoát): ").strip()
            
            # Kiểm tra lệnh thoát
            if user_input.lower() in ['quit', 'exit', 'q', '']:
                print("\n✅ Đã kết thúc phần nhập tự do.")
                break
            
            # Kiểm tra độ dài
            if len(user_input) < 3:
                print("⚠️  Văn bản quá ngắn! Vui lòng nhập ít nhất 3 ký tự.")
                continue
            
            # Phân tích
            analyze_sentiment_demo(user_input)
            
            # Hỏi có muốn tiếp tục không
            print(f"\n{'─'*70}")
            continue_choice = input("❓ Bạn có muốn phân tích văn bản khác không? (y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes', 'có', 'c']:
                print("\n✅ Đã kết thúc phần nhập tự do.")
                break
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Đã hủy bởi người dùng.")
            break
        except Exception as e:
            print(f"\n❌ Lỗi: {e}")
            print("Vui lòng thử lại.")
    
    print(f"\n{'='*70}")
    print("🎉 HOÀN TẤT DEMO ỨNG DỤNG!")
    print(f"{'='*70}")


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Hàm chính chạy toàn bộ pipeline"""
    print("\n" + "="*70)
    print("🎯 ĐỒ ÁN: PHÂN LỚP SENTIMENT ANALYSIS VỚI YOUTUBE API")
    print("="*70)
    print("\n👨‍🎓 Sinh viên thực hiện:")
    print("   1. Đỗ Tài Khải Nguyên (MSSV: 52300230)")
    print("   2. Tống Phương Nam")
    print("\n" + "="*70)
    
    try:
        # Bước 1: Thu thập dữ liệu
        df_raw = get_youtube_comments(VIDEO_INFO, API_KEYS, target_count=100000)
        df_raw.to_csv('youtube_raw_data.csv', index=False, encoding='utf-8-sig')
        print("💾 Đã lưu: youtube_raw_data.csv")
        
        # Bước 2: Chuẩn hóa
        df_clean = normalize_data(df_raw)
        df_clean.to_csv('youtube_clean_data.csv', index=False, encoding='utf-8-sig')
        print("💾 Đã lưu: youtube_clean_data.csv")
        
        # Bước 3: Gán nhãn (xử lý toàn bộ dữ liệu)
        df_labeled = label_data(df_clean, sample_size=None)
        df_labeled.to_csv('youtube_labeled_data.csv', index=False, encoding='utf-8-sig')
        print("💾 Đã lưu: youtube_labeled_data.csv")
        
        # Bước 4: Trực quan hóa
        visualize_distribution(df_labeled)
        visualize_analysis(df_labeled)
        
        # Bước 5: Phân tích sâu
        deep_analysis(df_labeled)
        
        # Bước 6: Demo ứng dụng
        demo_application()
        
        print(f"\n{'='*70}")
        print("✅ HOÀN TẤT TẤT CẢ CÁC BƯỚC!")
        print(f"{'='*70}")
        print("\n📁 Các file đã tạo:")
        print("   - youtube_raw_data.csv")
        print("   - youtube_clean_data.csv")
        print("   - youtube_labeled_data.csv")
        print("   - distribution.png")
        print("   - analysis.png")
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
