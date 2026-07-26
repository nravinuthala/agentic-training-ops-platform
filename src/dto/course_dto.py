from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class CourseSearchResult:
    """DTO representing a course search result."""

    course_code: str
    course_name: str | None
    duration_days: float | None
    level: str | None
    technology_area: str | None
    required_skills: list[str]


@dataclass(slots=True)
class CourseSkillRequirement:
    """DTO representing a required skill for a course."""

    skill_name: str
    skill_category: Optional[str]
    importance: Optional[str]
