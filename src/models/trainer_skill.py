from __future__ import annotations

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class TrainerSkill(Base):
    __tablename__ = "trainer_skills"
    __table_args__ = (
        UniqueConstraint("trainer_id", "skill_id", name="uq_trainer_skills_trainer_skill"),
    )

    trainer_skill_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    trainer_id: Mapped[int] = mapped_column(ForeignKey("core.trainers.trainer_id"), nullable=False)
    skill_id: Mapped[int] = mapped_column(ForeignKey("core.skills.skill_id"), nullable=False)
    proficiency: Mapped[str | None] = mapped_column(String(50), nullable=True)

    trainer: Mapped["Trainer"] = relationship(back_populates="trainer_skills")
    skill: Mapped["Skill"] = relationship(back_populates="trainer_skills")

    def __repr__(self) -> str:
        return (
            f"TrainerSkill(trainer_skill_id={self.trainer_skill_id!r}, trainer_id={self.trainer_id!r}, "
            f"skill_id={self.skill_id!r}, proficiency={self.proficiency!r})"
        )
