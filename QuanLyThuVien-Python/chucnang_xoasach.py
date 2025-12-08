# hôm nay anh sẽ code và hướng dẫn em chức năng xóa sách
# bởi vì các bạn của em chưa làm xong chức năng hiển thị sách và thêm sách nên demo chức năng sẽ không có giao diện để thực hiện nên anh chỉ trình bày trên code thôi.
# chúng ta sẽ bắt đầu nhé .

import mysql.connector # đầu tiên impoort thư viện để kết nối mysql
from config import Config # chúng ta sẽ imporrt thêm phần cấu hình từ file config.py mà hôm bữa anh đã giải thích

# vì em và các bạn không thực hiện mô hình MVC nên cta sẽ làm theo phương pháp dùng hàm nhé
# nội dung hôm nay chỉ là chức năng xóa sách nên cta chỉ có 1 hàm là xóa sách

def delete_book(book_id) # đây là hàm nhận book_id từ database có kiểu dữ liệu là int .
    try:
        conn =mysql.connector.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
            
        )
        cursor = conn.cursor(dictionary=True) # tạo cursor và trả kết quả về dạng dict 
        # đây là phần kết nối với database bằng thông tin từ config nhé
        cursor.execute("SELECT code, title FROM books WHERE id = %s",(book_id))
        book = cursor.fetchone()
        if not book:
            return{'success': False,'message':'Không tìm thấy sách'}
        # phần này sẽ sellect vào bảng sách để kiểm xem sách có tồn tại hay không
        # trả về susscess nếu tìm thấy và không tìm thấy sách nếu không tim thấy vaf thoát
        #Tiếp theo chúng ta sẽ kiểm tra xem sách có đang được  mượn hay không, nếu sách đang mượn thì không thể xóa
        cursor.execute("""
                       SELECT COUNT(*) as count FROM borrow_items
                       WHERE book_id = %s AND status = 'borrowed
                       """, (book_id,))
        if cursor.fetchone()['count']>0:
            return{'success': False,'message':'Sach dang duoc muon,khong the xoa'}
         # Tiếp theo sẽ dến bước xóa sách, xóa cả book_author và copie theo CASCADE
        cursor.execute("DELETE FROM books WHERE id = %s ", (book_id,))
        conn.commit()
        return{'success': True,'message':f"Đã xóa : {book['code']} -{book['title']} "}
    except Exception as e:
        return{'success':False,'message':f'Lỗi:{str(e)}'}
    # bắt ngoại lệ trả về thông báo lỗi nếu xảy ra bất kỳ lỗi nào để tránh crash chương trình
    finally:
        if conn:
            cursor.close(
                conn.close()
                # đóng cursor và đóng kết nối
            )
            
            