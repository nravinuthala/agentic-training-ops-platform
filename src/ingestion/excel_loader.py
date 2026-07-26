from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import Dict

import pandas as pd


class ExcelLoader:
    """Load Excel seed files from the repository data directories."""

    def __init__(self, data_dir: str | Path | None = None) -> None:
        self.repo_root = Path(__file__).resolve().parents[2]
        self.data_dir = Path(data_dir) if data_dir is not None else self.repo_root / "data" / "raw"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _resolve_file_path(self, file_name: str) -> Path:
        candidate_paths = [
            self.data_dir / file_name,
            self.repo_root / "data" / "raw" / file_name,
            self.repo_root / "data" / file_name,
            self.repo_root / file_name,
        ]

        for candidate in candidate_paths:
            if candidate.exists():
                if candidate != self.data_dir / file_name and not (self.data_dir / file_name).exists():
                    self.data_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(candidate, self.data_dir / file_name)
                return candidate

        if (self.repo_root / "generate_seed_data.py").exists():
            sys.path.insert(0, str(self.repo_root))
            from generate_seed_data import generate_all_datasets

            generated_files = generate_all_datasets(output_dir=self.repo_root / "data")
            for generated_file in generated_files:
                if generated_file.name == file_name:
                    target_file = self.data_dir / file_name
                    self.data_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(generated_file, target_file)
                    return target_file

        raise FileNotFoundError(f"Excel file not found: {self.data_dir / file_name}")

    def _read_excel(self, file_name: str) -> pd.DataFrame:
        file_path = self._resolve_file_path(file_name)
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
