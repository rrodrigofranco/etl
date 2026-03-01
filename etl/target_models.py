from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Declaring the Signal model from the signal table
class Signal(Base):
    __tablename__ = "signal"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

# Declaring the Data model from the data table
class Data(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    signal_id = Column(Integer, ForeignKey("signal.id"))
    value = Column(Float)