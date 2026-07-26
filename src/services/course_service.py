from __future__ import annotations

from typing import Any

from src.dto.course_dto import CourseSearchResult, CourseSkillRequirement
from src.repositories.course_repository import CourseRepository


class CourseService:
    """Service layer for course search and course profile operations."""

    def __init__(self, repository: CourseRepository) -> None:
        self.repository = repository

    def search_courses(self, course_name: str) -> list[CourseSearchResult]:
        courses = self.repository.find_by_course_name(course_name)
        return [self._to_search_result(item) for item in courses]

    def search_by_technology_area(self, area: str) -> list[CourseSearchResult]:
        courses = self.repository.find_by_technology_area(area)
        return [self._to_search_result(item) for item in courses]

    def search_courses_by_skill(self, skill: str) -> list[CourseSearchResult]:
        courses = self.repository.find_by_skill(skill)
        return [self._to_search_result(item) for item in courses]

    def get_course_profile(self, course_code: str) -> dict[str, Any] | None:
        profile = self.repository.get_course_profile(course_code)
        if profile is None:
            return None
        return {
            "course_code": profile["course_code"],
            "course_name": profile["course_name"],
            "duration_days": profile["duration_days"],
            "level": profile["level"],
            "technology_area": profile["technology_area"],
            "required_skills": [
                {
                    "skill_name": item["skill_name"],
                    "skill_category": item["skill_category"],
                    "importance": item["importance"],
                }
                for item in profile["required_skills"]
            ],
        }

    def get_course_skill_requirements(self, course_code: str) -> list[CourseSkillRequirement]:
        profile = self.repository.get_course_profile(course_code)
        if profile is None:
            return []
        return [
            CourseSkillRequirement(
                skill_name=item["skill_name"],
                skill_category=item.get("skill_category"),
                importance=item.get("importance"),
            )
            for item in profile["required_skills"]
        ]

    @staticmethod
    def _to_search_result(item: dict[str, Any]) -> CourseSearchResult:
        return CourseSearchResult(
            course_code=str(item["course_code"]),
            course_name=item.get("course_name"),
            duration_days=item.get("duration_days"),
            level=item.get("level"),
            technology_area=item.get("technology_area"),
            required_skills=list(item.get("required_skills", [])),
        )
