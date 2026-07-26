from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from src.repositories.trainer_repository import TrainerRepository


@dataclass(slots=True)
class TrainerSearchResult:
    """DTO for a trainer search result."""

    trainer_code: str
    trainer_name: str
    email: str | None
    primary_location: str | None
    availability_percentage: float | None
    skill_name: str
    proficiency: str | None


class TrainerService:
    """Service layer for trainer search operations."""

    def __init__(self, repository: TrainerRepository) -> None:
        self.repository = repository

    def search_by_skill(self, skill_name: str) -> List[TrainerSearchResult]:
        results = self.repository.find_by_skill(skill_name)
        return [self._to_dto(item) for item in results]

    def search_experts(self, skill_name: str) -> List[TrainerSearchResult]:
        results = self.repository.find_by_skill_and_proficiency(skill_name, "Expert")
        return [self._to_dto(item) for item in results]

    def search_by_skill_and_location(self, skill_name: str, location: str) -> List[TrainerSearchResult]:
        results = self.repository.find_by_skill(skill_name)
        filtered = [item for item in results if item.get("primary_location") and location.lower() in str(item.get("primary_location")).lower()]
        return [self._to_dto(item) for item in filtered]

    def search_available_trainers(self, skill_name: str, min_availability: float) -> List[TrainerSearchResult]:
        results = self.repository.find_by_skill(skill_name)
        filtered = [item for item in results if (item.get("availability_percentage") or 0) >= min_availability]
        return [self._to_dto(item) for item in filtered]

    def get_trainer_profile(self, trainer_code: str) -> Optional[dict[str, object]]:
        return self.repository.get_trainer_profile(trainer_code)

    @staticmethod
    def _to_dto(item: dict[str, object]) -> TrainerSearchResult:
        return TrainerSearchResult(
            trainer_code=str(item["trainer_code"]),
            trainer_name=str(item["trainer_name"]),
            email=item.get("email"),
            primary_location=item.get("primary_location"),
            availability_percentage=item.get("availability_percentage"),
            skill_name=str(item["skill_name"]),
            proficiency=item.get("proficiency"),
        )
