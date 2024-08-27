from fastapi import FastAPI, HTTPException , status, Depends
from pydantic import BaseModel, Field
from uuid import UUID
import models
from database import engin,SessionLocal
from sqlalchemy.orm import Session

# this is to create the database and tables is it does not exist
models.Base.metadata.create_all(bind=engin)
app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Book(BaseModel):
    title:str = Field(min_length=1)
    author:str = Field(min_length=1,max_length=100)
    description:str = Field(min_length=1,max_length=100)
    rating:int = Field(gt=1,lt=101)



@app.get("/")
def read_api(db:Session = Depends(get_db)):
    return db.query(models.Books).all()

@app.post("/")
def create_book(book:Book,db:Session = Depends(get_db)):
    book_model = models.Books(
        title = book.title,
        author = book.author,
        description = book.description,
        rating = book.rating
    )

    db.add(book_model)
    db.commit()
    db.refresh(book_model) # to refress our instance so that it contains any new data from the database
    return book_model

@app.put("/{book_id}")
def update_book(book_id:int,book:Book,db:Session=Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()
    if book_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {book_id} does not exist.")

    
    book_model.title=book.title
    book_model.author=book.author
    book_model.description = book.description
    book_model.rating = book.rating
    
    db.add(book_model)
    db.commit()
    db.refresh(book_model)
    return book_model

@app.delete("/{book_id}")
def delete_book(book_id:int, db:Session=Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()
    if book_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {book_id} does not exist")
    db.delete(book_model)
    db.commit()
    return {"detail": f"Book with ID {book_id} is deleted successfully."}