from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.database.session import SessionLocal
from src.repositories.trainer_repository import TrainerRepository
from src.services.trainer_service import TrainerService


def print_results(title: str, results: list[object]) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    if not results:
        print("No trainers found.")
        return
    for item in results:
        print(
            f"{item.trainer_code} | {item.trainer_name} | {item.primary_location} | "
            f"availability={item.availability_percentage}% | skill={item.skill_name} | proficiency={item.proficiency}"
        )


def main() -> None:
    session = SessionLocal()
    repository = TrainerRepository(session)
    service = TrainerService(repository)

    print("Trainer Search Demo")
    print("=" * 20)

    print_results("Example 1: Find trainers for Kubernetes", service.search_by_skill("Kubernetes"))
    print_results("Example 2: Find experts in Azure DevOps", service.search_experts("Azure DevOps"))
    print_results("Example 3: Find available trainers for Terraform (>= 50%)", service.search_available_trainers("Terraform", 50))

    profile = service.get_trainer_profile("TRN001")
    if profile:
        print("\nExample 4: Trainer Profile")
        print("-" * 24)
        print(f"Trainer: {profile['trainer_name']} ({profile['trainer_code']})")
        print(f"Location: {profile['primary_location']}")
        print(f"Email: {profile['email']}")
        print("Skills:")
        for skill in profile.get("skills", []):
            print(f"  - {skill['skill_name']} ({skill['proficiency']})")
    else:
        print("\nExample 4: Trainer profile not found")

    session.close()


if __name__ == "__main__":
    main()
