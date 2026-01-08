# Extra services for library module
# Shared services of CNPM-NHOM2
# NOTE:
# This service module is shared across multiple APIs.
# Changes should be reviewed carefully to avoid breaking dependencies.
from sqlalchemy.sql.expression import except_
from libary.extension import db
from libary.libary_ma import StudentSchema, AuthorSchema, CatSchema, BookSchema
from libary.model import Students, Category, Author, Books
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from datetime import timedelta, datetime


# ===== Schema initialization =====
author_schema = AuthorSchema()                  
# schema for single author
authors_schema = AuthorSchema(many=True)   
# schema for list of authors
cat_schema = CatSchema()                          
# schema for single category
cats_schema = CatSchema(many=True)               
# schema for list of categories
book_schema = BookSchema()                     
# schema for single book
books_schema = BookSchema(many=True)               # schema for list of books
# Student Schemas
student_schema = StudentSchema()                   # schema for single student
students_schema = StudentSchema(many=True)         # schema for list of students

# ===== Author services =====
# Get author information by id
def get_author_by_id_serv(id):
    author = Author.query.get(id)
    if author:
        return author_schema.jsonify(author)
    return jsonify({"message": "Author not found"}), 404   

# Update author information
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

# ===== Book services =====
# Get all books
def get_all_books_serv():
    books = Books.query.all()
    return books_schema.jsonify(books)

# NOTE:
# This function should be protected by admin authorization middleware.
# Delete book by id (admin only)
def quick_delete_book(id):
    # Admin only function
    book = Books.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return "Deleted"
    return "Not Found"

# ===== Utility / Statistics services =====
# Count authors and categories
def count_stats_serv():
    a_count = Author.query.count()
    c_count = Category.query.count()
    return jsonify({"authors": a_count, "categories": c_count})

# Validate input data
def validate_input_data(data):
    if not data:
        return False
    if 'name' not in data:
        return False
    return True

# Get current server timestamp
def get_current_timestamp_serv():
    now = datetime.now()
    return jsonify({"timestamp": now.isoformat()})

# ===== Student services =====
# Get all students
def get_all_students_serv():
    students = Students.query.all()
    return students_schema.jsonify(students)


# End of extra services module
if __name__ == "__main__":
    print("Services module loaded")
