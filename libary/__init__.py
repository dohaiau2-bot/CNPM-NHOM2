from flask import Flask, request, Blueprint
from flask_cors import CORS
import os

# Import các extension
from .extension import db, ma

# Import các Model (cần thiết để create_all nhận diện được bảng)
from .model import Students, Books, Author, Category, Borrows, WorkShift

# Import các Controller
from .books.controller import books
from .borrow.controller import borrow
from .category_author.controller import author_cat

# LƯU Ý: Kiểm tra file shift/controller.py. 
# Nếu bên đó bạn viết "shifts = Blueprint..." thì sửa dòng dưới thành "import shifts"
from .shift.controller import shift 
# Hoặc: from .shift.controller import shifts as shift

def create_db(app):
    # Đã bỏ qua kiểm tra file tồn tại để luôn cập nhật bảng mới
    with app.app_context():
        db.create_all()
        print(">> DB checked and updated! (Tables created if missing)")

def libary_app(config_file="config.py"):
    app = Flask(__name__)
    CORS(app)
    app.config.from_pyfile(config_file)
    
    # Cấu hình đường dẫn DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///libary.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Khởi tạo DB và Marshmallow
    db.init_app(app)
    ma.init_app(app)

    # --- BƯỚC QUAN TRỌNG: GỌI HÀM TẠO DB ---
    # Phải gọi ở đây thì bảng WorkShift mới được tạo
    create_db(app) 
    # ---------------------------------------

    # Đăng ký các blueprint
    app.register_blueprint(books)
    app.register_blueprint(borrow)
    app.register_blueprint(author_cat)
    app.register_blueprint(shift) # Đăng ký blueprint Ca trực
    
    return app