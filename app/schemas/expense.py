from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.expense import (
    ExpenseCategory,
    ExpenseStatus,
)


class ExpenseCreate(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )

    amount: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    category: ExpenseCategory


class ExpenseUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )

    amount: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    category: ExpenseCategory | None = None


class ExpenseResponse(BaseModel):
    id: int
    title: str
    description: str | None
    amount: Decimal
    category: ExpenseCategory
    status: ExpenseStatus
    submitted_by_id: int
    reviewed_by_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )