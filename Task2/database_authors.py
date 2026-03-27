from datetime import datetime
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime

Base_Authors = declarative_base()

class Author(Base_Authors):
    __tablename__ = "Authors"
    #Create the skeleton of the database
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(150), nullable=False)
    date_of_birth = Column(String(150), nullable=False)
    born_location = Column(String(150), nullable=False)
    description = Column(String, nullable=False)

    def __repr__(self):
        return f"Author: {self.fullname}, id: {self.id}"