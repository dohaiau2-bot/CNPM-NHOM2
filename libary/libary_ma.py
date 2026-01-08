from .extension import ma
from marshmallow import fields

class StudentSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    birth_date = fields.Date()
    gender = fields.Str()
    class_name = fields.Str()

class CatSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class AuthorSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class BorrowSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    book_id = fields.Int(required=True)
    student_id = fields.Int(required=True)
    borrow_date = fields.Date()
    return_date = fields.Date(allow_none=True)

class BookSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    page_count = fields.Int()
    author_id = fields.Int()
    category_id = fields.Int()


class WorkShiftSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    staff_name = fields.Str(required=True)
    shift_type = fields.Str()
    work_date = fields.Date() # Định dạng chuẩn là YYYY-MM-DD