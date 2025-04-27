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

        # Loại bỏ các tour mà user đã tương tác khỏi danh sách gợi ý
        candidate_tours = all_tours[~all_tours['tourId'].isin(interacted_tours)]

        if candidate_tours.empty:
            return jsonify({"message": "No tours available for recommendations."}), 404

        # Kết hợp các đặc điểm để gợi ý
        all_tours['combineFeatures'] = all_tours.apply(combine_features, axis=1)
        candidate_tours.loc[:, 'combineFeatures'] = candidate_tours.apply(combine_features, axis=1)

        # Tính toán TF-IDF cho tất cả các tour
        tfidf = TfidfVectorizer()
        tfidf_matrix_all = tfidf.fit_transform(all_tours['combineFeatures'])

        # Tạo ma trận tương tự cosine cho tất cả các tour
        cosine_sim = cosine_similarity(tfidf_matrix_all, tfidf_matrix_all)

        # Tính toán độ tương tự giữa các tour người dùng đã tương tác và các tour còn lại
        interacted_indices = all_tours[all_tours['tourId'].isin(interacted_tours)].index
        candidate_indices = candidate_tours.index

        sim_scores = cosine_sim[interacted_indices][:, candidate_indices].mean(axis=0)
        candidate_tours.loc[:, 'similarity'] = sim_scores
        # print(sim_scores)

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
