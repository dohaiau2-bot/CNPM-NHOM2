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