from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    ExpenseAccessDeniedError,
    ExpenseLockedError,
    ExpenseNotFoundError,
    InvlaidExpenseStateError,
    UserAlreadyExistsError,
)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(UserAlreadyExistsError)
    async def user_already_exists_handler(
        request: Request,
        exc: UserAlreadyExistsError,
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": "Email already registered"
            },
        )

    @app.exception_handler(ExpenseNotFoundError)
    async def expense_not_found_handler(
        request: Request,
        exc: ExpenseNotFoundError,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": "Expense not found"
            },
        )

    @app.exception_handler(ExpenseAccessDeniedError)
    async def expense_access_denied_handler(
        request: Request,
        exc: ExpenseAccessDeniedError,
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "detail": "You do not have access to this expense"
            },
        )

    @app.exception_handler(ExpenseLockedError)
    async def expense_locked_handler(
        request: Request,
        exc: ExpenseLockedError,
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": "Expense is no longer editable"
            },
        )

    @app.exception_handler(InvlaidExpenseStateError)
    async def invalid_expense_state_handler(
        request: Request,
        exc: InvlaidExpenseStateError,
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": "Expense state does not allow this action"
            },
        )