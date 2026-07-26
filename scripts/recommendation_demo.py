from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.database.session import SessionLocal
from src.repositories.course_repository import CourseRepository
from src.repositories.trainer_repository import TrainerRepository
from src.services.recommendation_service import RecommendationService


def print_recommendations(title: str, recommendations: list[object]) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    if not recommendations:
        print("No recommendations found.")
        return
    for index, item in enumerate(recommendations, start=1):
        print(f"Rank {index}")
        print(f"Trainer: {item.trainer_code} | {item.trainer_name}")
        print(f"Overall Score: {item.overall_score:.2f}")
        print(f"Availability: {item.availability_percentage}%")
        print(f"Matched Skills: {', '.join(item.matched_skills)}")
        print(f"Missing Skills: {', '.join(item.missing_skills) if item.missing_skills else 'None'}")
        print(f"Recommended Skills Matched: {item.recommended_skills_matched}")
        print(f"Reason: {item.recommendation_reason}")
        print()


def main() -> None:
    session = SessionLocal()
    course_repository = CourseRepository(session)
    trainer_repository = TrainerRepository(session)
    service = RecommendationService(course_repository, trainer_repository)

    course_code = "CR024"
    course_requirements = course_repository.get_course_requirements(course_code)
    if course_requirements:
        print("=" * 50)
        print("COURSE")
        print(course_requirements["course_name"])
        print("=" * 50)

    print_recommendations(f"Example 1: recommend_trainers('{course_code}')", service.recommend_trainers(course_code))
    print_recommendations(f"Example 2: recommend_top_n('{course_code}', 5)", service.recommend_top_n(course_code, 5))

    session.close()


if __name__ == "__main__":
    main()
