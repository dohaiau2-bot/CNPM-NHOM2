from flask import Blueprint, render_template
from .services import (add_book_service,get_book_by_id_service,get_all_books_service,
                        update_book_by_id_service,delete_book_by_id_service,
                        get_book_by_author_service, search_books_service)
books=Blueprint("books",__name__)


@books.route("/book-management/book",methods=['POST'])
def add_book():
    return add_book_service()

#get book by id
@books.route("/book-management/book/id/<int:id>",methods=['GET'])
def get_book_by_id(id):
    return get_book_by_id_service(id)
#get all books
@books.route("/book-management/books",methods=['GET'])
def get_all_books():
    return get_all_books_service()
#update book
@books.route("/book-management/book/<int:id>",methods=['PUT'])
def update_book_by_id(id):
    return update_book_by_id_service(id)
#delete books
@books.route("/book-management/book/<int:id>",methods=['DELETE'])
def delete_book_by_id(id):
    return delete_book_by_id_service(id)
#get book by author
@books.route("/book-management/book/author/<string:author>",methods=['GET'])
def get_book_by_author(author):
    return get_book_by_author_service(author)

@books.route("/delete-books-page", methods=['GET'])
def delete_book_page():
    return render_template('delete.html')

@books.route("/book-management/books/search-api", methods=['GET'])
def search_books_api():
    return search_books_service()

# Route hiển thị trang quản lý sách (render ra file HTML)
@books.route('/books') 
def books_management():
    return render_template('books.html')