from libary.extension import db
from libary.libary_ma import BookSchema
from libary.model import Author, Books, Borrows, Category, Students
from flask import request, jsonify
from sqlalchemy.sql import func
from datetime import date
import json


def get_borrow_author_cat_service(student_name):
    borrows = db.session.query(Borrows.id, Books.name, Category.name, Author.name).join(Students, Borrows.student_id == Students.id).join(Books, Borrows.book_id == Books.id).join(
        Category, Books.category_id == Category.id).join(Author, Books.author_id == Author.id).filter(func.lower(Students.name) == student_name.lower()).all()
    if borrows:
        return jsonify({f"{student_name} borrowed": borrows}), 200
    else:
        return jsonify({"message": "Not found borrow!"}), 404

def borrow_book_service(book_id, student_id):
    # 1. Kiểm tra sách tồn tại
    book = Books.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    # 2. Kiểm tra sinh viên tồn tại
    student = Students.query.get(student_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    # 3. Kiểm tra trạng thái sách (đang được mượn chưa)
    borrowed = Borrows.query.filter(
        Borrows.book_id == book_id,
        Borrows.return_date == None
    ).first()

    if borrowed:
        return jsonify({"message": "Book is currently borrowed"}), 400

    # 4. Tạo bản ghi mượn
    new_borrow = Borrows(
        book_id=book_id,
        student_id=student_id,
        borrow_date=date.today(),
        return_date=None
    )

    db.session.add(new_borrow)
    db.session.commit()

    return jsonify({
        "message": "Borrow book successfully",
        "data": {
            "borrow_id": new_borrow.id,
            "book_id": book_id,
            "student_id": student_id,
            "borrow_date": new_borrow.borrow_date.isoformat()
        }
    }), 201
