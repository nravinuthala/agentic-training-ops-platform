from __future__ import annotations

import logging
import re
from typing import Any

from src.dto.recommendation_dto import TrainerRecommendation
from src.repositories.course_repository import CourseRepository
from src.repositories.trainer_repository import TrainerRepository

logger = logging.getLogger(__name__)


class RecommendationService:
    """Service for recommending trainers for a course using skill, proficiency, and availability scoring."""

    PROFICIENCY_WEIGHTS = {
        "Expert": 100.0,
        "Advanced": 75.0,
        "Intermediate": 50.0,
        "Beginner": 25.0,
    }

    def __init__(self, course_repository: CourseRepository, trainer_repository: TrainerRepository) -> None:
        self.course_repository = course_repository
        self.trainer_repository = trainer_repository

    def recommend_trainers(self, course_code: str) -> list[TrainerRecommendation]:
        """Recommend trainers for a course, excluding trainers that miss mandatory skills."""
        course_requirements = self.course_repository.get_course_requirements(course_code)
        if course_requirements is None:
            logger.warning("Course %s not found", course_code)
            return []

        mandatory_skills = [skill["skill_name"] for skill in course_requirements["mandatory_skills"]]
        recommended_skills = [skill["skill_name"] for skill in course_requirements["recommended_skills"]]

        trainer_profiles = self.trainer_repository.get_trainer_skill_profiles()
        recommendations: list[TrainerRecommendation] = []

        for profile in trainer_profiles:
            trainer_skill_names = [skill["skill_name"] for skill in profile["skills"]]
            trainer_skills = {self._normalize_skill_name(skill) for skill in trainer_skill_names}
            normalized_mandatory = {self._normalize_skill_name(skill) for skill in mandatory_skills}
            normalized_recommended = {self._normalize_skill_name(skill) for skill in recommended_skills}

            matched_mandatory = [skill for skill in mandatory_skills if self._normalize_skill_name(skill) in trainer_skills]
            matched_recommended = [skill for skill in recommended_skills if self._normalize_skill_name(skill) in trainer_skills]
            missing_skills = sorted({skill for skill in mandatory_skills if self._normalize_skill_name(skill) not in trainer_skills})

            if missing_skills:
                continue

            recommended_skills_matched = len(matched_recommended)

            skill_score = self._calculate_skill_score(len(matched_mandatory), len(mandatory_skills), len(matched_recommended), len(recommended_skills))
            proficiency_score = self._calculate_proficiency_score(profile["skills"])
            availability_score = self._calculate_availability_score(profile.get("availability_percentage"))
            overall_score = self._calculate_overall_score(skill_score, proficiency_score, availability_score)
            reason = self._build_reason(matched_mandatory, matched_recommended, availability_score, proficiency_score)

            recommendations.append(
                TrainerRecommendation(
                    trainer_code=str(profile["trainer_code"]),
                    trainer_name=str(profile["trainer_name"]),
                    availability_percentage=profile.get("availability_percentage"),
                    matched_skills=sorted(matched_mandatory + matched_recommended),
                    missing_skills=missing_skills,
                    recommended_skills_matched=recommended_skills_matched,
                    skill_score=round(skill_score, 2),
                    proficiency_score=round(proficiency_score, 2),
                    availability_score=round(availability_score, 2),
                    overall_score=round(overall_score, 2),
                    recommendation_reason=reason,
                )
            )

        recommendations.sort(key=lambda item: item.overall_score, reverse=True)
        return recommendations

    def recommend_top_n(self, course_code: str, top_n: int) -> list[TrainerRecommendation]:
        """Return the top N recommendations for a course."""
        recommendations = self.recommend_trainers(course_code)
        return recommendations[:top_n]

    @staticmethod
    def _normalize_skill_name(skill_name: str) -> str:
        normalized = skill_name.lower().strip()
        normalized = re.sub(r"[^a-z0-9]+", " ", normalized)
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return normalized

    @staticmethod
    def _calculate_skill_score(matched_mandatory: int, mandatory_total: int, matched_recommended: int, recommended_total: int) -> float:
        if mandatory_total == 0 and recommended_total == 0:
            return 0.0

        mandatory_component = (matched_mandatory / mandatory_total) * 100 if mandatory_total else 100.0
        recommended_component = (matched_recommended / recommended_total) * 100 if recommended_total else 0.0
        return (mandatory_component * 0.8) + (recommended_component * 0.2)

    @staticmethod
    def _calculate_proficiency_score(skills: list[dict[str, Any]]) -> float:
        if not skills:
            return 0.0
        proficiency_values = [RecommendationService.PROFICIENCY_WEIGHTS.get(str(skill.get("proficiency")), 0.0) for skill in skills]
        return sum(proficiency_values) / len(proficiency_values)

    @staticmethod
    def _calculate_availability_score(availability_percentage: Any) -> float:
        if availability_percentage is None:
            return 0.0
        try:
            return float(availability_percentage)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _calculate_overall_score(skill_score: float, proficiency_score: float, availability_score: float) -> float:
        return (skill_score * 0.60) + (proficiency_score * 0.20) + (availability_score * 0.20)

    @staticmethod
    def _build_reason(matched_mandatory: list[str], matched_recommended: list[str], availability_score: float, proficiency_score: float) -> str:
        mandatory_phrase = "Matched all mandatory skills." if len(matched_mandatory) > 0 else "Missing mandatory skills."
        recommended_phrase = f"Matched {len(matched_recommended)} recommended skills." if matched_recommended else "Matched 0 recommended skills."
        proficiency_label = "Advanced" if proficiency_score >= 75 else "Intermediate" if proficiency_score >= 50 else "Beginner"
        return (
            f"{mandatory_phrase} {recommended_phrase} "
            f"Availability {availability_score:.0f}%. Average proficiency {proficiency_label}."
        )
