from sqlalchemy.sql.expression import except_
from libary.extension import db
from libary.libary_ma import StudentSchema, AuthorSchema, CatSchema, BookSchema
from libary.model import Students, Category, Author, Books
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

# Init schemas
author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
cat_schema = CatSchema()
cats_schema = CatSchema(many=True)
book_schema = BookSchema()
books_schema = BookSchema(many=True)

def get_author_by_id_serv(id):
    author = Author.query.get(id)
    if author:
        return author_schema.jsonify(author)
    return jsonify({"message": "Author not found"}), 404   
def update_author_serv(id):
    author = Author.query.get(id)
    if author:
        try:
            name = request.json['name']
            author.name = name
            db.session.commit()
            return author_schema.jsonify(author)
        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "Update failed"}), 400
    return jsonify({"message": "Author not found"}), 404

def get_all_books_serv():
    books = Books.query.all()
    return books_schema.jsonify(books)