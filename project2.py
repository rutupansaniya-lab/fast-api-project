from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app=FastAPI()

class Books():
    def __init__(self, id: int, title: str, author: str, category: str, rating: float, published_year: int):
        self.id = id
        self.title = title
        self.author = author
        self.category = category
        self.rating = rating 
        self.published_year = published_year

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="optional", default=None)
    title: str = Field(min_lenght=3)
    author: str = Field(min_lenght=3)
    category: str = Field(min_lenght=3)
    rating: float = Field(ge=0,le=5)
    published_year: int = Field(ge=1930,le=2026)

    model_config={

        "json_schema_extra": {

            "example":{
                "title": "Book_title",
                "author": "Author_name",
                "category": "Category",
                "rating" : "rating"
            }
        }
    }

books=[
    Books(1, "Chankyaniti", "Chanakya", "Politics", 4.5,1948),
    Books(2, "Ramayan","Valmiki", "Religion", 5.0,1930),
    Books(3, "Mahabharat", "Vyasa", "Religion", 4.8,1978),
    Books(4, "Gita", "Krihsna", "Religion", 5.0,1967),
    Books(5, "Vidur Niti", "Vidhur", "Politics", 4.5,2021)
]

@app.get("/", status_code=status.HTTP_200_OK)
async def get_books():
    return books
 

@app.get("/find_books_year/{pubilshed_year}", status_code=status.HTTP_200_OK)
def get_book_by_year(pubilshed_year: int = Path(ge=1930,le=2026)):
    book_by_year=[]
    for book in books:
        if book.published_year==pubilshed_year:
            book_by_year.append(book)

    return book_by_year


@app.post("/add_book" , status_code=status.HTTP_201_CREATED)
async def add_book(book_request: BookRequest):
    new_book=Books(**book_request.model_dump())
    books.append(get_id(new_book))
    return "book added sucussefully"

def get_id(new_book: Books):
    if (len(books)>0):
        new_book.id=books[-1].id+1
    else:
        new_book.id=1

    return new_book

@app.get("/rating", status_code=status.HTTP_200_OK)
async def Get_book_by_rating(rating: float =  Query(ge=0,le=5)):
    books_to_return= []
    for book in books:
        if book.rating>= rating:
            books_to_return.append(book)
    return books_to_return


@app.get("/books", status_code=status.HTTP_200_OK)
#get books by author or category or both it can be none as well if both parameter are none then all books
async def Get_book_by_author_category(author:Optional[str] = Query(None, min_length=3, description="Author's name"), category: Optional[str] = Query(None, min_length=3, description="Book category")):
    filtered_list=books
    if author:
        filtered_list=[book for book in filtered_list if book.author.casefold()==author.casefold()]
    if category:
        filtered_list=[book for book in filtered_list if book.category.casefold()==category.casefold()]
    return filtered_list

@app.get("/books/id/{id}", status_code=status.HTTP_200_OK)
async def read_book_by_id(book_id: int = Path(ge=0)):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')


@app.delete("books/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Query(ge=0)):
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return "book deleted successfully"
    raise HTTPException(status_code=404, detail='Item not found')

@app.put("/books/update",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_id: int = Query(ge=0), book_request: BookRequest = None):
    for book in books:
        if book.id == book_id:
            book.title = book_request.title
            book.author = book_request.author
            book.category = book_request.category
            book.rating = book_request.rating
            book.published_year = book_request.published_year
            return "book updated successfully"
    raise HTTPException(status_code=404, detail='Item not found')