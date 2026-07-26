from __future__ import annotations

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class CourseSkill(Base):
    __tablename__ = "course_skills"
    __table_args__ = (
        UniqueConstraint("course_id", "skill_id", name="uq_course_skills_course_skill"),
    )

    course_skill_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("core.courses.course_id"), nullable=False)
    skill_id: Mapped[int] = mapped_column(ForeignKey("core.skills.skill_id"), nullable=False)
    importance: Mapped[str | None] = mapped_column(String(50), nullable=True)

    course: Mapped["Course"] = relationship(back_populates="course_skills")
    skill: Mapped["Skill"] = relationship(back_populates="course_skills")

    def __repr__(self) -> str:
        return (
            f"CourseSkill(course_skill_id={self.course_skill_id!r}, course_id={self.course_id!r}, "
            f"skill_id={self.skill_id!r}, importance={self.importance!r})"
        )
