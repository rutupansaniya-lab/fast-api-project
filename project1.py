from fastapi import FastAPI
from fastapi import Body 
app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/")
async def firstfunction():
    return {"message": "Hello World"}

@app.get("/books")
async def get_books(category: str = None, author: str = None):
    filtered_books = BOOKS
    if category:
        filtered_books = [book for book in filtered_books if book['category'].casefold() == category.casefold()]
    if author:
        filtered_books = [book for book in filtered_books if book['author'].casefold() == author.casefold()]
    return filtered_books

@app.get("/books/category/{category}")
async def get_books_by_category(category: str):
    return [book for book in BOOKS if book['category'].casefold() == category.casefold()]

@app.get("/books/author/{author}")
async def get_books_by_author(author: str):
    return [book for book in BOOKS if book['author'].casefold() == author.casefold()] 

@app.get("/books/find/")
async def get_books_by_category_and_author(category: str, author: str):
    return [book for book in BOOKS if book['category'].casefold() == category.casefold() and book['author'].casefold() == author.casefold()]    

@app.post("/books/add_book")
async def add_book(new_book=Body()):
    BOOKS.append(new_book)
    return {"message": "Book added successfully", "book": new_book}

@app.put("/books/update_book")
async def update_book(book_to_update=Body()):
    for book in BOOKS:
        for i in range (len(BOOKS)):
            if BOOKS[i]['title'].casefold() == book_to_update['title'].casefold():
                BOOKS[i] = book_to_update
                return {"message": "Book updated successfully", "book": book_to_update}
        return {"message": "Book not found"}
            
@app.delete("/books/delete_book")
async def delete_book(book_title: str):
    for i in range (len(BOOKS)):
        if BOOKS[i]['title'].casefold() == book_title.casefold():
            deleted_book = BOOKS.pop(i)
            return {"message": "Book deleted successfully", "book": deleted_book}
    return {"message": "Book not found"}