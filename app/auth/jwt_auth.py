from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY = 30

def hash_password(password: str):                                   # Password enter kiya login krte time, to hashed password is stored
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):     # Next time, user aaya so verifying the password, by hashing the current password using the same stored salt and matching them
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):                                # JWT token create krna h
    to_encode = data.copy()                                         # data ko copy isliye kr rhe h, bcz we don't want to modify the actual data
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRY)
    to_encode.update({"exp": expire})                               # to_encode me payload data already tha, usme ab expiration ka data bhi add krdiya hai ("exp" ek standard payload claim h jwt ka)
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)   # jwt created


# Token decoding....

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.users import Users

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")           # Whenever oauth2 is used as dependency, FastAPI will automatcially look for Authorization header in the incoming request, check for the Bearer word and pulls out the token string.
                                                             

def get_curr_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    
    print(token)
    credentials_excpetion = HTTPException(status_code=401, detail="Curr_user nhi mil rha h bhai")

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        email: str = payload.get("sub")

        if email is None:
            raise credentials_excpetion
        
    except JWTError:
        raise credentials_excpetion
    
    user = db.query(Users).filter(Users.email == email).first()

    if user is None:
        raise credentials_excpetion
    
    return user

# from fastapi.security import OAuth2PasswordRequestForm



