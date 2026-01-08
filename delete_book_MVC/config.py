"""
config.py
Cấu hình cho ứng dụng quản lý thư viện
"""

class Config:
    """Cấu hình database và Flask"""
    
    # Cấu hình MySQL Database
    DB_HOST = 'localhost'
    DB_PORT = 3306
    DB_NAME = 'library'
    DB_USER = 'root'
    DB_PASSWORD = ''  
    
    # Cấu hình Flask
    SECRET_KEY = '123'
    DEBUG = True