# auth_routes.py
from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from pydantic import BaseModel
import database, models, auth

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, session: Session = Depends(database.get_session)):
    # 1. Find user in DB
    user = session.exec(select(models.User).where(models.User.username == request.username)).first()
    if not user or not auth.verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # 2. Create JWT
    token = auth.create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=token)

@router.get("/me")
def get_me(session: Session = Depends(database.get_session)):
    # Placeholder for now, we will protect this in the next step
    return {"message": "You are authenticated"}