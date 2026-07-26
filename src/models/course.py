from __future__ import annotations

from typing import List

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Course(Base):
    __tablename__ = "courses"

    course_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    course_code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    course_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    duration_days: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    technology_area: Mapped[str | None] = mapped_column(String(100), nullable=True)

    course_skills: Mapped[List["CourseSkill"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return (
            f"Course(course_id={self.course_id!r}, course_code={self.course_code!r}, "
            f"course_name={self.course_name!r})"
        )


from src.models.course_skill import CourseSkill
