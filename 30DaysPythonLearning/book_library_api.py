from fastapi import FastAPI,  HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

# Creating instance of fastapi class
app = FastAPI()

# Creating class using pydantic model to ensure endpoint data validation
class Book(BaseModel):
    title : str
    author : str
    published_year : int

# Creating another class for book update (we can update any field of book_id i.e partially update)
class UpdateBook(BaseModel):
    title : Optional[str] = None
    author : Optional[str] = None
    published_year : Optional[int] = None

# Creating book dictionary
books : Dict[int, Book] = {
    1 : Book(title="The Alchemist", author="Paulo Coelho", published_year=1988),
    2: Book(title="Clean Code", author="Robert C. Martin", published_year=2008)
}

# creating variable to store new book_id index.Start book_id after last existing book_id
book_id_counter = max(books.keys())+1

# getting book detail
@app.get("/books")
def get_all_books():
    return {book_id : book for book_id, book in books.items()}

# getting book details by using book_id (using path parameter)
@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]

# Adding new book details in existing book dictionary
@app.post("/books")
def add_book(book: Book):
    global book_id_counter
    books[book_id_counter] = book
    response = {"book_id": book_id_counter, **book.dict()}
    book_id_counter += 1
    return response

# updating book details. Getting book by book_id to update particular details
@app.put("/books/{book_id}")
def update_book(book_id: int, updated: UpdateBook):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")

    book = books[book_id]

    # Manually update each field if it's provided
    if updated.title is not None:
        book.title = updated.title
    if updated.author is not None:
        book.author = updated.author
    if updated.published_year is not None:
        book.published_year = updated.published_year

    # Save back to dictionary
    books[book_id] = book
    return {"book_id": book_id, **book.dict()}

# deleting book 
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    del books[book_id]
    return {"message": f"Book {book_id} deleted successfully"}
