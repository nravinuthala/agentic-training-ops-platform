from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.course import Course
from src.models.course_skill import CourseSkill
from src.models.skill import Skill


class CourseRepository:
    """Repository for course search and profile lookup operations."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_course_name(self, course_name: str) -> list[dict[str, Any]]:
        statement = (
            select(Course)
            .filter(Course.course_name.ilike(f"%{course_name}%"))
            .order_by(Course.course_name.asc())
        )
        return [self._course_to_dict(course) for course in self.session.execute(statement).scalars().all()]

    def find_by_technology_area(self, area: str) -> list[dict[str, Any]]:
        statement = (
            select(Course)
            .filter(Course.technology_area.ilike(f"%{area}%"))
            .order_by(Course.course_name.asc())
        )
        return [self._course_to_dict(course) for course in self.session.execute(statement).scalars().all()]

    def find_by_skill(self, skill_name: str) -> list[dict[str, Any]]:
        statement = (
            select(Course)
            .join(Course.course_skills)
            .join(CourseSkill.skill)
            .filter(Skill.skill_name.ilike(f"%{skill_name}%"))
            .order_by(Course.course_name.asc())
            .distinct()
        )
        return [self._course_to_dict(course) for course in self.session.execute(statement).scalars().all()]

    def get_course_profile(self, course_code: str) -> dict[str, Any] | None:
        course = self.session.execute(
            select(Course).filter(Course.course_code == course_code)
        ).scalar_one_or_none()

        if course is None:
            return None

        return {
            "course_code": course.course_code,
            "course_name": course.course_name,
            "duration_days": course.duration_days,
            "level": course.level,
            "technology_area": course.technology_area,
            "required_skills": [
                {
                    "skill_name": relation.skill.skill_name,
                    "skill_category": relation.skill.skill_category,
                    "importance": relation.importance,
                }
                for relation in course.course_skills
            ],
        }

    def get_course_requirements(self, course_code: str) -> dict[str, Any] | None:
        """Return course skill requirements grouped by mandatory and recommended."""
        course = self.session.execute(
            select(Course).filter(Course.course_code == course_code)
        ).scalar_one_or_none()

        if course is None:
            return None

        mandatory_skills: list[dict[str, Any]] = []
        recommended_skills: list[dict[str, Any]] = []

        for relation in course.course_skills:
            requirement = {
                "skill_name": relation.skill.skill_name,
                "skill_category": relation.skill.skill_category,
                "importance": relation.importance,
            }
            if str(relation.importance or "").lower() == "mandatory":
                mandatory_skills.append(requirement)
            else:
                recommended_skills.append(requirement)

        return {
            "course_code": course.course_code,
            "course_name": course.course_name,
            "mandatory_skills": mandatory_skills,
            "recommended_skills": recommended_skills,
        }

    def list_all_courses(self) -> list[dict[str, Any]]:
        statement = select(Course).order_by(Course.course_name.asc())
        return [self._course_to_dict(course) for course in self.session.execute(statement).scalars().all()]

    @staticmethod
    def _course_to_dict(course: Course) -> dict[str, Any]:
        return {
            "course_code": course.course_code,
            "course_name": course.course_name,
            "duration_days": course.duration_days,
            "level": course.level,
            "technology_area": course.technology_area,
            "required_skills": [
                relation.skill.skill_name for relation in course.course_skills
            ],
        }
