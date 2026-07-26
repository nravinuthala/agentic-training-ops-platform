from __future__ import annotations

from typing import Any

from src.ai.intent_classifier import UserIntent
from src.services.course_service import CourseService
from src.services.recommendation_service import RecommendationService
from src.services.trainer_service import TrainerService


class QueryRouter:
    """Routes a classified intent to the appropriate business service."""

    def __init__(self, trainer_service: TrainerService, course_service: CourseService, recommendation_service: RecommendationService) -> None:
        self.trainer_service = trainer_service
        self.course_service = course_service
        self.recommendation_service = recommendation_service

    def route(self, intent: UserIntent) -> dict[str, Any]:
        """Execute the appropriate service call and return a structured payload."""
        intent_type = intent.intent_type.upper()

        if intent_type == "TRAINER_SEARCH":
            skill = intent.entity or ""
            return {
                "type": "trainer_search",
                "data": self.trainer_service.search_by_skill(skill),
            }

        if intent_type == "EXPERT_SEARCH":
            skill = intent.entity or ""
            return {
                "type": "expert_search",
                "data": self.trainer_service.search_experts(skill),
            }

        if intent_type == "COURSE_SEARCH":
            entity = intent.entity or ""
            if entity and entity.upper().startswith("CRS"):
                entity = entity.replace("CRS", "CR")
            if entity:
                return {
                    "type": "course_search",
                    "data": self.course_service.search_courses_by_skill(entity),
                }
            return {
                "type": "course_search",
                "data": [],
            }

        if intent_type == "COURSE_PROFILE":
            code = intent.entity_code or intent.entity or ""
            if code.upper().startswith("CRS"):
                code = code.replace("CRS", "CR")
            return {
                "type": "course_profile",
                "data": self.course_service.get_course_profile(code),
            }

        if intent_type == "TRAINER_PROFILE":
            code = intent.entity_code or intent.entity or ""
            return {
                "type": "trainer_profile",
                "data": self.trainer_service.get_trainer_profile(code),
            }

        if intent_type == "TRAINER_RECOMMENDATION":
            code = intent.entity_code or ""
            if not code and intent.entity:
                code = intent.entity.upper()
            if code.startswith("CRS"):
                code = code.replace("CRS", "CR")
            if code.startswith("TRN"):
                code = code.replace("TRN", "TR")
            return {
                "type": "trainer_recommendation",
                "data": self.recommendation_service.recommend_top_n(code, 5),
            }

        return {"type": "unsupported", "data": []}
