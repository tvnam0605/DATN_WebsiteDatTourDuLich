from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from nltk.tokenize import word_tokenize
import nltk
# nltk.data.path.append('C:/Users/minhd/nltk_data')

# Tạo ứng dụng Flask
app = Flask(__name__)

# Danh sách stop words tiếng Việt
vietnamese_stopwords = [
    'và', 'là', 'của', 'các', 'đã', 'trong', 'khi', 'này', 'một',
    'những', 'được', 'với', 'cho', 'thì', 'tại', 'bởi', 'về', 'để',
    'nếu', 'sẽ', 'không', 'có', 'đây', 'đó', 'này', 'thấy', 'ra',
    'phải', 'ai', 'gì', 'nào', 'lại', 'hơn', 'như', 'vậy', 'chỉ',
    'làm', 'lúc', 'người', 'năm', 'ngày'
    # Thêm các từ không cần thiết khác...
]


# Hàm tiền xử lý văn bản
def preprocess_text(text):
    """
    
    Tiền xử lý văn bản bằng cách loại bỏ stop words và giữ lại các từ quan trọng.
    Args:
        text (str): Văn bản gốc.
    Returns:
        str: Văn bản đã được xử lý.
    """
    # Chuyển thành chữ thường
    text = text.lower()

    # Tokenize văn bản
    tokens = word_tokenize(text)

    # Loại bỏ stop words
    processed_tokens = [word for word in tokens if word not in vietnamese_stopwords and word.isalnum()]

    # Kết hợp lại thành chuỗi
    return ' '.join(processed_tokens)


# Kết nối cơ sở dữ liệu (giả sử bạn đã có hàm kết nối và truy vấn dữ liệu)
def create_connection():
    from sqlalchemy import create_engine
    engine = create_engine('mysql+mysqlconnector://root:@localhost/travela')
    return engine


def fetch_tours(engine):
    """
    Lấy dữ liệu tour từ cơ sở dữ liệu.
    """
    query = "SELECT * FROM tbl_tours;"
    df_tours = pd.read_sql(query, engine)
    print(df_tours)
    return df_tours


# API tìm kiếm tour
@app.route('/api/search-tours', methods=['GET'])
def search_tours():
    """
    API tìm kiếm tour dựa trên input từ người dùng sau khi xử lý dữ liệu đầu vào.
    """
    user_input = request.args.get('query')  # Lấy input từ người dùng
    if not user_input:
        return jsonify({"error": "Missing search query"}), 400

    # Kết nối cơ sở dữ liệu và lấy dữ liệu
    engine = create_connection()
    try:
        tours_df = fetch_tours(engine)
        if tours_df.empty:
            return jsonify({"error": "No tours found"}), 404

        # Kết hợp các cột để tạo chuỗi tìm kiếm
        tours_df['combineFeatures'] = tours_df.apply(
            lambda row: f"{row['title']} {row['description']} {row['destination']}", axis=1
        )

        # Tiền xử lý văn bản trong cột dữ liệu và input
        tours_df['processedFeatures'] = tours_df['combineFeatures'].apply(preprocess_text)
        processed_input = preprocess_text(user_input)

        # Tính toán TF-IDF
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(tours_df['processedFeatures'])
        input_vector = tfidf.transform([processed_input])

        # Tính độ tương tự cosine
        cosine_sim = cosine_similarity(input_vector, tfidf_matrix)

        # Xếp hạng kết quả tìm kiếm
        sim_scores = list(enumerate(cosine_sim[0]))
        sim_scores_sorted = sorted(sim_scores, key=lambda x: x[1], reverse=True)[:9]  # Top 5 kết quả

        # Lấy thông tin các tour tương tự
        similar_tours_indices = [i[0] for i in sim_scores_sorted]
        related_tours = tours_df.iloc[similar_tours_indices]

        # Chuẩn bị dữ liệu trả về
        result = related_tours[['tourId', 'title', 'description', 'destination']].to_dict(orient='records')
        return jsonify({"related_tours": result})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
