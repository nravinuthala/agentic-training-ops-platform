from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.validation.validator import DataValidator
from src.validation.validation_report import ValidationReport


def main() -> None:
    print("Validation Started")
    validator = DataValidator()
    results = [
        validator._validate_trainers(validator.excel_loader.load_trainers()),
        validator._validate_skills(validator.excel_loader.load_skills()),
        validator._validate_courses(validator.excel_loader.load_courses()),
        validator._validate_trainer_skills(
            validator.excel_loader.load_trainer_skills(),
            validator.excel_loader.load_trainers(),
            validator.excel_loader.load_skills(),
        ),
        validator._validate_course_skills(
            validator.excel_loader.load_course_skills(),
            validator.excel_loader.load_courses(),
            validator.excel_loader.load_skills(),
        ),
    ]
    summary = validator._build_summary(*results)
    report = ValidationReport()
    report.write(results, summary)
    print("Validation Complete")
    print(f"Report Written: {report.output_dir / 'validation_report.xlsx'}")
    print(summary)


if __name__ == "__main__":
    main()
