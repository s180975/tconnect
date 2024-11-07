from sqlalchemy import Column, Integer, String
from database import Base  # Make sure Base is imported from the database file

class User(Base):
    __tablename__ = 'users'  # Name of the table in the database

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    contact_info = Column(String)
