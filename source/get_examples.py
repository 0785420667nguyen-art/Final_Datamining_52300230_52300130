import pandas as pd

# Đọc dữ liệu
df = pd.read_csv('youtube_labeled_data.csv')

print("="*70)
print("VÍ DỤ THỰC TẾ TỪ DỮ LIỆU YOUTUBE")
print("="*70)

# 1. POSITIVE - Lấy comment tích cực nhất
print("\n😊 TRƯỜNG HỢP 1: POSITIVE (Tích cực)")
print("-"*70)
pos = df[df['sentiment_label'] == 'Positive'].nlargest(1, 'sentiment_score').iloc[0]
print(f"Điểm cảm xúc: {pos['sentiment_score']:.3f}")
print(f"Độ tin cậy: {pos['confidence_level']}")
print(f"Mô tả: {pos['sentiment_description']}")
print(f"\nBình luận gốc:")
print(f"  {pos['review_text'][:300]}")
print(f"\nBình luận đã làm sạch:")
print(f"  {pos['cleaned_text'][:300]}")

# 2. NEGATIVE - Lấy comment tiêu cực nhất
print("\n\n😞 TRƯỜNG HỢP 2: NEGATIVE (Tiêu cực)")
print("-"*70)
neg = df[df['sentiment_label'] == 'Negative'].nsmallest(1, 'sentiment_score').iloc[0]
print(f"Điểm cảm xúc: {neg['sentiment_score']:.3f}")
print(f"Độ tin cậy: {neg['confidence_level']}")
print(f"Mô tả: {neg['sentiment_description']}")
print(f"\nBình luận gốc:")
print(f"  {neg['review_text'][:300]}")
print(f"\nBình luận đã làm sạch:")
print(f"  {neg['cleaned_text'][:300]}")

# 3. NEUTRAL - Lấy comment trung lập (gần 0 nhất)
print("\n\n😐 TRƯỜNG HỢP 3: NEUTRAL (Trung lập)")
print("-"*70)
neu_df = df[df['sentiment_label'] == 'Neutral']
neu = neu_df.iloc[(neu_df['sentiment_score'] - 0).abs().argsort()[:1]].iloc[0]
print(f"Điểm cảm xúc: {neu['sentiment_score']:.3f}")
print(f"Độ tin cậy: {neu['confidence_level']}")
print(f"Mô tả: {neu['sentiment_description']}")
print(f"\nBình luận gốc:")
print(f"  {neu['review_text'][:300]}")
print(f"\nBình luận đã làm sạch:")
print(f"  {neu['cleaned_text'][:300]}")

print("\n" + "="*70)
print("TỔNG KẾT")
print("="*70)
print(f"Tổng số bình luận: {len(df):,}")
print(f"  😊 Positive: {len(df[df['sentiment_label'] == 'Positive']):,} ({len(df[df['sentiment_label'] == 'Positive'])/len(df)*100:.1f}%)")
print(f"  😐 Neutral:  {len(df[df['sentiment_label'] == 'Neutral']):,} ({len(df[df['sentiment_label'] == 'Neutral'])/len(df)*100:.1f}%)")
print(f"  😞 Negative: {len(df[df['sentiment_label'] == 'Negative']):,} ({len(df[df['sentiment_label'] == 'Negative'])/len(df)*100:.1f}%)")
print("="*70)
