from __future__ import annotations

from typing import List

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Trainer(Base):
    __tablename__ = "trainers"

    trainer_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    trainer_code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    trainer_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    experience_years: Mapped[int | None] = mapped_column(nullable=True)
    primary_location: Mapped[str | None] = mapped_column(String(100), nullable=True)
    availability_percentage: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)

    trainer_skills: Mapped[List["TrainerSkill"]] = relationship(
        back_populates="trainer",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return (
            f"Trainer(trainer_id={self.trainer_id!r}, trainer_code={self.trainer_code!r}, "
            f"trainer_name={self.trainer_name!r})"
        )


from src.models.trainer_skill import TrainerSkill
