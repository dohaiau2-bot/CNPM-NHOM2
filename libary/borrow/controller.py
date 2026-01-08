from flask import Blueprint
from .services import get_borrow_author_cat_service
borrow = Blueprint("borrow", __name__)


@borrow.route("/borrow-management/borrow/<string:student_name>", methods=['GET'])
def get_borrow_author_cat(student_name):
    return get_borrow_author_cat_service(student_name)
from flask import Blueprint, request
from libary.borrow.services import borrow_book_service

borrow = Blueprint("borrow", __name__)

@borrow.route("/borrow", methods=["POST"])
def borrow_book():
    data = request.get_json()

    book_id = data.get("book_id")
    student_id = data.get("student_id")

    if not book_id or not student_id:
        return {"message": "book_id and student_id are required"}, 400

    return borrow_book_service(book_id, student_id)
