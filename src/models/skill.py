from __future__ import annotations

from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Skill(Base):
    __tablename__ = "skills"

    skill_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    skill_code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    skill_name: Mapped[str] = mapped_column(String(200), nullable=False)
    skill_category: Mapped[str | None] = mapped_column(String(100), nullable=True)

    trainer_skills: Mapped[List["TrainerSkill"]] = relationship(
        back_populates="skill",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    course_skills: Mapped[List["CourseSkill"]] = relationship(
        back_populates="skill",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return (
            f"Skill(skill_id={self.skill_id!r}, skill_code={self.skill_code!r}, "
            f"skill_name={self.skill_name!r})"
        )


from src.models.course_skill import CourseSkill
from src.models.trainer_skill import TrainerSkill
