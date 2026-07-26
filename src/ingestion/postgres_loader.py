from __future__ import annotations

from typing import Any

import pandas as pd
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.models.course import Course
from src.models.course_skill import CourseSkill
from src.models.skill import Skill
from src.models.trainer import Trainer
from src.models.trainer_skill import TrainerSkill


class PostgresLoader:
    """Load DataFrames into PostgreSQL using natural-key upserts."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def _upsert(self, model: type[Any], natural_key: str, data: pd.DataFrame, columns: list[str]) -> int:
        inserted = 0
        for row in data.to_dict(orient="records"):
            try:
                existing = self.session.query(model).filter(getattr(model, natural_key) == row[natural_key]).first()
                if existing is None:
                    instance = model(**{col: row[col] for col in columns if col in row})
                    self.session.add(instance)
                    inserted += 1
                else:
                    for col in columns:
                        if col in row:
                            setattr(existing, col, row[col])
            except IntegrityError as exc:
                self.session.rollback()
                raise RuntimeError(f"Integrity error while upserting {model.__name__}: {exc}") from exc
        return inserted

    def load_trainers(self, df: pd.DataFrame) -> int:
        rows = df.copy()
        rows = rows.rename(columns={"trainer_code": "trainer_code"})
        if rows.empty:
            return 0

        required_columns = [
            "trainer_code",
            "trainer_name",
            "email",
            "experience_years",
            "primary_location",
            "availability_percentage",
            "status",
        ]
        return self._upsert(
            Trainer,
            "trainer_code",
            rows[required_columns],
            required_columns,
        )

    def load_skills(self, df: pd.DataFrame) -> int:
        rows = df.copy()
        if rows.empty:
            return 0

        required_columns = ["skill_code", "skill_name", "skill_category"]
        return self._upsert(Skill, "skill_code", rows[required_columns], required_columns)

    def load_courses(self, df: pd.DataFrame) -> int:
        rows = df.copy()
        if rows.empty:
            return 0

        required_columns = ["course_code", "course_name", "duration_days", "level", "technology_area"]
        return self._upsert(Course, "course_code", rows[required_columns], required_columns)

    def load_trainer_skills(self, df: pd.DataFrame) -> int:
        if df.empty:
            return 0

        inserted = 0
        for row in df.to_dict(orient="records"):
            trainer_code = row.get("trainer_code")
            skill_code = row.get("skill_code")
            if not trainer_code or not skill_code:
                raise ValueError("trainer_skills row is missing trainer_code or skill_code")

            trainer = self.session.query(Trainer).filter(Trainer.trainer_code == trainer_code).one_or_none()
            skill = self.session.query(Skill).filter(Skill.skill_code == skill_code).one_or_none()
            if trainer is None or skill is None:
                raise LookupError(f"Missing reference for trainer_code={trainer_code} or skill_code={skill_code}")

            existing = (
                self.session.query(TrainerSkill)
                .filter(TrainerSkill.trainer_id == trainer.trainer_id)
                .filter(TrainerSkill.skill_id == skill.skill_id)
                .one_or_none()
            )
            if existing is None:
                instance = TrainerSkill(
                    trainer_id=trainer.trainer_id,
                    skill_id=skill.skill_id,
                    proficiency=row.get("proficiency"),
                )
                self.session.add(instance)
                inserted += 1
            else:
                existing.proficiency = row.get("proficiency")

        return inserted

    def load_course_skills(self, df: pd.DataFrame) -> int:
        if df.empty:
            return 0

        inserted = 0
        for row in df.to_dict(orient="records"):
            course_code = row.get("course_code")
            skill_code = row.get("skill_code")
            if not course_code or not skill_code:
                raise ValueError("course_skills row is missing course_code or skill_code")

            course = self.session.query(Course).filter(Course.course_code == course_code).one_or_none()
            skill = self.session.query(Skill).filter(Skill.skill_code == skill_code).one_or_none()
            if course is None or skill is None:
                raise LookupError(f"Missing reference for course_code={course_code} or skill_code={skill_code}")

            existing = (
                self.session.query(CourseSkill)
                .filter(CourseSkill.course_id == course.course_id)
                .filter(CourseSkill.skill_id == skill.skill_id)
                .one_or_none()
            )
            if existing is None:
                instance = CourseSkill(
                    course_id=course.course_id,
                    skill_id=skill.skill_id,
                    importance=row.get("importance"),
                )
                self.session.add(instance)
                inserted += 1
            else:
                existing.importance = row.get("importance")

        return inserted

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def close(self) -> None:
        self.session.close()
