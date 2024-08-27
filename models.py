from sqlalchemy import Column,String,Integer
from database import Base

class Books(Base):
    __tablename__="books"
    id = Column(Integer,primary_key=True,index=True)
    title =Column(String)
    author=Column(String)
    description = Column(String)
    rating = Column(Integer)