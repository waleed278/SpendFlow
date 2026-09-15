from sqlalchemy import Select, delete , select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import logger
from app.core.exceptions import (
    ExpenseAccessDeniedError,
    ExpenseLockedError,
    ExpenseNotFoundError,
    InvlaidExpenseStateError
)
from app.models.expense import (
    Expense,
    ExpenseCategory,
    ExpenseStatus,
)

from app.schemas.expense import ExpenseCreate,ExpenseUpdate

from app.models.users import User


async def create_expense(
    db: AsyncSession,
    current_user: User,
    expense_in: ExpenseCreate,
) -> Expense:

    expense = Expense(
        title=expense_in.title,
        description=expense_in.description,
        amount=expense_in.amount,
        category=expense_in.category,
        submitted_by_id=current_user.id,
    )

    db.add(expense)

    await db.commit()
    await db.refresh(expense)
    logger.info(
        "Expense%s created by user %s",
        expense.id,
        current_user.id,
    )
    return expense

async def get_expense_by_id(
    db: AsyncSession,
    expense_id: int,
) -> Expense | None:

    statement = select(Expense).where(
        Expense.id == expense_id
    )

    result = await db.execute(statement)

    return result.scalar_one_or_none()

def ensure_expense_owner(
    expense: Expense,
    current_user: User,
) -> None:

    if expense.submitted_by_id != current_user.id:
        raise ExpenseAccessDeniedError()

def ensure_expense_is_pending(
    expense: Expense,
) -> None:

    if expense.status != ExpenseStatus.PENDING:
        raise ExpenseLockedError()

async def get_expense_for_user(
    db: AsyncSession,
    current_user: User,
    expense_id: int,
) -> Expense:

    expense = await get_expense_by_id(
        db,
        expense_id,
    )

    if expense is None:
        raise ExpenseNotFoundError()

    ensure_expense_owner(
        expense,
        current_user,
    )

    return expense


async def list_expenses_for_user(
        db:AsyncSession,
        current_user: User,
        status_filter: ExpenseStatus | None,
        category_filter: ExpenseCategory | None,
        page: int,
        page_size: int
)-> list[Expense]:

    statement = select(Expense).where(
        Expense.submitted_by_id == current_user.id
    )

    if status_filter is not None:
        statement = statement.where(
            Expense.status == status_filter
        )
    if category_filter is not None:
        statement = select(Expense).where(
            Expense.category == category_filter
        )

    offset = (page-1)*page_size

    statement = (
        statement.order_by(Expense.created_at.desc()).offset(offset).limit(page_size)
    )

    result = await db.execute(statement)

    return list(result.scalars().all())


async def update_expense(
    db: AsyncSession,
    current_user: User,
    expense_id: int,
    expense_in: ExpenseUpdate,
) -> Expense:

    expense = await get_expense_for_user(
        db,
        current_user,
        expense_id,
    )

    ensure_expense_is_pending(expense)

    update_data = expense_in.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(
            expense,
            field,
            value,
        )

    await db.commit()
    await db.refresh(expense)

    return expense


async def delete_expense(
    db: AsyncSession,
    current_user: User,
    expense_id: int,
) -> None:

    expense = await get_expense_for_user(
        db,
        current_user,
        expense_id,
    )

    ensure_expense_is_pending(expense)

    await db.delete(expense)
    await db.commit()


async def list_all_expenses(
    db: AsyncSession,
    status_filter: ExpenseStatus | None,
    category_filter: ExpenseCategory | None,
    page: int,
    page_size: int,
) -> list[Expense]:

    statement = select(Expense)

    if status_filter is not None:
        statement = statement.where(
            Expense.status == status_filter
        )

    if category_filter is not None:
        statement = statement.where(
            Expense.category == category_filter
        )

    offset = (page - 1) * page_size

    statement = (
        statement
        .order_by(Expense.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )

    result = await db.execute(statement)

    return list(result.scalars().all())

async def review_expense(
    db: AsyncSession,
    manager: User,
    expense_id: int,
    new_status: ExpenseStatus,
) -> Expense:

    expense = await get_expense_by_id(
        db,
        expense_id,
    )

    if expense is None:
        raise ExpenseNotFoundError()

    if expense.status != ExpenseStatus.PENDING:
        raise InvalidExpenseStateError()

    if new_status not in {
        ExpenseStatus.APPROVED,
        ExpenseStatus.REJECTED,
    }:
        raise InvalidExpenseStateError()

    expense.status = new_status
    expense.reviewed_by_id = manager.id

    await db.commit()
    await db.refresh(expense)

    return expense

async def approve_expense(
    db: AsyncSession,
    manager: User,
    expense_id: int,
) -> Expense:

    return await review_expense(
        db=db,
        manager=manager,
        expense_id=expense_id,
        new_status=ExpenseStatus.APPROVED,
    )

async def reject_expense(
    db: AsyncSession,
    manager: User,
    expense_id: int,
) -> Expense:

    return await review_expense(
        db=db,
        manager=manager,
        expense_id=expense_id,
        new_status=ExpenseStatus.REJECTED,
    )