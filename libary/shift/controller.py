from flask import Blueprint, request, jsonify
from ..extension import db
from ..model import WorkShift
from ..libary_ma import WorkShiftSchema
from datetime import datetime
from flask import render_template

# Tạo Blueprint với đường dẫn riêng
# Mọi API trong này sẽ bắt đầu bằng /api/shifts
shift = Blueprint('shifts', __name__, url_prefix='/api/shifts')

shift_schema = WorkShiftSchema()
shifts_schema = WorkShiftSchema(many=True)

# 1. Lấy danh sách ca trực
@shift.route('/', methods=['GET'])
def get_shifts():
    all_shifts = WorkShift.query.all()
    return shifts_schema.jsonify(all_shifts)

# 2. Thêm ca trực mới
@shift.route('/', methods=['POST'])
def add_shift():
    staff_name = request.json['staff_name']
    shift_type = request.json['shift_type']
    
    # Xử lý ngày tháng từ chuỗi gửi lên (VD: "2023-12-20")
    date_str = request.json['work_date']
    work_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    new_shift = WorkShift(staff_name, shift_type, work_date)

    db.session.add(new_shift)
    db.session.commit()

    return shift_schema.jsonify(new_shift)

# 3. Xóa ca trực
@shift.route('/<id>', methods=['DELETE'])
def delete_shift(id):
    shift = WorkShift.query.get(id)
    if not shift:
        return jsonify({"message": "Shift not found"}), 404
        
    db.session.delete(shift)
    db.session.commit()
    return jsonify({"message": "Shift deleted successfully"})

@shift.route('/view', methods=['GET']) # Đường dẫn sẽ là /api/shifts/view
def view_shifts_page():
    return render_template('shifts.html')