from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.database.session import SessionLocal
from src.repositories.course_repository import CourseRepository
from src.services.course_service import CourseService


def print_search_results(title: str, results: list[object]) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    if not results:
        print("No courses found.")
        return
    for item in results:
        print(
            f"{item.course_code} | {item.course_name} | {item.technology_area} | "
            f"level={item.level} | skills={', '.join(item.required_skills)}"
        )


def resolve_course_code(service: CourseService, requested_code: str) -> str:
    if service.get_course_profile(requested_code):
        return requested_code
    if requested_code.startswith("CRS") and requested_code[3:].isdigit():
        fallback = f"CR{requested_code[3:]}"
        if service.get_course_profile(fallback):
            return fallback
    return requested_code


def main() -> None:
    session = SessionLocal()
    repository = CourseRepository(session)
    service = CourseService(repository)

    print("Course Search Demo")
    print("=" * 20)

    print_search_results("Example 1: Search Azure", service.search_courses("Azure"))
    print_search_results("Example 2: Search courses requiring Terraform", service.search_courses_by_skill("Terraform"))

    requested_code = "CRS001"
    resolved_code = resolve_course_code(service, requested_code)
    profile = service.get_course_profile(resolved_code)
    if profile:
        print(f"\nExample 3: Course Profile ({requested_code})")
        print("-" * 24)
        print(f"Code: {profile['course_code']}")
        print(f"Name: {profile['course_name']}")
        print(f"Duration: {profile['duration_days']} days")
        print(f"Level: {profile['level']}")
        print(f"Technology Area: {profile['technology_area']}")
        print("Required Skills:")
        for skill in profile.get("required_skills", []):
            print(f"  - {skill['skill_name']} ({skill['skill_category']}, importance={skill['importance']})")

    requirements = service.get_course_skill_requirements(resolved_code)
    print("\nExample 4: Course Skill Requirements")
    print("-" * 35)
    if not requirements:
        print("No skill requirements found.")
    for requirement in requirements:
        print(f"- {requirement.skill_name} | category={requirement.skill_category} | importance={requirement.importance}")

    session.close()


if __name__ == "__main__":
    main()
