from fastapi import APIRouter, HTTPException , Depends , status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.core.exceptions import UserAlreadyExistsError
from app.db.sessions import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import register_user , authenticate_user
from app.core.security import create_access_token
from app.schemas.auth import   TokenResponse
from app.models.users import User
from app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate,
                   db:AsyncSession = Depends(get_db)):
    try:
        return await register_user(
            db,
            user_in,
        )
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

@router.post("/login",response_model=TokenResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],db:Annotated[AsyncSession,Depends(get_db)]):
    user = await authenticate_user(db,email=form_data.username,password=form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    access_token = create_access_token(
        user.id
    )

    return TokenResponse(
        access_token=access_token
    )

@router.get("/me",response_model=UserResponse)

async def get_me(current_user:Annotated[User,Depends(get_current_user)]):
    return current_user