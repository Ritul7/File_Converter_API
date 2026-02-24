from pydantic import BaseModel

class UserCreate(BaseModel):            # Jab User create hoga to email and password leje ayega,
    email: str
    password: str

class UserLogin(BaseModel):             # Similarly jab login krega tab bhi 
    email: str
    password: str

class UserResponse(BaseModel):          # Reponse jayega to user ki id and email jayega in return
    id: int
    email: str

    class Config:
        from_attributes = True      # Reads value from objects too, not expects dictionary only.