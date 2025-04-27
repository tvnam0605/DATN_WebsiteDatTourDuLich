import mysql.connector
from mysql.connector import Error
import pandas as pd
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, jsonify, request
from nltk.tokenize import word_tokenize
pd.options.mode.chained_assignment = None

app = Flask(__name__)
# Danh sách stop words tiếng Việt
vietnamese_stopwords = [
    'và', 'là', 'của', 'các', 'đã', 'trong', 'khi', 'này', 'một',
    'những', 'được', 'với', 'cho', 'thì', 'tại', 'bởi', 'về', 'để',
    'nếu', 'sẽ', 'không', 'có', 'đây', 'đó', 'này', 'thấy', 'ra',
    'phải', 'ai', 'gì', 'nào', 'lại', 'hơn', 'như', 'vậy', 'chỉ',
    'làm', 'lúc', 'người', 'năm', 'ngày'
]
def create_connection():
    """
    Create a connection to the MySQL database using SQLAlchemy.

    Returns:
        engine: A SQLAlchemy engine object.
    """
    try:
        engine = create_engine('mysql+mysqlconnector://root:@localhost/travela')
        print("Kết nối tới MySQL database thành công!")
        return engine
    except Error as e:
        print(f"Đã xảy ra lỗi khi kết nối tới MySQL: {e}")
        return None

def close_connection(engine):
    """
    Close the connection to the MySQL database.

    Args:
        engine: The SQLAlchemy engine object to close.
    """
    if engine:
        engine.dispose()
        print("Kết nối đã được đóng.")

def fetch_tours(engine):
    """
    Fetch tour data from the database.

    Args:
        engine: The SQLAlchemy engine object.

    Returns:
        DataFrame: A DataFrame containing the tour data.
    """
    try:
        query = "SELECT * FROM tbl_tours;"
        df_tours = pd.read_sql(query, engine)
        print("Dữ liệu tours đã được lấy thành công!")
        return df_tours
    except Error as e:
        print(f"Đã xảy ra lỗi khi truy vấn dữ liệu: {e}")
        return pd.DataFrame()

def combine_features(row):
    """
    Combine selected features into a single string.

    Args:
        row: A row of the DataFrame.

    Returns:
        str: A combined string of features.
    """
    features = ['title', 'description', 'time', 'priceAdult', 'destination']
    return ' '.join([str(row[feature]) for feature in features if feature in row and pd.notnull(row[feature])])

@app.route('/api/tour-recommendations', methods=['GET'])
def get_recommendations():
    engine = create_connection()
    if engine:
        tours_df = fetch_tours(engine)
        if not tours_df.empty:
            # Kiểm tra sự tồn tại của các cột cần thiết
            required_columns = ['tourId', 'title', 'description', 'time', 'priceAdult', 'destination']
            for col in required_columns:
                if col not in tours_df.columns:
                    return jsonify({"error": f"Cột '{col}' không tồn tại trong dữ liệu."}), 400

            # Kết hợp các đặc điểm vào một cột
            tours_df['combineFeatures'] = tours_df.apply(combine_features, axis=1)

            # Tính toán TF-IDF và độ tương tự cosine
            tfidf = TfidfVectorizer()
            tfidf_matrix = tfidf.fit_transform(tours_df['combineFeatures'])
            cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

            # Lấy tour_id từ query parameter
            tour_id = request.args.get('tour_id')

            # Kiểm tra nếu tour_id hợp lệ
            if not tour_id or not tour_id.isdigit():
                return jsonify({"error": "Invalid or missing 'tour_id' parameter"}), 400

            tour_id = int(tour_id)  # Chuyển tour_id thành số nguyên

            # Kiểm tra nếu tour_id tồn tại trong cột 'tourId' của DataFrame
            if tour_id not in tours_df['tourId'].values:
                return jsonify({"error": "Invalid tour ID"}), 400

            # Lấy chỉ số của tour_id trong DataFrame
            tour_index = tours_df[tours_df['tourId'] == tour_id].index[0]

            # Tính toán điểm tương tự cho tour được chọn
            sim_scores = list(enumerate(cosine_sim[tour_index]))
            sim_scores_sorted = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:4]  # Lấy 3 tour tương tự nhất

            # Lấy chỉ số của 3 tour tương tự nhất
            similar_tours_indices = [i[0] for i in sim_scores_sorted]

            # Chuẩn bị dữ liệu phản hồi
            related_tours = tours_df.iloc[similar_tours_indices]
            related_tours_list = related_tours['tourId'].tolist()

            close_connection(engine)
            return jsonify({"related_tours": related_tours_list})

    return jsonify({"error": "Unable to connect to the database"}), 500


