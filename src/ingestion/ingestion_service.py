from __future__ import annotations

import logging
from typing import Any, Dict, List

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.database.session import SessionLocal
from src.ingestion.excel_loader import ExcelLoader
from src.ingestion.postgres_loader import PostgresLoader


class IngestionService:
    """Orchestrate Excel-to-PostgreSQL ingestion with structured logging and resilience."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.logger = logger or self._build_logger()
        self.excel_loader = ExcelLoader()

    @staticmethod
    def _build_logger() -> logging.Logger:
        logger = logging.getLogger("ingestion_service")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
            logger.addHandler(handler)
        return logger

    def run(self) -> Dict[str, Any]:
        summary: Dict[str, Any] = {
            "success": True,
            "results": [],
            "errors": [],
        }

        session = SessionLocal()
        loader = PostgresLoader(session)

        try:
            self._create_schema_and_tables(session)
            frames = self.excel_loader.get_all_frames()
            self._ingest_dataset("skills", frames["skills"], loader.load_skills, session, summary)
            self._ingest_dataset("courses", frames["courses"], loader.load_courses, session, summary)
            self._ingest_dataset("trainers", frames["trainers"], loader.load_trainers, session, summary)
            self._ingest_dataset("trainer_skills", frames["trainer_skills"], loader.load_trainer_skills, session, summary)
            self._ingest_dataset("course_skills", frames["course_skills"], loader.load_course_skills, session, summary)
            loader.commit()
            self.logger.info("Ingestion Complete")
        except Exception as exc:  # noqa: BLE001
            loader.rollback()
            self.logger.exception("Ingestion failed: %s", exc)
            summary["success"] = False
            summary["errors"].append(str(exc))
        finally:
            loader.close()

        return summary

    def _create_schema_and_tables(self, session: Any) -> None:
        session.execute(text("CREATE SCHEMA IF NOT EXISTS core"))
        session.commit()

        from src.models.base import Base
        from src.models.course import Course
        from src.models.course_skill import CourseSkill
        from src.models.skill import Skill
        from src.models.trainer import Trainer
        from src.models.trainer_skill import TrainerSkill

        Base.metadata.create_all(bind=session.get_bind())
        session.commit()

    def _ingest_dataset(
        self,
        name: str,
        dataframe: Any,
        load_method: Any,
        session: Any,
        summary: Dict[str, Any],
    ) -> None:
        try:
            self.logger.info("Loading %s.xlsx", name)
            row_count = len(dataframe)
            self.logger.info("Loaded %s %s", row_count, name)

            inserted = load_method(dataframe)
            self.logger.info("Inserted %s %s", inserted, name)
            summary["results"].append({"name": name, "rows": row_count, "inserted": inserted})
            session.commit()
        except (SQLAlchemyError, ValueError, LookupError, IntegrityError, RuntimeError) as exc:  # type: ignore[name-defined]
            self.logger.exception("Failed to ingest %s: %s", name, exc)
            summary["errors"].append({"name": name, "error": str(exc)})
            summary["success"] = False
            session.rollback()
        except Exception as exc:  # noqa: BLE001
            self.logger.exception("Unexpected failure while ingesting %s: %s", name, exc)
            summary["errors"].append({"name": name, "error": str(exc)})
            summary["success"] = False
            session.rollback()

    def get_summary_report(self) -> Dict[str, Any]:
        return self.run()


class IngestionError(Exception):
    """Raised when ingestion encounters a fatal error."""


IntegrityError = SQLAlchemyError
