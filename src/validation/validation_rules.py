from __future__ import annotations

import re
from collections import Counter
from typing import Any, Dict, List, Tuple

import pandas as pd


class ValidationRules:
    """Validation rules for each dataset."""

    VALID_PROFICIENCIES = {"Beginner", "Intermediate", "Advanced", "Expert"}
    VALID_IMPORTANCES = {"Mandatory", "Recommended"}

    @staticmethod
    def validate_trainers(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[Dict[str, Any]], Dict[str, Any]]:
        errors: List[Dict[str, Any]] = []
        warnings: List[Dict[str, Any]] = []
        stats: Dict[str, Any] = {
            "duplicate_counts": {},
            "missing_value_counts": {},
            "reference_failures": {},
        }

        working_df = df.copy()
        working_df["__row_error"] = False
        working_df["__row_warning"] = False

        required_columns = {"trainer_code", "trainer_name"}
        missing_columns = required_columns - set(working_df.columns)
        if missing_columns:
            for column in sorted(missing_columns):
                errors.append({"dataset": "trainers", "row": None, "field": column, "message": "Missing required column"})

        if "trainer_code" in working_df.columns:
            duplicate_codes = working_df[working_df["trainer_code"].duplicated(keep=False)]
            if not duplicate_codes.empty:
                stats["duplicate_counts"]["trainer_code"] = int(duplicate_codes["trainer_code"].count())
                for index, value in duplicate_codes["trainer_code"].dropna().items():
                    errors.append({"dataset": "trainers", "row": int(index) + 2, "field": "trainer_code", "message": f"Duplicate trainer_code: {value}"})

        for column in ["trainer_code", "trainer_name"]:
            if column in working_df.columns:
                missing_count = int(working_df[column].isna().sum())
                if missing_count:
                    stats["missing_value_counts"][column] = missing_count
                    for index, value in working_df[working_df[column].isna()].index.items():
                        errors.append({"dataset": "trainers", "row": int(index) + 2, "field": column, "message": "Missing required value"})

        if "email" in working_df.columns:
            pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
            invalid_emails = working_df[working_df["email"].notna() & ~working_df["email"].astype(str).str.match(pattern)]
            if not invalid_emails.empty:
                for index in invalid_emails.index:
                    errors.append({"dataset": "trainers", "row": int(index) + 2, "field": "email", "message": "Invalid email format"})

        if "experience_years" in working_df.columns:
            negative = working_df[working_df["experience_years"].notna() & (working_df["experience_years"] < 0)]
            if not negative.empty:
                for index in negative.index:
                    errors.append({"dataset": "trainers", "row": int(index) + 2, "field": "experience_years", "message": "experience_years must be >= 0"})

        if "availability_percentage" in working_df.columns:
            invalid_range = working_df[working_df["availability_percentage"].notna() & ((working_df["availability_percentage"] < 0) | (working_df["availability_percentage"] > 100))]
            if not invalid_range.empty:
                for index in invalid_range.index:
                    errors.append({"dataset": "trainers", "row": int(index) + 2, "field": "availability_percentage", "message": "availability_percentage must be between 0 and 100"})

        working_df["__is_valid"] = True
        if errors:
            working_df.loc[working_df.index.isin([error["row"] - 2 for error in errors if error["row"] is not None]), "__is_valid"] = False
        return working_df, errors, stats

    @staticmethod
    def validate_skills(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[Dict[str, Any]], Dict[str, Any]]:
        errors: List[Dict[str, Any]] = []
        stats: Dict[str, Any] = {
            "duplicate_counts": {},
            "missing_value_counts": {},
            "reference_failures": {},
        }
        working_df = df.copy()
        working_df["__is_valid"] = True

        for column in ["skill_code", "skill_name"]:
            if column in working_df.columns:
                missing_count = int(working_df[column].isna().sum())
                if missing_count:
                    stats["missing_value_counts"][column] = missing_count
                    for index, value in working_df[working_df[column].isna()].index.items():
                        errors.append({"dataset": "skills", "row": int(index) + 2, "field": column, "message": "Missing required value"})

        if "skill_code" in working_df.columns:
            duplicate_codes = working_df[working_df["skill_code"].duplicated(keep=False)]
            if not duplicate_codes.empty:
                stats["duplicate_counts"]["skill_code"] = int(duplicate_codes["skill_code"].count())
                for index, value in duplicate_codes["skill_code"].dropna().items():
                    errors.append({"dataset": "skills", "row": int(index) + 2, "field": "skill_code", "message": f"Duplicate skill_code: {value}"})

        if errors:
            working_df.loc[working_df.index.isin([error["row"] - 2 for error in errors if error["row"] is not None]), "__is_valid"] = False
        return working_df, errors, stats

    @staticmethod
    def validate_courses(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[Dict[str, Any]], Dict[str, Any]]:
        errors: List[Dict[str, Any]] = []
        stats: Dict[str, Any] = {
            "duplicate_counts": {},
            "missing_value_counts": {},
            "reference_failures": {},
        }
        working_df = df.copy()
        working_df["__is_valid"] = True

        for column in ["course_code", "course_name"]:
            if column in working_df.columns:
                missing_count = int(working_df[column].isna().sum())
                if missing_count:
                    stats["missing_value_counts"][column] = missing_count
                    for index, value in working_df[working_df[column].isna()].index.items():
                        errors.append({"dataset": "courses", "row": int(index) + 2, "field": column, "message": "Missing required value"})

        if "course_code" in working_df.columns:
            duplicate_codes = working_df[working_df["course_code"].duplicated(keep=False)]
            if not duplicate_codes.empty:
                stats["duplicate_counts"]["course_code"] = int(duplicate_codes["course_code"].count())
                for index, value in duplicate_codes["course_code"].dropna().items():
                    errors.append({"dataset": "courses", "row": int(index) + 2, "field": "course_code", "message": f"Duplicate course_code: {value}"})

        if "duration_days" in working_df.columns:
            invalid_duration = working_df[working_df["duration_days"].notna() & (working_df["duration_days"] <= 0)]
            if not invalid_duration.empty:
                for index in invalid_duration.index:
                    errors.append({"dataset": "courses", "row": int(index) + 2, "field": "duration_days", "message": "duration_days must be > 0"})

        if errors:
            working_df.loc[working_df.index.isin([error["row"] - 2 for error in errors if error["row"] is not None]), "__is_valid"] = False
        return working_df, errors, stats

    @staticmethod
    def validate_trainer_skills(
        df: pd.DataFrame,
        existing_trainers: set[str],
        existing_skills: set[str],
    ) -> Tuple[pd.DataFrame, List[Dict[str, Any]], Dict[str, Any]]:
        errors: List[Dict[str, Any]] = []
        stats: Dict[str, Any] = {
            "duplicate_counts": {},
            "missing_value_counts": {},
            "reference_failures": {},
        }
        working_df = df.copy()
        working_df["__is_valid"] = True

        for column in ["trainer_code", "skill_code", "proficiency"]:
            if column in working_df.columns:
                missing_count = int(working_df[column].isna().sum())
                if missing_count:
                    stats["missing_value_counts"][column] = missing_count
                    for index, value in working_df[working_df[column].isna()].index.items():
                        errors.append({"dataset": "trainer_skills", "row": int(index) + 2, "field": column, "message": "Missing required value"})

        if "proficiency" in working_df.columns:
            invalid_proficiency = working_df[working_df["proficiency"].notna() & ~working_df["proficiency"].isin(ValidationRules.VALID_PROFICIENCIES)]
            if not invalid_proficiency.empty:
                for index in invalid_proficiency.index:
                    errors.append({"dataset": "trainer_skills", "row": int(index) + 2, "field": "proficiency", "message": "Invalid proficiency value"})

        if "trainer_code" in working_df.columns:
            missing_trainers = working_df[~working_df["trainer_code"].isin(existing_trainers)]
            if not missing_trainers.empty:
                stats["reference_failures"]["trainer_code"] = int(missing_trainers.shape[0])
                for index in missing_trainers.index:
                    errors.append({"dataset": "trainer_skills", "row": int(index) + 2, "field": "trainer_code", "message": "Referenced trainer_code does not exist"})

        if "skill_code" in working_df.columns:
            missing_skills = working_df[~working_df["skill_code"].isin(existing_skills)]
            if not missing_skills.empty:
                stats["reference_failures"]["skill_code"] = int(missing_skills.shape[0])
                for index in missing_skills.index:
                    errors.append({"dataset": "trainer_skills", "row": int(index) + 2, "field": "skill_code", "message": "Referenced skill_code does not exist"})

        if {"trainer_code", "skill_code"}.issubset(working_df.columns):
            duplicate_mappings = working_df.duplicated(subset=["trainer_code", "skill_code"], keep=False)
            if duplicate_mappings.any():
                stats["duplicate_counts"]["trainer_code_skill_code"] = int(duplicate_mappings.sum())
                for index in working_df.index[duplicate_mappings]:
                    errors.append({"dataset": "trainer_skills", "row": int(index) + 2, "field": "trainer_code/skill_code", "message": "Duplicate trainer-skill mapping"})

        if errors:
            working_df.loc[working_df.index.isin([error["row"] - 2 for error in errors if error["row"] is not None]), "__is_valid"] = False
        return working_df, errors, stats

    @staticmethod
    def validate_course_skills(
        df: pd.DataFrame,
        existing_courses: set[str],
        existing_skills: set[str],
    ) -> Tuple[pd.DataFrame, List[Dict[str, Any]], Dict[str, Any]]:
        errors: List[Dict[str, Any]] = []
        stats: Dict[str, Any] = {
            "duplicate_counts": {},
            "missing_value_counts": {},
            "reference_failures": {},
        }
        working_df = df.copy()
        working_df["__is_valid"] = True

        for column in ["course_code", "skill_code", "importance"]:
            if column in working_df.columns:
                missing_count = int(working_df[column].isna().sum())
                if missing_count:
                    stats["missing_value_counts"][column] = missing_count
                    for index, value in working_df[working_df[column].isna()].index.items():
                        errors.append({"dataset": "course_skills", "row": int(index) + 2, "field": column, "message": "Missing required value"})

        if "importance" in working_df.columns:
            invalid_importance = working_df[working_df["importance"].notna() & ~working_df["importance"].isin(ValidationRules.VALID_IMPORTANCES)]
            if not invalid_importance.empty:
                for index in invalid_importance.index:
                    errors.append({"dataset": "course_skills", "row": int(index) + 2, "field": "importance", "message": "Invalid importance value"})

        if "course_code" in working_df.columns:
            missing_courses = working_df[~working_df["course_code"].isin(existing_courses)]
            if not missing_courses.empty:
                stats["reference_failures"]["course_code"] = int(missing_courses.shape[0])
                for index in missing_courses.index:
                    errors.append({"dataset": "course_skills", "row": int(index) + 2, "field": "course_code", "message": "Referenced course_code does not exist"})

        if "skill_code" in working_df.columns:
            missing_skills = working_df[~working_df["skill_code"].isin(existing_skills)]
            if not missing_skills.empty:
                stats["reference_failures"]["skill_code"] = int(missing_skills.shape[0])
                for index in missing_skills.index:
                    errors.append({"dataset": "course_skills", "row": int(index) + 2, "field": "skill_code", "message": "Referenced skill_code does not exist"})

        if {"course_code", "skill_code"}.issubset(working_df.columns):
            duplicate_mappings = working_df.duplicated(subset=["course_code", "skill_code"], keep=False)
            if duplicate_mappings.any():
                stats["duplicate_counts"]["course_code_skill_code"] = int(duplicate_mappings.sum())
                for index in working_df.index[duplicate_mappings]:
                    errors.append({"dataset": "course_skills", "row": int(index) + 2, "field": "course_code/skill_code", "message": "Duplicate course-skill mapping"})

        if errors:
            working_df.loc[working_df.index.isin([error["row"] - 2 for error in errors if error["row"] is not None]), "__is_valid"] = False
        return working_df, errors, stats