@app.route('/api/user-recommendations', methods=['GET'])
def get_user_recommendations():
    user_id = request.args.get('user_id')  # Lấy user_id từ query parameter

    if not user_id or not user_id.isdigit():
        return jsonify({"error": "Invalid or missing 'user_id' parameter"}), 400

    user_id = int(user_id)  # Chuyển user_id thành số nguyên

    # Kết nối cơ sở dữ liệu
    engine = create_connection()
    try:
        # Lấy dữ liệu từ các bảng cần thiết
        bookings_query = "SELECT * FROM tbl_booking WHERE userId = %(user_id)s;"
        reviews_query = "SELECT * FROM tbl_reviews WHERE userId = %(user_id)s;"
        tours_query = "SELECT * FROM tbl_tours WHERE availability = 1;"

        user_bookings = pd.read_sql(bookings_query, engine, params={"user_id": user_id})
        user_reviews = pd.read_sql(reviews_query, engine, params={"user_id": user_id})
        all_tours = pd.read_sql(tours_query, engine)

        # Kiểm tra và xử lý dữ liệu rỗng
        if user_bookings.empty and user_reviews.empty:
            interacted_tours = []
        elif user_bookings.empty:
            interacted_tours = user_reviews['tourId'].unique()
        elif user_reviews.empty:
            interacted_tours = user_bookings['tourId'].unique()
        else:
            # Nếu cả hai không rỗng
            interacted_tours = pd.concat([user_bookings['tourId'], user_reviews['tourId']]).unique()
        # print(user_bookings, user_reviews)
        # Loại bỏ các tour mà user đã tương tác khỏi danh sách gợi ý
        candidate_tours = all_tours[~all_tours['tourId'].isin(interacted_tours)]
        # print(candidate_tours)

        if candidate_tours.empty:
            return jsonify({"message": "No tours available for recommendations."}), 404

        # Kết hợp các đặc điểm để gợi ý
        all_tours['combineFeatures'] = all_tours.apply(combine_features, axis=1)
        candidate_tours['combineFeatures'] = candidate_tours.apply(combine_features, axis=1)

        # Tính toán TF-IDF cho tất cả các tour
        tfidf = TfidfVectorizer()
        tfidf_matrix_all = tfidf.fit_transform(all_tours['combineFeatures'])

        # Tạo ma trận tương tự cosine cho tất cả các tour
        cosine_sim = cosine_similarity(tfidf_matrix_all, tfidf_matrix_all)

        # Tính toán độ tương tự giữa các tour người dùng đã tương tác và các tour còn lại
        interacted_indices = all_tours[all_tours['tourId'].isin(interacted_tours)].index
        candidate_indices = candidate_tours.index

        sim_scores = cosine_sim[interacted_indices][:, candidate_indices].mean(axis=0)
        candidate_tours['similarity'] = sim_scores

        # Tính điểm rating trung bình cho từng tour (dựa trên đánh giá của tất cả người dùng)
        avg_rating = user_reviews.groupby('tourId')['rating'].mean().reset_index()
        avg_rating.columns = ['tourId', 'avg_rating']

        # Kết hợp điểm rating trung bình với candidate_tours
        candidate_tours = pd.merge(candidate_tours, avg_rating, on='tourId', how='left')

        # Sắp xếp theo điểm tương tự cao nhất và rating cao nhất
        recommended_tours = candidate_tours.sort_values(by=['similarity', 'avg_rating'], ascending=[False, False]).head(
            6)

        # Chuẩn bị dữ liệu phản hồi
        # result = recommended_tours[['tourId', 'title', 'description', 'destination', 'avg_rating']].to_dict(
        #     orient='records')
        result = recommended_tours['tourId'].tolist()

        return jsonify({"recommended_tours": result})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

    finally:
        close_connection(engine)


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


# API tìm kiếm tour
@app.route('/api/search-tours', methods=['GET'])
def search_tours():
    """
    API tìm kiếm tour dựa trên input từ người dùng sau khi xử lý dữ liệu đầu vào.
    """
    user_input = request.args.get('keyword')  # Lấy input từ người dùng
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
        sim_scores_sorted = sorted(sim_scores, key=lambda x: x[1], reverse=True)[:9]  # Top 9 kết quả

        # Lấy thông tin các tour tương tự
        similar_tours_indices = [i[0] for i in sim_scores_sorted]
        related_tours = tours_df.iloc[similar_tours_indices]

        # Chuẩn bị dữ liệu trả về
        # result = related_tours[['tourId', 'title', 'description', 'destination']].to_dict(orient='records')
        # Chuẩn bị dữ liệu phản hồi
        related_tours_list = related_tours['tourId'].tolist()
        return jsonify({"related_tours": related_tours_list})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)  
