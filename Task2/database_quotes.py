from datetime import datetime
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base_Quotes = declarative_base()

class Quote(Base_Quotes):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String(150), nullable=False)
    quote = Column(String(150), nullable=False)
    tags = Column(String(150), nullable=False)

    def __repr__(self):
        return f"Quote: {self.quote}, Author: {self.author}, Tags: {self.tags}"