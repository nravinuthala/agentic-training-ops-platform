from __future__ import annotations

from typing import List, Optional

from sqlalchemy import and_, case, desc, or_, select
from sqlalchemy.orm import Session

from src.models.trainer import Trainer
from src.models.trainer_skill import TrainerSkill
from src.models.skill import Skill


class TrainerRepository:
    """Repository for trainer search and profile lookup operations."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_skill(self, skill_name: str) -> List[dict[str, object]]:
        statement = (
            select(
                Trainer.trainer_code,
                Trainer.trainer_name,
                Trainer.email,
                Trainer.primary_location,
                Trainer.availability_percentage,
                Skill.skill_name,
                TrainerSkill.proficiency,
            )
            .join(Trainer.trainer_skills)
            .join(TrainerSkill.skill)
            .filter(Skill.skill_name.ilike(f"%{skill_name}%"))
            .order_by(
                case(
                    (TrainerSkill.proficiency == "Expert", 0),
                    (TrainerSkill.proficiency == "Advanced", 1),
                    (TrainerSkill.proficiency == "Intermediate", 2),
                    (TrainerSkill.proficiency == "Beginner", 3),
                    else_=4,
                ),
                desc(Trainer.availability_percentage),
            )
        )
        return [self._row_to_result(row) for row in self.session.execute(statement).all()]

    def find_by_skill_and_proficiency(self, skill_name: str, proficiency: str) -> List[dict[str, object]]:
        statement = (
            select(
                Trainer.trainer_code,
                Trainer.trainer_name,
                Trainer.email,
                Trainer.primary_location,
                Trainer.availability_percentage,
                Skill.skill_name,
                TrainerSkill.proficiency,
            )
            .join(Trainer.trainer_skills)
            .join(TrainerSkill.skill)
            .filter(Skill.skill_name.ilike(f"%{skill_name}%"))
            .filter(TrainerSkill.proficiency == proficiency)
            .order_by(desc(Trainer.availability_percentage))
        )
        return [self._row_to_result(row) for row in self.session.execute(statement).all()]

    def find_by_location(self, location: str) -> List[dict[str, object]]:
        statement = (
            select(
                Trainer.trainer_code,
                Trainer.trainer_name,
                Trainer.email,
                Trainer.primary_location,
                Trainer.availability_percentage,
                Skill.skill_name,
                TrainerSkill.proficiency,
            )
            .join(Trainer.trainer_skills)
            .join(TrainerSkill.skill)
            .filter(Trainer.primary_location.ilike(f"%{location}%"))
            .order_by(desc(Trainer.availability_percentage))
        )
        return [self._row_to_result(row) for row in self.session.execute(statement).all()]

    def find_available_trainers(self, min_availability: float) -> List[dict[str, object]]:
        statement = (
            select(
                Trainer.trainer_code,
                Trainer.trainer_name,
                Trainer.email,
                Trainer.primary_location,
                Trainer.availability_percentage,
                Skill.skill_name,
                TrainerSkill.proficiency,
            )
            .join(Trainer.trainer_skills)
            .join(TrainerSkill.skill)
            .filter(Trainer.availability_percentage >= min_availability)
            .order_by(desc(Trainer.availability_percentage))
        )
        return [self._row_to_result(row) for row in self.session.execute(statement).all()]

    def get_trainer_profile(self, trainer_code: str) -> Optional[dict[str, object]]:
        trainer = self.session.execute(
            select(Trainer).filter(Trainer.trainer_code == trainer_code)
        ).scalar_one_or_none()

        if trainer is None:
            return None

        skills = [
            {
                "skill_name": relation.skill.skill_name,
                "proficiency": relation.proficiency,
            }
            for relation in trainer.trainer_skills
        ]

        return {
            "trainer_code": trainer.trainer_code,
            "trainer_name": trainer.trainer_name,
            "email": trainer.email,
            "primary_location": trainer.primary_location,
            "availability_percentage": trainer.availability_percentage,
            "experience_years": trainer.experience_years,
            "status": trainer.status,
            "skills": skills,
        }

    def get_trainer_skill_profiles(self) -> List[dict[str, object]]:
        """Return trainer availability and skill proficiency profiles for ranking."""
        statement = (
            select(
                Trainer.trainer_code,
                Trainer.trainer_name,
                Trainer.availability_percentage,
                TrainerSkill.proficiency,
                Skill.skill_name,
            )
            .join(Trainer.trainer_skills)
            .join(TrainerSkill.skill)
            .order_by(Trainer.trainer_code.asc(), Trainer.trainer_name.asc())
        )

        rows = self.session.execute(statement).all()
        profiles: dict[str, dict[str, object]] = {}

        for trainer_code, trainer_name, availability, proficiency, skill_name in rows:
            profile = profiles.setdefault(
                trainer_code,
                {
                    "trainer_code": trainer_code,
                    "trainer_name": trainer_name,
                    "availability_percentage": availability,
                    "skills": [],
                },
            )
            profile["skills"].append({"skill_name": skill_name, "proficiency": proficiency})

        return list(profiles.values())

    @staticmethod
    def _row_to_result(row: tuple[object, ...]) -> dict[str, object]:
        return {
            "trainer_code": row[0],
            "trainer_name": row[1],
            "email": row[2],
            "primary_location": row[3],
            "availability_percentage": row[4],
            "skill_name": row[5],
            "proficiency": row[6],
        }
