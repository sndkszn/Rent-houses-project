from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime

#   --------------- USER ------------------     

class UserCreate(BaseModel):
    username: str
    password: str
    
    class Config:
        from_attributes = True
        
class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class UserBalance(BaseModel):
    balance: Decimal
    
#   --------------- TOKEN ------------------     
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None
    
#   --------------- POST ------------------     
    
class PostBase(BaseModel):
    title: str
    body: str
    price: Decimal
    
class PostUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    price: Decimal | None = None
    
class PostResponse(PostBase):
    id: int
    author: UserResponse
    in_basket: bool = False
    is_rented: bool = False
    rented_until: datetime | None = None
    
    class Config:
        from_attributes = True
        
class MessageResponse(BaseModel):
    ok: bool
    message: str
    
#   ------------BASKET--------------------

class BasketResponse(BaseModel):
    ok: bool
    in_basket: bool
    message: str
    
class BasketPostResponse(PostBase):
    id: int
    author: UserResponse

    class Config:
        from_attributes = True
        
# ------------------FEEDBACK---------------

class FeedbackCreate(BaseModel):
    text: str
    stars: int = Field(ge=1, le=5)
    
class FeedbackUpdate(BaseModel):
    text: str | None = None
    stars: int | None = Field(default=None, ge=1, le=5)
    
class FeedbackResponse(BaseModel):
    id: int
    text: str
    stars: int = Field(ge=1, le=5)
    post_id: int
    author: UserResponse
    
    class Config:
        from_attributes = True