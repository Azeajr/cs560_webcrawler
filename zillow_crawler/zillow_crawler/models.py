# models.py
from pathlib import Path

from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_path = Path(__file__).parent.parent / "zillow_crawler.db"
db_path.unlink(missing_ok=True)

Base = declarative_base()


class ZillowListing(Base):
    __tablename__ = "zillow_listings"
    id = Column(Integer, primary_key=True)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    zipcode = Column(String)
    address = Column(String)
    price = Column(Float)
    sqft = Column(Integer)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    house_hash = Column(String)


class ZillowPage(Base):
    __tablename__ = "zillow_pages"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    crawled = Column(Boolean)
    page_hash = Column(String)


# Set up the engine and session here if you want to create tables
# from here or move this part to your main script or pipeline
engine = create_engine("sqlite:///zillow_crawler.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
