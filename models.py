from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base
from datetime import datetime

class URL(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    original_url  = Column(String, nullable=False)
    short_code = Column(String, unique=True, nullable=False) 
    clicks        = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
