from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd

from src.ingestion.excel_loader import ExcelLoader
from src.validation.validation_rules import ValidationRules


class DataValidator:
    """Validate Excel datasets before ingestion."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.logger = logger or self._build_logger()
        self.excel_loader = ExcelLoader()

    @staticmethod
    def _build_logger() -> logging.Logger:
        logger = logging.getLogger("data_validator")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
            logger.addHandler(handler)
        return logger

    def validate_all(self) -> Dict[str, Any]:
        frames = self.excel_loader.get_all_frames()

        trainer_df = frames["trainers"]
        skill_df = frames["skills"]
        course_df = frames["courses"]
        trainer_skill_df = frames["trainer_skills"]
        course_skill_df = frames["course_skills"]

        trainer_results = self._validate_trainers(trainer_df)
        skill_results = self._validate_skills(skill_df)
        course_results = self._validate_courses(course_df)
        trainer_skill_results = self._validate_trainer_skills(trainer_skill_df, trainer_df, skill_df)
        course_skill_results = self._validate_course_skills(course_skill_df, course_df, skill_df)

        summary = self._build_summary(
            trainer_results,
            skill_results,
            course_results,
            trainer_skill_results,
            course_skill_results,
        )
        return summary

    def _validate_trainers(self, df: pd.DataFrame) -> Dict[str, Any]:
        self.logger.info("Validating trainers.xlsx")
        validated_df, errors, stats = ValidationRules.validate_trainers(df)
        return {"name": "trainers", "dataframe": validated_df, "errors": errors, "stats": stats, "rows": len(df)}

    def _validate_skills(self, df: pd.DataFrame) -> Dict[str, Any]:
        self.logger.info("Validating skills.xlsx")
        validated_df, errors, stats = ValidationRules.validate_skills(df)
        return {"name": "skills", "dataframe": validated_df, "errors": errors, "stats": stats, "rows": len(df)}

    def _validate_courses(self, df: pd.DataFrame) -> Dict[str, Any]:
        self.logger.info("Validating courses.xlsx")
        validated_df, errors, stats = ValidationRules.validate_courses(df)
        return {"name": "courses", "dataframe": validated_df, "errors": errors, "stats": stats, "rows": len(df)}

    def _validate_trainer_skills(self, df: pd.DataFrame, trainer_df: pd.DataFrame, skill_df: pd.DataFrame) -> Dict[str, Any]:
        self.logger.info("Validating trainer_skills.xlsx")
        existing_trainers = set(trainer_df["trainer_code"].dropna().astype(str))
        existing_skills = set(skill_df["skill_code"].dropna().astype(str))
        validated_df, errors, stats = ValidationRules.validate_trainer_skills(df, existing_trainers, existing_skills)
        return {"name": "trainer_skills", "dataframe": validated_df, "errors": errors, "stats": stats, "rows": len(df)}

    def _validate_course_skills(self, df: pd.DataFrame, course_df: pd.DataFrame, skill_df: pd.DataFrame) -> Dict[str, Any]:
        self.logger.info("Validating course_skills.xlsx")
        existing_courses = set(course_df["course_code"].dropna().astype(str))
        existing_skills = set(skill_df["skill_code"].dropna().astype(str))
        validated_df, errors, stats = ValidationRules.validate_course_skills(df, existing_courses, existing_skills)
        return {"name": "course_skills", "dataframe": validated_df, "errors": errors, "stats": stats, "rows": len(df)}

    def _build_summary(self, *results: Dict[str, Any]) -> Dict[str, Any]:
        total_rows = sum(result["rows"] for result in results)
        error_count = sum(len(result["errors"]) for result in results)
        valid_rows = sum(int(result["dataframe"]["__is_valid"].sum()) for result in results)
        invalid_rows = total_rows - valid_rows

        summary = {
            "status": "PASSED" if error_count == 0 else "FAILED",
            "total_rows": int(total_rows),
            "valid_rows": int(valid_rows),
            "invalid_rows": int(invalid_rows),
            "error_count": int(error_count),
            "warning_count": 0,
        }
        return summary
