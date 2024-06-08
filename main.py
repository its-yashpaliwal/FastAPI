from fastapi import FastAPI,Query,Depends 
from typing import Optional
from database import Base,engine,SessionLocal
from sqlalchemy import Column,String,Integer,Boolean
from sqlalchemy.orm import Session
app = FastAPI()

from pydantic import BaseModel



#Model is being created here
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,index=True)
    email = Column(String,unique=True,index=True)
    is_active= Column(Boolean,default=True)


#Creating Schema
class UserSchema(BaseModel):
    id:int
    email:str
    is_active:bool

    class Config:
        orm_model=True

Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/hello")
def index():
    return "Hello"

@app.post("/addUser",response_model=UserSchema)
def addUser( user:UserSchema,db:Session=Depends(get_db) ):
    u=User(email=user.email,is_active=user.is_active,id=user.id)
    db.add(u)
    db.commit()
    return u

    
