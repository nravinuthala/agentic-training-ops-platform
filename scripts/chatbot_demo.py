from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.ai.assistant import Assistant
from src.ai.intent_classifier import IntentClassifier
from src.ai.query_router import QueryRouter
from src.database.session import SessionLocal
from src.repositories.course_repository import CourseRepository
from src.repositories.trainer_repository import TrainerRepository
from src.services.course_service import CourseService
from src.services.recommendation_service import RecommendationService
from src.services.trainer_service import TrainerService


def build_assistant() -> Assistant:
    session = SessionLocal()
    trainer_repository = TrainerRepository(session)
    course_repository = CourseRepository(session)
    trainer_service = TrainerService(trainer_repository)
    course_service = CourseService(course_repository)
    recommendation_service = RecommendationService(course_repository, trainer_repository)
    router = QueryRouter(trainer_service, course_service, recommendation_service)
    classifier = IntentClassifier()
    return Assistant(classifier, router)


def main() -> None:
    assistant = build_assistant()
    questions = [
        "Who can teach Kubernetes?",
        "Who are the experts in Kubernetes?",
        "Show Terraform courses.",
        "Recommend trainer for CRS004.",
        "Show profile for TR001.",
    ]

    for question in questions:
        print(f"\nUser: {question}")
        print("-" * (len(question) + 6))
        print(assistant.answer(question))


if __name__ == "__main__":
    main()
