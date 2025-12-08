import mysql.connector
from config import Config

def delete_book(book_id):
    """
    Xóa sách khỏi hệ thống
    
    Parameters:
        book_id (int): ID của sách cần xóa
    
    Returns:
        dict: {'success': bool, 'message': str}
    """
    try:
        # Kết nối database
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
        )
        cursor = conn.cursor(dictionary=True)
        
        # Kiểm tra sách tồn tại
        cursor.execute("SELECT code, title FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()
        if not book:
            return {'success': False, 'message': 'Không tìm thấy sách'}
        
        # Kiểm tra đang được mượn
        cursor.execute("""
            SELECT COUNT(*) as count FROM borrow_items 
            WHERE book_id = %s AND status = 'borrowed'
        """, (book_id,))
        if cursor.fetchone()['count'] > 0:
            return {'success': False, 'message': 'Sách đang được mượn, không thể xóa'}
        
        # Xóa sách (CASCADE sẽ tự động xóa book_authors, copies)
        cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
        conn.commit()
        
        return {'success': True, 'message': f"Đã xóa: {book['code']} - {book['title']}"}
        
    except Exception as e:
        return {'success': False, 'message': f'Lỗi: {str(e)}'}
    finally:
        if conn:
            cursor.close()
            conn.close()


# Sử dụng
if __name__ == "__main__":
    result = delete_book(3)
    print(result['message'])