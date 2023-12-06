"""
This module contains the SQLAlchemy models for the Zillow crawler.

Attributes:
    db_path (Path): The path to the database file.
    Base (DeclarativeMeta): The base class for the SQLAlchemy models.
    ZillowListing (ZillowListing): The SQLAlchemy model for storing house data.
    ZillowPage (ZillowPage): The SQLAlchemy model for storing page data.
    engine (Engine): The SQLAlchemy engine for the database.
    Session (Session): The SQLAlchemy session for the database.
"""
from pathlib import Path

from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Delete the database file if it exists currently
db_path = Path(__file__).parent.parent / "zillow_crawler.db"
db_path.unlink(missing_ok=True)

# Create the database
Base = declarative_base()


class ZillowListing(Base):
    """
    SQLAlchemy model for storing house data.
    """

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
    """
    SQLAlchemy model for storing page data.
    """
    __tablename__ = "zillow_pages"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    crawled = Column(Boolean)
    page_hash = Column(String)


# Create the database engine and session
engine = create_engine("sqlite:///zillow_crawler.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
