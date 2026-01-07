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