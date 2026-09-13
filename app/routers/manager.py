from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    ExpenseNotFoundError,
    InvlaidExpenseStateError
)
from app.db.sessions import get_db
from app.dependencies.auth import require_manager
from app.models.expense import (
    ExpenseCategory,
    ExpenseStatus,
)
from app.models.users import User
from app.schemas.expense import ExpenseResponse
from app.services.expense_service import (
    approve_expense,
    list_all_expenses,
    reject_expense,
)


router = APIRouter(
    prefix="/manager",
    tags=["Manager"],
)
@router.get(
    "/expenses",
    response_model=list[ExpenseResponse],
)
async def list_company_expenses(
    manager: Annotated[
        User,
        Depends(require_manager),
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
    return await list_all_expenses(
        db=db,
        status_filter=status_filter,
        category_filter=category_filter,
        page=page,
        page_size=page_size,
    )

@router.post(
    "/expenses/{expense_id}/approve",
    response_model=ExpenseResponse,
)
async def approve_expense_endpoint(
    expense_id: int,
    manager: Annotated[
        User,
        Depends(require_manager),
    ],
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):
    try:
        return await approve_expense(
            db=db,
            manager=manager,
            expense_id=expense_id,
        )

    except ExpenseNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    except InvalidExpenseStateError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only pending expenses can be approved",
        )
@router.post(
    "/expenses/{expense_id}/reject",
    response_model=ExpenseResponse,
)
async def reject_expense_endpoint(
    expense_id: int,
    manager: Annotated[
        User,
        Depends(require_manager),
    ],
    db: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):
    try:
        return await reject_expense(
            db=db,
            manager=manager,
            expense_id=expense_id,
        )

    except ExpenseNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    except InvalidExpenseStateError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only pending expenses can be rejected",
        )