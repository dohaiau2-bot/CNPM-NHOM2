"""
models/book_model.py
Model xử lý database cho sách - Đã tối ưu logic xóa
"""
import mysql.connector
from config import Config


class BookModel:
    """Model xử lý các thao tác database cho sách"""
    
    def get_db_connection(self):
        """Tạo kết nối database"""
        try:
            conn = mysql.connector.connect(
                host=Config.DB_HOST,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                port=Config.DB_PORT
            )
            return conn
        except Exception as e:
            print(f"Lỗi kết nối database: {str(e)}")
            return None
    
    def get_all_books(self):
        """Lấy danh sách tất cả sách"""
        conn = None
        try:
            conn = self.get_db_connection()
            if not conn:
                return []
            
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    b.id, 
                    b.code, 
                    b.title, 
                    p.name as publisher,
                    b.publication_year,
                    c.name as category,
                    b.total_copies,
                    b.available_copies,
                    GROUP_CONCAT(DISTINCT a.full_name SEPARATOR ', ') as authors
                FROM books b
                LEFT JOIN publishers p ON b.publisher_id = p.id
                LEFT JOIN categories c ON b.category_id = c.id
                LEFT JOIN book_authors ba ON b.id = ba.book_id
                LEFT JOIN authors a ON ba.author_id = a.id
                GROUP BY b.id, b.code, b.title, p.name, b.publication_year, 
                         c.name, b.total_copies, b.available_copies
                ORDER BY b.id DESC
            """)
            books = cursor.fetchall()
            return books
            
        except Exception as e:
            print(f"Lỗi lấy danh sách sách: {str(e)}")
            return []
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def get_book_by_id(self, book_id):
        """Lấy thông tin chi tiết một cuốn sách"""
        conn = None
        try:
            conn = self.get_db_connection()
            if not conn:
                return None
            
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    b.*,
                    p.name as publisher_name,
                    c.name as category_name,
                    GROUP_CONCAT(DISTINCT a.full_name SEPARATOR ', ') as authors
                FROM books b
                LEFT JOIN publishers p ON b.publisher_id = p.id
                LEFT JOIN categories c ON b.category_id = c.id
                LEFT JOIN book_authors ba ON b.id = ba.book_id
                LEFT JOIN authors a ON ba.author_id = a.id
                WHERE b.id = %s
                GROUP BY b.id
            """, (book_id,))
            
            return cursor.fetchone()
            
        except Exception as e:
            print(f"Lỗi lấy thông tin sách: {str(e)}")
            return None
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def get_book_copies(self, book_id):
        """Lấy danh sách bản sao của sách"""
        conn = None
        try:
            conn = self.get_db_connection()
            if not conn:
                return []
            
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, barcode, status, acquisition_date, location, note
                FROM copies
                WHERE book_id = %s
                ORDER BY id
            """, (book_id,))
            
            return cursor.fetchall()
            
        except Exception as e:
            print(f"Lỗi lấy danh sách bản sao: {str(e)}")
            return []
        finally:
            if conn:
                cursor.close()
                conn.close()
    
    def delete_book(self, book_id):
        """
        Xóa sách với logging chi tiết
        
        Args:
            book_id (int): ID của sách cần xóa
            
        Returns:
            dict: {'success': bool, 'message': str}
        """
        conn = None
        cursor = None
        
        try:
            print(f"\n🔍 BẮT ĐẦU XÓA SÁCH - ID: {book_id}")
            print("="*60)
            
            # BƯỚC 1: Kết nối database
            print("📡 Đang kết nối database...")
            conn = self.get_db_connection()
            if not conn:
                print("❌ Không thể kết nối database")
                return {
                    'success': False, 
                    'message': 'Không thể kết nối database'
                }
            print("✅ Kết nối database thành công")
            
            cursor = conn.cursor(dictionary=True)
            
            # BƯỚC 2: Kiểm tra sách tồn tại
            print(f"\n📚 Kiểm tra sách ID {book_id}...")
            cursor.execute(
                "SELECT id, code, title FROM books WHERE id = %s", 
                (book_id,)
            )
            book = cursor.fetchone()
            
            if not book:
                print("❌ Không tìm thấy sách")
                return {
                    'success': False, 
                    'message': 'Không tìm thấy sách cần xóa'
                }
            
            print(f"✅ Tìm thấy sách: [{book['code']}] {book['title']}")
            
            # BƯỚC 3: Kiểm tra bản sao đang mượn
            print("\n📋 Kiểm tra bản sao đang mượn...")
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM borrow_items bi
                INNER JOIN copies c ON bi.copy_id = c.id
                WHERE c.book_id = %s AND bi.status = 'borrowed'
            """, (book_id,))
            
            result = cursor.fetchone()
            borrowed_count = result['count'] if result else 0
            print(f"📊 Số bản sao đang mượn: {borrowed_count}")
            
            if borrowed_count > 0:
                print(f"❌ Không thể xóa - có {borrowed_count} bản sao đang mượn")
                return {
                    'success': False, 
                    'message': f'Sách đang có {borrowed_count} bản sao được mượn, không thể xóa'
                }
            
            print("✅ Không có bản sao đang mượn")
            
            # BƯỚC 4: Kiểm tra số lượng copies
            print("\n📦 Kiểm tra tổng số bản sao...")
            cursor.execute("""
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN status = 'available' THEN 1 ELSE 0 END) as available,
                       SUM(CASE WHEN status = 'borrowed' THEN 1 ELSE 0 END) as borrowed,
                       SUM(CASE WHEN status = 'lost' THEN 1 ELSE 0 END) as lost,
                       SUM(CASE WHEN status = 'damaged' THEN 1 ELSE 0 END) as damaged
                FROM copies
                WHERE book_id = %s
            """, (book_id,))
            
            copies_info = cursor.fetchone()
            print(f"📊 Thống kê bản sao:")
            print(f"   - Tổng: {copies_info['total']}")
            print(f"   - Có sẵn: {copies_info['available']}")
            print(f"   - Đang mượn: {copies_info['borrowed']}")
            print(f"   - Mất: {copies_info['lost']}")
            print(f"   - Hỏng: {copies_info['damaged']}")
            
            # BƯỚC 5: Xóa book_authors trước (nếu không có CASCADE)
            print("\n🔗 Xóa liên kết tác giả...")
            cursor.execute("DELETE FROM book_authors WHERE book_id = %s", (book_id,))
            deleted_authors = cursor.rowcount
            print(f"✅ Đã xóa {deleted_authors} liên kết tác giả")
            
            # BƯỚC 6: Xóa copies
            print("\n📦 Xóa bản sao...")
            cursor.execute("DELETE FROM copies WHERE book_id = %s", (book_id,))
            deleted_copies = cursor.rowcount
            print(f"✅ Đã xóa {deleted_copies} bản sao")
            
            # BƯỚC 7: Xóa sách
            print("\n📚 Xóa sách...")
            cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
            deleted_books = cursor.rowcount
            
            if deleted_books == 0:
                print("❌ Không thể xóa sách từ bảng books")
                conn.rollback()
                return {
                    'success': False, 
                    'message': 'Không thể xóa sách'
                }
            
            print(f"✅ Đã xóa sách khỏi database")
            
            # BƯỚC 8: Commit transaction
            print("\n💾 Lưu thay đổi vào database...")
            conn.commit()
            print("✅ Commit thành công!")
            
            print("="*60)
            print(f"🎉 HOÀN TẤT XÓA SÁCH: [{book['code']}] {book['title']}\n")
            
            return {
                'success': True, 
                'message': f'Đã xóa thành công: {book["code"]} - {book["title"]}'
            }
            
        except mysql.connector.Error as err:
            print(f"\n❌ LỖI MYSQL: {err}")
            print(f"   Error Code: {err.errno}")
            print(f"   SQL State: {err.sqlstate if hasattr(err, 'sqlstate') else 'N/A'}")
            
            if conn:
                conn.rollback()
                print("↩️  Đã rollback transaction")
            
            error_code = err.errno
            if error_code == 1451:  # Foreign key constraint
                return {
                    'success': False, 
                    'message': 'Không thể xóa sách do có ràng buộc dữ liệu liên quan'
                }
            elif error_code == 1452:  # Cannot add or update a child row
                return {
                    'success': False, 
                    'message': 'Lỗi ràng buộc khóa ngoại'
                }
            else:
                return {
                    'success': False, 
                    'message': f'Lỗi database: {str(err)}'
                }
                
        except Exception as e:
            print(f"\n❌ LỖI HỆ THỐNG: {str(e)}")
            print(f"   Type: {type(e).__name__}")
            
            if conn:
                conn.rollback()
                print("↩️  Đã rollback transaction")
            
            return {
                'success': False, 
                'message': f'Lỗi hệ thống: {str(e)}'
            }
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                print("🔌 Đã đóng kết nối database\n")