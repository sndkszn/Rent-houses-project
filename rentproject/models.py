from sqlalchemy import Column, Integer, String,ForeignKey, DateTime, UniqueConstraint, Numeric, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    balance = Column(Numeric(20,2), default= 0)
    
    posts = relationship("Post", back_populates="author")
    feedback = relationship("Feedback", back_populates="author")
    
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True,index=True)
    title = Column(String,index=True)
    body = Column(String)
    price = Column(Numeric(20, 2), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    
    basket = relationship("Basket", back_populates="post",cascade="all, delete-orphan")
    author = relationship("User", back_populates="posts")
    rentals = relationship("Rental", back_populates="post")
    feedback = relationship("Feedback", back_populates="post")

    
class Basket(Base):
    __tablename__ = "basket"
    __table_args__ = (UniqueConstraint("post_id", "user_id"),)
    
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    post = relationship("Post", back_populates="basket")
    user = relationship("User")
    
class Rental(Base):
    __tablename__ = "rentals"
    __table_args__ = (UniqueConstraint("post_id", "user_id"),)
    

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    rented_until = Column(DateTime, nullable=False)
    
    post = relationship("Post", back_populates="rentals")
    user = relationship("User")
    
    
class Feedback(Base):
    
    __tablename__ = "feedbacks"
    
    __table_args__ = (
        CheckConstraint("stars >= 1 AND stars <= 5", name="check_stars"),
    )
    
    id =Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String)
    stars = Column(Integer, nullable=False)
    
    post = relationship("Post", back_populates="feedback")
    author = relationship("User", back_populates="feedback")