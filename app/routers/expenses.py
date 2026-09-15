from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    ExpenseAccessDeniedError,
    ExpenseLockedError,
    ExpenseNotFoundError,
)
from app.db.sessions import get_db
from app.dependencies.auth import get_current_user
from app.models.expense import (
    ExpenseCategory,
    ExpenseStatus,
)
from app.models.users import User
from app.schemas.expense import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseUpdate,
)
from app.services.expense_service import (
    create_expense,
    delete_expense,
    get_expense_for_user,
    list_expenses_for_user,
    update_expense,
)


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
)

@router.post(
    "",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_expense_endpoint(
    expense_in: ExpenseCreate,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):

    return await create_expense(
        db,
        current_user,
        expense_in
    )

@router.get(
    "",
    response_model=list[ExpenseResponse],
)
async def list_expenses_endpoint(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    status_filter: ExpenseStatus | None = None,
    category_filter: ExpenseCategory | None = None,
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
):
    return await list_expenses_for_user(
        db=db,
        current_user=current_user,
        status_filter=status_filter,
        category_filter=category_filter,
        page=page,
        page_size=page_size,
    )

@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse,
)
async def get_expense_endpoint(
    expense_id: int,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):
    return await get_expense_for_user(
            db,
            current_user,
            expense_id,
        )


@router.patch(
    "/{expense_id}",
    response_model=ExpenseResponse,
)
async def update_expense_endpoint(
    expense_id: int,
    expense_in: ExpenseUpdate,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):
    try:
        return await update_expense(
            db,
            current_user,
            expense_id,
            expense_in,
        )

    except ExpenseNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    except ExpenseAccessDeniedError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this expense",
        )

    except ExpenseLockedError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only pending expenses can be edited",
        )

@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_expense_endpoint(
    expense_id: int,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):
    try:
        await delete_expense(
            db,
            current_user,
            expense_id,
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except ExpenseNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    except ExpenseAccessDeniedError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this expense",
        )

    except ExpenseLockedError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only pending expenses can be deleted",
        )


    