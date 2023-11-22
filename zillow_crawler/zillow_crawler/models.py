# models.py
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    book_name = Column(String)
    product_price = Column(String)


class ZillowListing(Base):
    __tablename__ = "zillow_listings"
    id = Column(Integer, primary_key=True)
    address = Column(String)
    price = Column(String)


# Set up the engine and session here if you want to create tables
# from here or move this part to your main script or pipeline
engine = create_engine("sqlite:///zillow_crawler.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
