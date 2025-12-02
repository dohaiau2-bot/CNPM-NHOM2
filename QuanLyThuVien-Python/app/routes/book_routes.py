from flask import Blueprint, render_template, request

# Tạo Blueprint cho chức năng quản lý sách
book_bp = Blueprint('book_bp', __name__)

@book_bp.route("/list")
def list_books():
    return "Book List Page"

@book_bp.route("/delete/<int:book_id>")
def delete_book(book_id):
    return f"Delete book: {book_id}"
