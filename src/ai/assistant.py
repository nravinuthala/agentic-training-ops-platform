from __future__ import annotations

import logging
from typing import Any

from src.ai.intent_classifier import IntentClassifier, UserIntent
from src.ai.query_router import QueryRouter

logger = logging.getLogger(__name__)


class Assistant:
    """Natural-language assistant that routes user questions to business services."""

    def __init__(self, classifier: IntentClassifier, router: QueryRouter) -> None:
        self.classifier = classifier
        self.router = router

    def answer(self, question: str) -> str:
        """Classify the question, route it to the correct service, and format a response."""
        intent = self.classifier.classify(question)
        payload = self.router.route(intent)
        return self._format_response(intent, payload)

    def _format_response(self, intent: UserIntent, payload: dict[str, Any]) -> str:
        intent_type = intent.intent_type.upper()
        data = payload.get("data", [])

        if intent_type == "TRAINER_SEARCH":
            if not data:
                return "No trainers found for the requested skill."
            lines = ["Trainers:"]
            for item in data[:5]:
                lines.append(f"- {item.trainer_name} ({item.trainer_code}) | skill={item.skill_name} | proficiency={item.proficiency} | availability={item.availability_percentage}%")
            return "\n".join(lines)

        if intent_type == "EXPERT_SEARCH":
            if not data:
                return "No expert trainers found for the requested skill."
            lines = ["Experts:"]
            for item in data[:5]:
                lines.append(f"- {item.trainer_name} ({item.trainer_code}) | proficiency={item.proficiency} | availability={item.availability_percentage}%")
            return "\n".join(lines)

        if intent_type == "COURSE_SEARCH":
            if not data:
                return "No matching courses found."
            lines = ["Courses:"]
            for item in data[:5]:
                lines.append(f"- {item.course_name} ({item.course_code}) | area={item.technology_area} | level={item.level}")
            return "\n".join(lines)

        if intent_type == "COURSE_PROFILE":
            if not data:
                return "No course profile found for that code."
            profile = data
            lines = [
                f"Course: {profile['course_name']} ({profile['course_code']})",
                f"Duration: {profile['duration_days']} days",
                f"Level: {profile['level']}",
                f"Technology Area: {profile['technology_area']}",
                "Required Skills:",
            ]
            for skill in profile.get("required_skills", []):
                lines.append(f"- {skill['skill_name']} ({skill['skill_category']}, importance={skill['importance']})")
            return "\n".join(lines)

        if intent_type == "TRAINER_PROFILE":
            if not data:
                return "No trainer profile found for that code."
            profile = data
            lines = [
                f"Trainer: {profile['trainer_name']} ({profile['trainer_code']})",
                f"Location: {profile['primary_location']}",
                f"Availability: {profile['availability_percentage']}%",
                "Skills:",
            ]
            for skill in profile.get("skills", []):
                lines.append(f"- {skill['skill_name']} ({skill['proficiency']})")
            return "\n".join(lines)

        if intent_type == "TRAINER_RECOMMENDATION":
            if not data:
                return "No trainer recommendations available for that course."
            lines = ["Top Recommendations:"]
            for item in data[:3]:
                lines.append(
                    f"- {item.trainer_name} ({item.trainer_code}) | score={item.overall_score:.2f} | reason={item.recommendation_reason}"
                )
            return "\n".join(lines)

        return "I can help with trainer searches, course searches, course profiles, trainer profiles, and trainer recommendations."
