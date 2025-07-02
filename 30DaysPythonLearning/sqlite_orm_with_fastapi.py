from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session, sessionmaker
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional,List

# initialize fastapi by creating its instance
app = FastAPI()

# sqlite database url
db_url = "sqlite:///./books.db"

# create engine
engine = create_engine(db_url, connect_args= {'check_same_thread' : False})

# session
SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind=engine)

# Base class for orm model
Base = declarative_base()

# defining database model
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    year = Column(Integer)

# creating function to get db session
def get_db():
    '''
        This function is responsible for managing database session which is crucial
        for interacting with database.
        It ensures the db session is closed after the request is processed whether 
        it is successful or error occured. This is crucial for preventing db connection leaks
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Defining pydantic model
# This model validates thedata before stored data into database

class BookCreate(BaseModel):
    title: str
    author: str
    year: int

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None

class DeleteBookMessage(BaseModel):
    message : str
    
class BookResponse(BookCreate):
    id: int

    class Config:
        orm_mode = True

# Create tables
Base.metadata.create_all(bind=engine)

# CRUD operation
@app.post("/books/", response_model= BookResponse )
def create_book(book : BookCreate, db : Session = Depends(get_db)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# get all book details
@app.get("/books/", response_model= List[BookResponse])
def get_books(db : Session = Depends(get_db)):
    return db.query(Book).all()

# get book by book id
@app.get("/books/{book_id}", response_model= BookResponse)
def get_book(book_id : int, db : Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if db_book is None:
        raise HTTPException(status_code= 404, detail= "Book not found")
    return db_book

# update book
@app.put("/books/{book_id}", response_model= BookResponse)
def update_book(book_id : int, updated_data : BookUpdate, db : Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if not db_book:
        raise HTTPException(status_code= 404, detail= "Book not found")
    
    # Update only fields that are provided
    update_fields = updated_data.dict(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book

# delete book by book id
@app.delete("/books/{book_id}", response_model= DeleteBookMessage)
def delete_book(book_id : int, db :Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if not db_book:
        raise HTTPException(status_code= 404, detail= "Book not found")
    
    db.delete(db_book)
    db.commit()
    return {"message": f"Book '{db_book.title}' deleted successfully"}




    

