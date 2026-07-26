from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


class ValidationReport:
    """Write validation results to Excel and JSON reports."""

    def __init__(self, output_dir: str | Path | None = None) -> None:
        self.output_dir = Path(output_dir or Path(__file__).resolve().parents[2] / "data" / "reports")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write(self, validation_results: Dict[str, Any], summary: Dict[str, Any]) -> Dict[str, Path]:
        excel_path = self.output_dir / "validation_report.xlsx"
        json_path = self.output_dir / "validation_summary.json"

        summary_sheet = pd.DataFrame(
            [
                {
                    "Dataset Name": result["name"],
                    "Rows Processed": result["rows"],
                    "Valid Rows": int(result["dataframe"]["__is_valid"].sum()),
                    "Invalid Rows": int(len(result["dataframe"]) - result["dataframe"]["__is_valid"].sum()),
                }
                for result in validation_results
            ]
        )

        errors_sheet = pd.DataFrame(
            [
                {
                    "Dataset": error["dataset"],
                    "Row": error["row"],
                    "Field": error["field"],
                    "Message": error["message"],
                }
                for result in validation_results
                for error in result["errors"]
            ]
        )

        warnings_sheet = pd.DataFrame(columns=["Dataset", "Row", "Field", "Message"])

        stats_sheet = pd.DataFrame(
            [
                {
                    "Dataset": result["name"],
                    "Metric": key,
                    "Value": value,
                }
                for result in validation_results
                for key, value in result["stats"].get("duplicate_counts", {}).items()
            ]
        )
        if stats_sheet.empty:
            stats_sheet = pd.DataFrame(columns=["Dataset", "Metric", "Value"])

        with pd.ExcelWriter(excel_path) as writer:
            summary_sheet.to_excel(writer, sheet_name="Summary", index=False)
            errors_sheet.to_excel(writer, sheet_name="Errors", index=False)
            warnings_sheet.to_excel(writer, sheet_name="Warnings", index=False)
            stats_sheet.to_excel(writer, sheet_name="Statistics", index=False)

        json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        return {"excel": excel_path, "json": json_path}
