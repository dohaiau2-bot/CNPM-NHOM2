// FILE: script.js

function loadBooks() {
    console.log("Đang tải dữ liệu...");

    // --- PHẦN NÀY THAY THẾ CHO FETCH API ---
    // Vì không có server, ta giả lập dữ liệu (Mock Data)
    // Cấu trúc giống hệt cái JSON mà Python server cũ trả về
    const data = [
        { id: 1, name: "Nhà Giả Kim", author: "Paulo Coelho" },
        { id: 2, name: "Đắc Nhân Tâm", author: "Dale Carnegie" },
        { id: 3, name: "Tuổi Trẻ Đáng Giá Bao Nhiêu", author: "Rosie Nguyễn" },
        { id: 10, name: "Harry Potter", author: "J.K. Rowling" }
    ];

    // --- PHẦN XỬ LÝ HIỂN THỊ (Logic cũ của bạn giữ nguyên) ---
    // Giả lập độ trễ 0.5s để giống mạng thật (không bắt buộc)
    setTimeout(() => {
        let html = "";
        
        // Vòng lặp duyệt qua từng quyển sách
        data.forEach(book => {
            // Dấu huyền (backtick) giúp viết HTML trong JS dễ dàng
            html += `
                <tr>
                    <td>${book.id}</td>
                    <td>${book.name}</td>
                    <td>${book.author}</td>
                </tr>
            `;
        });

        // Đưa đoạn HTML vừa tạo vào trong thẻ tbody bên file HTML
        document.getElementById("book-table").innerHTML = html;
        
        console.log("Đã tải xong!");
    }, 500); 
}