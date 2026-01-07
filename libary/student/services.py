import logging
from datetime import datetime

# Cấu hình logging để nhìn cho chuyên nghiệp
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StudentService:
    def __init__(self):
        # Giả lập kết nối database hoặc khởi tạo context
        self.context = "DatabaseConnectionString"
        logger.info("StudentService initialized successfully.")

    def _validate_connection(self):
        """Kiểm tra kết nối trước khi thực hiện giao dịch"""
        if not self.context:
            logger.error("Database context is missing.")
            return False
        return True
def get_student_by_id(self, student_id):
        try:
            if not self._validate_connection():
                raise ConnectionError("Database connection failed")
            
            logger.info(f"Attempting to retrieve student with ID: {student_id}")
            
            # Giả lập logic lấy dữ liệu (Code thật sẽ là truy vấn SQL)
            # TODO: Implement actual database query here
            if student_id <= 0:
                raise ValueError("Invalid student ID")
                
            return {"id": student_id, "status": "Active"}

        except ValueError as ve:
            logger.warning(f"Validation error: {str(ve)}")
            return None
        except Exception as e:
            logger.critical(f"System error in get_student_by_id: {str(e)}")
            raise e
def validate_student_data(self, data):
        """Kiểm tra tính hợp lệ của dữ liệu sinh viên đầu vào"""
        errors = []
        
        if not data:
            errors.append("Payload is empty")
            return False, errors

        if 'email' not in data or '@' not in data['email']:
            errors.append("Invalid email format")
            
        if 'age' in data and (data['age'] < 18 or data['age'] > 100):
            errors.append("Age must be between 18 and 100")
            
        if errors:
            logger.error(f"Data validation failed: {errors}")
            return False, errors
            
        return True, []