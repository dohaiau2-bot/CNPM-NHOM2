"""
models/database.py
Quản lý kết nối database
"""
import mysql.connector
from mysql.connector import Error
from config import Config


class Database:
    """
    Class quản lý kết nối MySQL database
    Sử dụng Singleton pattern để đảm bảo chỉ có 1 connection pool
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern - chỉ tạo 1 instance duy nhất"""
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def get_connection(self):
        """
        Tạo và trả về connection đến MySQL database
        
        Returns:
            mysql.connector.connection: Database connection
            
        Raises:
            Exception: Nếu không thể kết nối database
        """
        try:
            connection = mysql.connector.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                autocommit=False
            )
            return connection
        except Error as e:
            raise Exception(f"Lỗi kết nối database: {str(e)}")
    
    def execute_query(self, query, params=None, fetch_one=False):
        """
        Thực thi SELECT query và trả về kết quả
        
        Args:
            query (str): SQL query
            params (tuple): Tham số cho query
            fetch_one (bool): True nếu chỉ lấy 1 bản ghi, False lấy tất cả
            
        Returns:
            dict hoặc list: Kết quả query
            
        Raises:
            Exception: Nếu có lỗi khi thực thi query
        """
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch_one:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
            
            return result
            
        except Error as e:
            raise Exception(f"Lỗi thực thi query: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def execute_update(self, query, params=None):
        """
        Thực thi INSERT/UPDATE/DELETE query
        
        Args:
            query (str): SQL query
            params (tuple): Tham số cho query
            
        Returns:
            int: Số dòng bị ảnh hưởng
            
        Raises:
            Exception: Nếu có lỗi khi thực thi query
        """
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            connection.commit()
            
            return cursor.rowcount
            
        except Error as e:
            if connection:
                connection.rollback()
            raise Exception(f"Lỗi thực thi update: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()