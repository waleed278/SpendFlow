from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.sessions import get_db
from app.models.users import User , UserRole

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)
async def get_current_user(
        token:Annotated[str,Depends(oauth2_schema)],
        db:Annotated[AsyncSession,Depends(get_db)]
)->User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[
                settings.jwt_algorithm
            ],
        )

        subject = payload.get("sub")
        if subject is None:
            raise credentials_exception

        user_id =int(subject)

    except (
        InvalidTokenError,
        ValueError,
    ):
        raise credentials_exception


    statement = select(User).where(
        User.id == user_id
    )


    result = await db.execute(statement)

    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user


async def require_manager(
        current_user : Annotated[User, Depends(get_current_user)]
)->User:
    if current_user.role != UserRole.MANAGER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager access required"
        )
    return current_user

