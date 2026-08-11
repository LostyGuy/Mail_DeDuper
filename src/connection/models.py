from sqlalchemy import Column, Integer, String

from .connection import Base

class shared_emails(Base):
    __tablename__ = "shared_emails"
    
    shared_emails_id = Column(
        Integer,
        primary_key= True,
        autoincrement= True,
        nullable= False,
        unique= True,
        index= True
    )
    
    absolute_path = Column(
        String,
        nullable= False,
        unique= True,
    )
    
    date_of_mail = Column(
        String,
        nullable= False,
    )
    