from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


class ExcelLoader:
    """Load Excel seed files from the raw data directory."""

    def __init__(self, data_dir: str | Path | None = None) -> None:
        self.data_dir = Path(data_dir or Path(__file__).resolve().parents[2] / "data" / "raw")
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _read_excel(self, file_name: str) -> pd.DataFrame:
        file_path = self.data_dir / file_name
        if not file_path.exists():
            raise FileNotFoundError(f"Excel file not found: {file_path}")
        return pd.read_excel(file_path)

    def load_trainers(self) -> pd.DataFrame:
        return self._read_excel("trainers.xlsx")

    def load_skills(self) -> pd.DataFrame:
        return self._read_excel("skills.xlsx")

    def load_courses(self) -> pd.DataFrame:
        return self._read_excel("courses.xlsx")

    def load_trainer_skills(self) -> pd.DataFrame:
        return self._read_excel("trainer_skills.xlsx")

    def load_course_skills(self) -> pd.DataFrame:
        return self._read_excel("course_skills.xlsx")

    def get_all_frames(self) -> Dict[str, pd.DataFrame]:
        return {
            "trainers": self.load_trainers(),
            "skills": self.load_skills(),
            "courses": self.load_courses(),
            "trainer_skills": self.load_trainer_skills(),
            "course_skills": self.load_course_skills(),
        }
