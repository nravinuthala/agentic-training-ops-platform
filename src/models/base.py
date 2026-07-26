from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy declarative models."""

    metadata = MetaData(schema="core")

    type_annotation_map: dict[type[Any], type[Any]] = {}

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def __repr__(self) -> str:
        columns = ", ".join(
            f"{column_name}={getattr(self, column_name)!r}"
            for column_name in self.__table__.columns.keys()
        )
        return f"{self.__class__.__name__}({columns})"
