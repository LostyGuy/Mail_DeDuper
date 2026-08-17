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
    
    basename = Column(
            String,
            nullable= False,
        )
    
    date_of_mail = Column(
            String,
            nullable= False,
        )
    
    message_id = Column(
        Integer,
        nullable= False,
        unique= True,
    )
    
    email_path = Column(
        String,
        nullable= False,
    )
    
class user_emails(Base):
    __tablename__ = "user_emails"
    
    user_email_id = Column(
        Integer,
        nullable=False,
        unique= False,
        autoincrement= True,
        primary_key= True,
    )
    
    user_inbox_id = Column(
        Integer,
        nullable= False,
    )
    
    email_id = Column(
        Integer,
        nullable= False,
    )

class user_inboxes(Base):
    __tablename__ = "user_inboxes"
    
    inbox_id = Column(
        Integer,
        nullable= False,
        primary_key= True,
        unique= True,
        autoincrement= True
    )
    
    inbox_name = Column(
        String,
        unique= True,
        nullable= False,
    )

class duped_emails(Base):
    __tablename__ = "duped_emails"
    
    duped_emails_id = Column(
        Integer,
        primary_key= True,
        nullable= False,
        autoincrement= True
    )
    
    message_id= Column(
        String,
        nullable= False,
        unique= True
    )
    
    user_inbox_id = Column(
        Integer,
        nullable= False,
    )