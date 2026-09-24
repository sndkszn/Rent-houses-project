#from redis.asyncao import Redis
#from functools import lru_cache
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Annotated, Dict
from decimal import Decimal
from fastapi import Query
from datetime import datetime, timedelta


from schemas import (UserCreate, UserResponse, Token,PostBase, PostResponse, FeedbackCreate, FeedbackUpdate,
FeedbackResponse, MessageResponse, UserBalance,BasketResponse, BasketPostResponse, PostUpdate)
import models
from models import User, Post, Basket, Rental
import security
import database
from database import get_db

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#def get_redis() -> Redis:
   #return Redis(host="localhost",port=6379)

#                 ------------------------LOGIN--------------------------


@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(models.User).filter(models.User.username == user_data.username).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this nickname already exist!"
        )

    hashed_pwd = security.hash_password(user_data.password)

    db_user = models.User(
        username=user_data.username,
        hashed_password=hashed_pwd,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = security.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}



#          --------------------- USERS --------------------------


@app.get("/users/me", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[models.User, Depends(security.get_current_user)]
):
    return current_user

@app.get("/users/{user_id}", response_model=UserResponse)
async def read_users(
    user_id:int,db: Session = Depends(get_db)
):
    db_user=db.query(User).filter(User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/delete_account", response_model=MessageResponse)
async def delete_account(
    current_user: Annotated[models.User, Depends(security.get_current_user)],db: Session = Depends(get_db)):
    db.query(models.Post).filter(models.Post.author_id == current_user.id).delete()
    db.delete(current_user)
    db.commit()
    return {"ok": True, "message": "account has deleted"}

#          ------------------- BALANCE  ------------------------

@app.get("/users/me/balance", response_model=UserBalance)
async def check_b(
    current_user: Annotated[models.User, Depends(security.get_current_user)],
    db: Session = Depends(get_db)
):
    return {"balance": current_user.balance}

@app.post("/users/me/up-top", response_model=MessageResponse)
async def up_top(current_user: Annotated[models.User, Depends(security.get_current_user)],
    amount: Decimal = Query(..., gt=0),
    db: Session = Depends(get_db),
):
    current_user.balance += amount

    db.commit()
    db.refresh(current_user)

    return { "ok": True, "message": f"Balance increased by {amount}"}
    
    
#       -----------------------------POST-----------------------------


@app.post("/posts/create/", response_model=PostBase)
async def create_post(post: PostBase, current_user: Annotated[models.User, Depends(security.get_current_user)],
    db: Session = Depends(get_db)):
    db_post = models.Post(title=post.title, body=post.body, price=post.price, author_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.patch("/posts/{post_id}", response_model=PostUpdate)
async def edit_post(post_id: int, post_data: PostUpdate, 
    current_user: Annotated[models.User, Depends(security.get_current_user)],
    db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.id != current_user.id:
        raise HTTPException(status_code=403, detail="You dont have enough rights")
    
    update = post_data.model_dump(exclude_unset=True) 
    #----------"exclude_unset=True" -  delete all unsent by user messages(None)!!
    # --------- "model_dump" - do from Pydantic model to dict!!
    
    for key, value in update.items():
    #--------- "setattr" - change attributes like (post.price = 5000)!!
        
        setattr(post, key, value)
        
    db.commit()
    db.refresh(post)
    return post
        
 
@app.delete("/posts/{post_id}", response_model=MessageResponse)
async def delete_post(post_id: int,
    current_user: Annotated[models.User, Depends(security.get_current_user)],
    db: Session = Depends(get_db)):
        db_post = db.query(models.Post).filter(models.Post.id==post_id).first()
        if not db_post:
            raise HTTPException(status_code=404, detail="Post not found")
        if db_post.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="You dont have enough rights")
        db.delete(db_post)
        db.commit()
        return {"ok": True, "message": "post has deleted"}

@app.get("/posts/", response_model=List[PostResponse])
async def posts(
    current_user: Annotated[models.User, Depends(security.get_current_user)],
    db: Session = Depends(get_db)
):
    db_posts = db.query(models.Post).all()

    result = []

    for post in db_posts:
        basket = db.query(models.Basket).filter(
            models.Basket.post_id == post.id,
            models.Basket.user_id == current_user.id
        ).first()
        
        rental = db.query(models.Rental).filter(
            models.Rental.post_id == post.id,
            models.Rental.rented_until > datetime.utcnow()
        ).first()
                
        result.append({
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "price": post.price,
            "author": post.author,
            "in_basket": basket is not None,
            "is_rented": rental is not None,
            "rented_until": rental.rented_until if rental else None
        })
        
        
    return result


#               -------------------BASKET-------------------------

@app.get("/basket", response_model=List[BasketPostResponse])
async def basket_get(current_user: Annotated[models.User, Depends(security.get_current_user)],
    db: Session = Depends(get_db)):
    return db.query(models.Post).join(models.Basket).filter(
        models.Basket.user_id == current_user.id
    ).all()

@app.post("/basket/{post_id}/in", response_model=BasketResponse)
async def in_basket(post_id: int, current_user: Annotated[models.User, Depends(security.get_current_user)],
    db: Session = Depends(get_db))-> PostResponse:
    basket = db.query(Basket).filter(
        Basket.post_id == post_id,
        Basket.user_id == current_user.id
    ).first()

    if basket:
        db.delete(basket)
        message = "Removed from basket"
        added = False
    else:
        db.add(Basket(
            post_id=post_id,
            user_id=current_user.id
        ))
        message = "Added to basket"
        added = True

    db.commit()

    return {
        "ok": True,
        "message": message,
        "in_basket": added
    }
    

#         -----------------------BUY RENT----------------------------

@app.get("/rent/check", response_model=List[BasketPostResponse])
async def basket_get(current_user: Annotated[models.User, Depends(security.get_current_user)],
    db: Session = Depends(get_db)):
    return db.query(models.Post).join(models.Rental).filter(
        models.Rental.user_id == current_user.id
    ).all()

@app.post("/basket/{post_id}/rent", response_model=MessageResponse)
async def rent_house(post_id: int, current_user: Annotated[models.User, Depends(security.get_current_user)],
    db: Session = Depends(get_db)):    
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    amount = post.price
    own = post.author_id
    owner = db.query(models.User).filter(models.User.id == own).first()
    
    existing_rental = db.query(models.Rental).filter(
        models.Rental.post_id == post_id,
        models.Rental.rented_until > datetime.utcnow()
    ).first()
    

    if existing_rental:
        raise HTTPException(
            status_code=409,
            detail="This house is already rented"
        )
    
    if current_user.balance < amount:
        raise HTTPException(status_code=403, detail="You ain't have enough balance")

    current_user.balance-=amount
    owner.balance+=amount
    
    rental = models.Rental(
    user_id=current_user.id,
    post_id=post.id,
    rented_until=datetime.utcnow() + timedelta(minutes=5)
)
    
    db.add(rental)
    db.commit()
    return {"ok": "True",
            "message": "You rented the house!"}
    
    
    
@app.delete("/basket/{post_id}/cancel_rent", response_model=MessageResponse)
async def cancel_rent(
    post_id: int, 
    current_user: Annotated[models.User, Depends(security.get_current_user)],
    db: Session = Depends(get_db)
):
    rental = db.query(models.Rental).filter(
        models.Rental.post_id == post_id,
        models.Rental.user_id == current_user.id
    ).first()
    
    if not rental:
        raise HTTPException(status_code=404, detail="Rent don't found")
        
    now = datetime.utcnow()
    is_active = rental.rented_until > now
    
    if is_active:
        post = db.query(models.Post).filter(models.Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
            
        owner = db.query(models.User).filter(models.User.id == post.author_id).first()
        amount = post.price
        
        if owner.balance < amount:
            raise HTTPException(
                status_code=403, 
                detail="Rent can't be returned, owner does not have enough money"
            )
            
        current_user.balance += amount
        owner.balance -= amount

    db.delete(rental)
    db.commit()
    
    return {
        "ok": "True",
        "message": "Rent cancelled successfully!" + (" Money returned." if is_active else " Expired rental cleared.")
    }


#            ---------------------  FEEDBACK   ------------------------------------------


@app.post("/posts/{post_id}/feedback", response_model=FeedbackCreate)
async def post_feedback(text: str, post_id: int, stars: int, current_user: Annotated[models.User, Depends(security.get_current_user)],
    db: Session = Depends(get_db)):
    
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_feedback = db.query(models.Feedback).filter(
        models.Feedback.author_id == current_user.id,
        models.Feedback.post_id==post_id).first()
    
    if db_feedback:
        raise HTTPException(status_code=409, detail="There is already feedback")
    
    
    feedback = models.Feedback(post_id=post_id, author_id=current_user.id, text=text, stars=stars)
    
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback

@app.patch("/posts/{post_id}/feedback/{feedback_id}", response_model=FeedbackUpdate)
async def edit_feedback(feedback_id: int, post_id: int,
    current_user: Annotated[models.User, Depends(security.get_current_user)],
    db: Session = Depends(get_db),text: str | None = None, stars: int | None = None):
    
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_feedback = db.query(models.Feedback).filter(
        models.Feedback.id == feedback_id,
        models.Feedback.post_id==post_id).first()
    
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    if db_feedback.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to edit this feedback")
    
    if text is not None:
        db_feedback.text = text

    if stars is not None:
        db_feedback.stars = stars
    
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


@app.delete("/posts/{post_id}/feedback/{feedback_id}", response_model=MessageResponse)
async def delete_feedback(post_id: int, feedback_id: int,
    current_user: Annotated[models.User, Depends(security.get_current_user)],
    db: Session = Depends(get_db)):
    
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_feedback = db.query(models.Feedback).filter(
        models.Feedback.post_id == post_id,
        models.Feedback.id == feedback_id).first()
    
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    db.delete(db_feedback)
    db.commit()
    return {"ok": True, "message": "You have deleted the feedback"}


@app.get("/posts/{post_id}/feedbacks", response_model=List[FeedbackResponse])
async def get_feedback(post_id: int, db: Session = Depends(get_db)):
    
    return db.query(models.Feedback).filter(models.Feedback.post_id == post_id).all()