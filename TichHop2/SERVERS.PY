from libary.extension import db
from libary.libary_ma import BookSchema
from libary.model import Books,Author,Category
from flask import request, jsonify
from sqlalchemy.sql import func
import json

book_schema=BookSchema()
books_schema=BookSchema(many=True)

def add_book_service():
    data=request.json
    if (data and ('name' in data) and ('page_count'in data)
        and('author_id' in data) and ('category_id' in data)):
        name = data['name']
        page_count= data['page_count']
        author_id=data['author_id']
        category_id=data['category_id']
        try:
            new_book =Books(name=name,page_count=page_count,author_id=author_id,category_id=category_id)
            db.session.add(new_book)
            db.session.commit()
            return "Add success"
        except Exception as e:
            db.session.rollback()
            return "can not add book"
    else:
        return "Request error"
def get_book_by_id_service(id):
    book= Books.query.get(id)
    print(book.name)
    if book:
        return book_schema.jsonify(book)
    else:
        return "Not found book"
    
def get_all_books_service():
    books= Books.query.all()
    if books:
        return books_schema.jsonify(books)
    else:
        return "Not found book"
    
def update_book_by_id_service(id):
    book = Books.query.get(id)
    data = request.json
    if book:
        try:
            # Kiểm tra và cập nhật từng trường nếu có dữ liệu gửi lên
            if 'name' in data:
                book.name = data['name']
            if 'page_count' in data:
                book.page_count = data['page_count']
            if 'author_id' in data:
                book.author_id = data['author_id']
            if 'category_id' in data:
                book.category_id = data['category_id']
            
            db.session.commit()
            return jsonify({"message": "Book updated successfully!", "id": id})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Cannot update book: {str(e)}"}), 500
    else:
        return jsonify({"error": "Book not found"}), 404

def delete_book_by_id_service(id):
    book= Books.query.get(id)
    if book:
        try:
            db.session.delete(book)
            db.session.commit()
            return "Book deleted!"
        except Exception as e:
            db.session.rollback()
            return "Can not delete book!"
    else:
        return "Not found book"
    
def get_book_by_author_service(author):
    books=Books.query.join(Author).filter(
        func.lower(Author.name)==author.lower()).all()
    if books:
        return books_schema.jsonify(books)
    else:
        return ("Author not found !")
