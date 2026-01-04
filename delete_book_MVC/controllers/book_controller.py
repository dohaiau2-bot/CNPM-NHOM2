"""
controllers/book_controller.py
Controller xử lý logic nghiệp vụ cho sách - Đã sửa lỗi xóa
"""
from flask import render_template, jsonify, flash, redirect, url_for
from models.book_model import BookModel


class BookController:
    """
    Controller quản lý các chức năng liên quan đến sách
    Xử lý logic nghiệp vụ giữa Model và View
    """
    
    def __init__(self):
        """Khởi tạo controller với model instance"""
        self.model = BookModel()
    
    def index(self):
        """
        Hiển thị trang danh sách sách
        
        Returns:
            str: HTML template đã được render với danh sách sách
        """
        try:
            # Lấy danh sách sách từ model
            books = self.model.get_all_books()
            
            # Render template với dữ liệu
            return render_template('books/index.html', books=books)
            
        except Exception as e:
            # Xử lý lỗi và hiển thị thông báo
            flash(f'Lỗi tải dữ liệu: {str(e)}', 'danger')
            return render_template('books/index.html', books=[])
    
    def view_detail(self, book_id):
        """
        Xem chi tiết sách (API endpoint trả về JSON)
        
        Args:
            book_id (int): ID của sách cần xem
            
        Returns:
            tuple: (JSON response, HTTP status code)
        """
        try:
            # Lấy thông tin sách
            book = self.model.get_book_by_id(book_id)
            
            if not book:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy sách'
                }), 404
            
            # Lấy danh sách bản sao
            copies = self.model.get_book_copies(book_id)
            book['copies'] = copies
            
            # Trả về JSON thành công
            return jsonify({
                'success': True,
                'book': book
            }), 200
            
        except Exception as e:
            # Trả về lỗi dạng JSON
            return jsonify({
                'success': False,
                'message': f'Lỗi hệ thống: {str(e)}'
            }), 500
    
    def delete_ajax(self, book_id):
        """
        Xóa sách qua AJAX request (trả về JSON)
        
        Args:
            book_id (int): ID của sách cần xóa
            
        Returns:
            tuple: (JSON response, HTTP status code)
        """
        from flask import jsonify
        
        try:
            print(f"\n{'='*60}")
            print(f"🌐 AJAX REQUEST - XÓA SÁCH ID: {book_id}")
            print(f"{'='*60}")
            
            # Gọi model để xóa sách
            result = self.model.delete_book(book_id)
            
            print(f"\n📤 KẾT QUẢ TRẢ VỀ:")
            print(f"   Type: {type(result)}")
            print(f"   Data: {result}")
            
            # Xử lý kết quả
            if isinstance(result, dict):
                success = result.get('success', False)
                message = result.get('message', 'Không có thông báo')
            else:
                # Nếu model trả về tuple (success, message)
                success, message = result
            
            print(f"   Success: {success}")
            print(f"   Message: {message}")
            
            # Trả về kết quả với status code phù hợp
            if success:
                print("✅ Trả về status 200 (Success)")
                return jsonify({
                    'success': True,
                    'message': message
                }), 200
            else:
                print("⚠️  Trả về status 400 (Bad Request)")
                print(f"❌ LÝ DO: {message}")
                return jsonify({
                    'success': False,
                    'message': message
                }), 400
                
        except Exception as e:
            print(f"\n❌ EXCEPTION TRONG CONTROLLER:")
            print(f"   Type: {type(e).__name__}")
            print(f"   Message: {str(e)}")
            
            # Xử lý lỗi hệ thống
            return jsonify({
                'success': False,
                'message': f'Lỗi hệ thống: {str(e)}'
            }), 500
    
    def delete_form(self, book_id):
        """
        Xóa sách qua form submission (redirect về trang danh sách)
        
        Args:
            book_id (int): ID của sách cần xóa
            
        Returns:
            Response: Redirect về trang danh sách với flash message
        """
        try:
            # Gọi model để xóa sách
            result = self.model.delete_book(book_id)
            
            # Xử lý kết quả từ model
            if isinstance(result, dict):
                success = result.get('success', False)
                message = result.get('message', 'Không có thông báo')
            else:
                success, message = result
            
            # Hiển thị thông báo
            if success:
                flash(message, 'success')
            else:
                flash(message, 'danger')
                
        except Exception as e:
            # Hiển thị lỗi
            flash(f'Lỗi hệ thống: {str(e)}', 'danger')
        
        # Redirect về trang danh sách
        return redirect(url_for('books_index'))