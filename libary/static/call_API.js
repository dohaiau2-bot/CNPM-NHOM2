getBookApi = "http://127.0.0.1:5000/book-management/books"
addBookApi = "http://127.0.0.1:5000/book-management/book"
getAuthorApi = "http://127.0.0.1:5000/author-management/authors"
getCategoryApi = "http://127.0.0.1:5000/category-management/categories"
function start(){
    loadBook();
    handleCreateForm();
    loadAuthor();
    loadCategory();
}

function loadBook(){
    titleTable = 
    " <tr> <th> Id </th> <th> Name </th> <th> Page Count </th> </tr> "
    fetch(getBookApi)
        .then(function(response){
            return response.json();
        })
        .then(function(books){
            var htmls = books.map(function(book){
                return `<tr>
                <td>${book.id}</td>
                <td>${book.name}</td>
                <td>${book.page_count}</td>
                </tr>
                `
            })
            var html = titleTable + htmls.join('')
            document.getElementById("book-block").innerHTML = html
        })
        .catch(function(error){
            return error;
        })
    }
function loadAuthor(){
    fetch(getAuthorApi)
        .then(function(response){
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(function(authors){
            var htmls = authors.map(function(author){
                return `<option value="${author.id}">${author.name}</option>`;
            });
            // Nối chuỗi html đúng cách
            var html = '<option value="">-- Select Author --</option>' + htmls.join('');
            document.getElementById("author").innerHTML = html;
        })
        .catch(function(error){
            console.error('Error loading authors:', error);
        });
}

function loadCategory(){
    fetch(getCategoryApi)
        .then(function(response){
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(function(cats){
            var htmls = cats.map(function(cat){
                return `<option value="${cat.id}">${cat.name}</option>`;
            });
            var html = '<option value="">-- Select Category --</option>' + htmls.join('');
            document.getElementById("category").innerHTML = html;
        })
        .catch(function(error){
            console.error('Error loading categories:', error);
        });
}


function handleCreateForm(){
    var form = document.querySelector('form')
    
    form.onsubmit = function(event){
        event.preventDefault()   // <-- Chặn reload trang
        var name = document.querySelector('input[name="name"]').value
        var pageCount = document.querySelector('input[name="page-count"]').value
        var authorId = document.querySelector('select[name="author"]').value
        var catId = document.querySelector('select[name="category"]').value

        if (name && pageCount && authorId && catId) {
            let data = {
                name: name,
                page_count: pageCount,
                author_id: parseInt(authorId),
                category_id: parseInt(catId)
            }
            console.log(data)
            createBook(data, loadBook)
        } else {
            alert("Invalid value")
        }
    }
}

function createBook(data, callback){
    var options = {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    }
    fetch(addBookApi, options)
        .then(function(response){
            return response.json()
        })
        .then(callback)
        .catch(function(error){
            console.log(error)
        })
}
start()