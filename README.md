# Website Đặt Tour Du Lịch - Hệ Thống Gợi Ý Tour

## Mục Lục
- [Giới Thiệu](#giới-thiệu)
- [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
- [Hướng Dẫn Cài Đặt](#hướng-dẫn-cài-đặt)
- [Hướng Dẫn Chạy](#hướng-dẫn-chạy)
- [Đóng Góp](#đóng-góp)
- [Liên Hệ](#liên-hệ)

## Giới thiệu
Dự án này bao gồm hai phần:

- **Website đặt tour du lịch**: Xây dựng website bằng PHP thuần, cho phép người dùng tìm kiếm, đặt tour, quản lý thông tin cá nhân.
- **Hệ thống gợi ý tour du lịch**: Ứng dụng Flask API Python, gợi ý tour cho người dùng dựa trên sở thích, lịch sử tìm kiếm và đặt tour.

Mục tiêu nhằm xây dựng hệ thống hỗ trợ trải nghiệm người dùng tốt hơn khi tham khảo và đặt tour du lịch.

---

## Yêu cầu hệ thống

**Website PHP:**
- PHP >= 7.4
- MySQL >= 5.7
- XAMPP hoặc tương đương

**Hệ thống gợi ý Python:**
- Python >= 3.8

**Thư viện Python:**
- Flask
- Flask-Cors
- Flask-SQLAlchemy
- pandas
- scikit-learn
- numpy
- underthesea
- vncorenlp
- PyMySQL

**Phần mềm hỗ trợ:**
- phpMyAdmin (quản lý database)
- Postman (test API - tùy chọn)

---

## Hướng dẫn cài đặt

### Clone repository:

  ```bash
  git clone https://github.com/tvnam0605/DATN_WebsiteDatTourDuLich.git
  cd DATN_WebsiteDatTourDuLich
  # Di chuyển vào thư mục recommendation
  cd recommendation
  ```

# Tạo môi trường ảo
  ```bash
  python -m venv venv
  
  # Kích hoạt môi trường ảo
  venv\Scripts\activate       # Windows
  source venv/bin/activate    # Linux/Mac
  ```
# Cài đặt các thư viện từ requirements.txt
  ```bash
  pip install -r requirements.txt
  ```
## Hướng dẫn chạy
### Website đặt tour du lịch
1. Bật Apache và MySQL trong XAMPP
2. Tạo cơ sở dữ liệu và tải lên tập tin goviettour.sql
3. Chỉnh sửa tên cơ sở dữ liệu trong file .env của hệ thống
4. Thực thi câu lệnh
   ```bash
   php artisan serve
   ```
5. Truy cập đường dẫn "127.0.0.1:8000" để sử dụng
### Hệ thống gợi ý tour cá nhân hóa
1. Di chuyển vào thư mục recommendation
  ```bash
  cd recommendation
  ```
2. Khởi chạy server Flask
  ```bash
  python app.py
  ```
Mặc định server sẽ chạy tại:
  ```bash
  http://127.0.0.1:5000
  ```
## Đóng góp
- Trần Văn Nam - 2115239
- La O Thị Thanh - 2115268
- Trương Tấn Diệm - 2111817
## Liên hệ
📧 Email: trannamvan0605@gmail.com

