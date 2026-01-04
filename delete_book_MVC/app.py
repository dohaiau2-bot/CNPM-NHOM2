"""
app.py
File chính khởi chạy ứng dụng Flask theo mô hình MVC
Chức năng: Hiển thị danh sách sách và XÓA sách
"""
from flask import Flask
from config import Config
from controllers.book_controller import BookController

# ==================== KHỞI TẠO FLASK APP ====================

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Khởi tạo controller
book_controller = BookController()


# ==================== ROUTES - HIỂN THỊ TRANG ====================

@app.route('/')
@app.route('/books')
def books_index():
    """
    Route hiển thị trang danh sách sách
    URL: http://localhost:5000/ hoặc http://localhost:5000/books
    """
    return book_controller.index()


# ==================== API ROUTES - XEM CHI TIẾT ====================

@app.route('/api/books/<int:book_id>')
def api_book_detail(book_id):
    """
    API endpoint xem chi tiết sách
    URL: http://localhost:5000/api/books/<id>
    Method: GET
    Return: JSON
    """
    return book_controller.view_detail(book_id)


# ==================== ROUTES - XÓA SÁCH ====================

@app.route('/books/<int:book_id>/delete', methods=['POST'])
def books_delete_ajax(book_id):
    """
    Route xóa sách qua AJAX
    URL: http://localhost:5000/books/<id>/delete
    Method: POST
    Return: JSON
    """
    return book_controller.delete_ajax(book_id)


@app.route('/books/<int:book_id>/delete-form', methods=['POST'])
def books_delete_form(book_id):
    """
    Route xóa sách qua form submission (không dùng AJAX)
    URL: http://localhost:5000/books/<id>/delete-form
    Method: POST
    Return: Redirect
    """
    return book_controller.delete_form(book_id)


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(error):
    """Xử lý lỗi 404 - Trang không tồn tại"""
    return "Trang không tồn tại", 404


@app.errorhandler(500)
def internal_server_error(error):
    """Xử lý lỗi 500 - Lỗi server"""
    return "Lỗi server nội bộ", 500


# ==================== CHẠY ỨNG DỤNG ====================

if __name__ == '__main__':
    print("=" * 60)
    print(" Khởi động ứng dụng Quản lý Thư viện")
    print("=" * 60)
    print(" Chức năng: Hiển thị danh sách sách và XÓA sách")
    print(" URL: http://localhost:5000")
    print("=" * 60)
    
    app.run(
        debug=Config.DEBUG,
        host='0.0.0.0',
        port=5000
    )