from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.users import Users
from app.schemas.user import UserCreate
from app.auth.jwt_auth import hash_password

from app.schemas.user import UserLogin                                     # These are for "/login" route
from app.auth.jwt_auth import verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["Auth"])               # All auth related endpoints here


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(Users).filter(Users.email == user.email).first()        # email me ek validation lagaya hai apn ne of keeping it unique, so checking ki kya aready present users me email repeat to nhi hoyega
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered hai bhai!! Try another email")      # If this email already exists then, raise the error ki bhai dusra email daalo, ye to already exist krta h

    hashed_pwd = hash_password(user.password)                   # Jo password enter kiya user ne, use hash kradiya

    new_user = Users(                                           # new user created, taking email and pass as argument because, schema me UserCreate me apn ne wo define kr rkha h 
        email=user.email,   
        hashed_password=hashed_pwd
    )

    db.add(new_user)                    
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}             # new user create hogya 

from  fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):

    curr_user = db.query(Users).filter(Users.email == form_data.username).first()

    if not curr_user:
        raise HTTPException(status_code=400, detail="Invalid Credentials, user not found")
    
    if not verify_password(form_data.password, curr_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Credentials, user not found")
    
    access_token = create_access_token(
        data= {"sub": curr_user.email}              # While creating token, we have to keep payload minimal and need one entity which helps in uniquely identifying it.
    )                                               # "sub" is standard JWT claim

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

