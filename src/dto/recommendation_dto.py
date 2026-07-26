from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class TrainerRecommendation:
    """DTO describing a trainer recommendation for a course."""

    trainer_code: str
    trainer_name: str
    availability_percentage: Optional[float]
    matched_skills: list[str]
    missing_skills: list[str]
    recommended_skills_matched: int
    skill_score: float
    proficiency_score: float
    availability_score: float
    overall_score: float
    recommendation_reason: str
