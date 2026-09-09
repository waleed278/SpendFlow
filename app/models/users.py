from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, String , func
from sqlalchemy.orm import Mapped , mapped_column , relationship

from app.db.base import Base

class UserRole(str,enum.Enum):
    EMPLOYEE = "EMPLOYEE"
    MANAGER = "MANAGER"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole,name="user_role"),
        default=UserRole.EMPLOYEE,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False,
    )

    expenses_submitted: Mapped[list["Expense"]] = relationship(
        back_populates="submitted_by",
        foreign_keys="Expense.submitted_by_id",
    )
    expenses_reviewed: Mapped[list["Expense"]] = relationship(
        back_populates="reviewed_by",
        foreign_keys="Expense.reviewed_by_id",
    )