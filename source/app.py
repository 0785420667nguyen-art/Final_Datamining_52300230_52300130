"""
WEB APP PHÂN TÍCH CẢM XÚC
Ứng dụng web đơn giản sử dụng Flask

Sinh viên thực hiện:
1. Đỗ Tài Khải Nguyên (MSSV: 52300230)
2. Tống Phương Nam
"""

from flask import Flask, render_template, request, jsonify
import re
from textblob import TextBlob
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

# Tạo thư mục lưu lịch sử nếu chưa có
if not os.path.exists('history'):
    os.makedirs('history')

HISTORY_FILE = 'history/analysis_history.csv'


def clean_text(text):
    """Làm sạch văn bản"""
    if not isinstance(text, str):
        return ""
    
    # Loại bỏ URL
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Loại bỏ mention
    text = re.sub(r'@\w+', '', text)
    # Loại bỏ hashtags
    text = re.sub(r'#\w+', '', text)
    # Loại bỏ email
    text = re.sub(r'\S+@\S+', '', text)
    # Loại bỏ ký tự đặc biệt
    text = re.sub(r'[^\w\s.,!?]', '', text)
    # Chuẩn hóa khoảng trắng
    text = re.sub(r'\s+', ' ', text).strip()
    # Chuyển về chữ thường
    text = text.lower()
    
    return text


def get_sentiment_score(text):
    """Tính điểm cảm xúc"""
    try:
        blob = TextBlob(text)
        return blob.sentiment.polarity, blob.sentiment.subjectivity
    except:
        return 0.0, 0.0


def classify_sentiment(score):
    """Phân loại cảm xúc"""
    if score > 0.1:
        if score > 0.5:
            return 'Positive', 'High', 'Rất tích cực', '😊', 'success'
        elif score > 0.2:
            return 'Positive', 'Medium', 'Tích cực', '😊', 'success'
        else:
            return 'Positive', 'Low', 'Hơi tích cực', '🙂', 'info'
    elif score < -0.1:
        if score < -0.5:
            return 'Negative', 'High', 'Rất tiêu cực', '😞', 'danger'
        elif score < -0.2:
            return 'Negative', 'Medium', 'Tiêu cực', '😞', 'danger'
        else:
            return 'Negative', 'Low', 'Hơi tiêu cực', '😕', 'warning'
    else:
        return 'Neutral', 'Medium', 'Trung lập', '😐', 'secondary'


def save_to_history(original_text, cleaned_text, label, score, confidence):
    """Lưu kết quả vào lịch sử"""
    try:
        data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'original_text': original_text,
            'cleaned_text': cleaned_text,
            'sentiment_label': label,
            'sentiment_score': score,
            'confidence_level': confidence
        }
        
        # Đọc file hiện tại hoặc tạo mới
        if os.path.exists(HISTORY_FILE):
            df = pd.read_csv(HISTORY_FILE)
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        else:
            df = pd.DataFrame([data])
        
        # Lưu file (giữ tối đa 100 bản ghi gần nhất)
        df = df.tail(100)
        df.to_csv(HISTORY_FILE, index=False, encoding='utf-8-sig')
    except Exception as e:
        print(f"Lỗi khi lưu lịch sử: {e}")


@app.route('/')
def index():
    """Trang chủ"""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """API phân tích cảm xúc"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        # Validate
        if not text:
            return jsonify({
                'success': False,
                'error': 'Vui lòng nhập văn bản!'
            })
        
        if len(text) < 3:
            return jsonify({
                'success': False,
                'error': 'Văn bản quá ngắn! Vui lòng nhập ít nhất 3 ký tự.'
            })
        
        # Xử lý
        original_length = len(text)
        cleaned = clean_text(text)
        cleaned_length = len(cleaned)
        
        if cleaned_length == 0:
            return jsonify({
                'success': False,
                'error': 'Văn bản không chứa nội dung hợp lệ sau khi làm sạch!'
            })
        
        polarity, subjectivity = get_sentiment_score(cleaned)
        label, confidence, description, emoji, badge_class = classify_sentiment(polarity)
        
        # Lưu lịch sử
        save_to_history(text, cleaned, label, polarity, confidence)
        
        # Trả kết quả
        result = {
            'success': True,
            'original_text': text,
            'cleaned_text': cleaned,
            'original_length': original_length,
            'cleaned_length': cleaned_length,
            'reduction_percent': round((original_length - cleaned_length) / original_length * 100, 1) if original_length > 0 else 0,
            'sentiment': {
                'label': label,
                'confidence': confidence,
                'description': description,
                'emoji': emoji,
                'badge_class': badge_class,
                'score': round(polarity, 3),
                'subjectivity': round(subjectivity, 3)
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Lỗi: {str(e)}'
        })


@app.route('/history')
def history():
    """Xem lịch sử phân tích"""
    try:
        if os.path.exists(HISTORY_FILE):
            df = pd.read_csv(HISTORY_FILE)
            # Lấy 20 bản ghi gần nhất
            df = df.tail(20).iloc[::-1]  # Đảo ngược để mới nhất lên đầu
            records = df.to_dict('records')
            return jsonify({
                'success': True,
                'records': records,
                'total': len(records)
            })
        else:
            return jsonify({
                'success': True,
                'records': [],
                'total': 0
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Lỗi: {str(e)}'
        })


@app.route('/stats')
def stats():
    """Thống kê tổng quan"""
    try:
        if os.path.exists(HISTORY_FILE):
            df = pd.read_csv(HISTORY_FILE)
            
            total = len(df)
            positive = len(df[df['sentiment_label'] == 'Positive'])
            negative = len(df[df['sentiment_label'] == 'Negative'])
            neutral = len(df[df['sentiment_label'] == 'Neutral'])
            
            avg_score = df['sentiment_score'].mean()
            
            return jsonify({
                'success': True,
                'stats': {
                    'total': total,
                    'positive': positive,
                    'negative': negative,
                    'neutral': neutral,
                    'positive_percent': round(positive / total * 100, 1) if total > 0 else 0,
                    'negative_percent': round(negative / total * 100, 1) if total > 0 else 0,
                    'neutral_percent': round(neutral / total * 100, 1) if total > 0 else 0,
                    'avg_score': round(avg_score, 3) if total > 0 else 0
                }
            })
        else:
            return jsonify({
                'success': True,
                'stats': {
                    'total': 0,
                    'positive': 0,
                    'negative': 0,
                    'neutral': 0,
                    'positive_percent': 0,
                    'negative_percent': 0,
                    'neutral_percent': 0,
                    'avg_score': 0
                }
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Lỗi: {str(e)}'
        })


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 SENTIMENT ANALYSIS WEB APP")
    print("="*70)
    print("\n👨‍🎓 Sinh viên thực hiện:")
    print("   1. Đỗ Tài Khải Nguyên (MSSV: 52300230)")
    print("   2. Tống Phương Nam")
    print("\n" + "="*70)
    print("\n🌐 Mở trình duyệt và truy cập:")
    print("   http://localhost:5000")
    print("\n⚠️  Nhấn Ctrl+C để dừng server")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
