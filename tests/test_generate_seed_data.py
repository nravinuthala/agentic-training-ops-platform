from pathlib import Path

from generate_seed_data import generate_all_datasets


def test_generate_all_datasets_creates_expected_excel_files(tmp_path: Path) -> None:
    output_dir = tmp_path / "data"

    generated_files = generate_all_datasets(output_dir=output_dir)

    assert generated_files == [
        output_dir / "trainers.xlsx",
        output_dir / "skills.xlsx",
        output_dir / "courses.xlsx",
        output_dir / "trainer_skills.xlsx",
        output_dir / "course_skills.xlsx",
    ]

    for file_path in generated_files:
        assert file_path.exists(), f"Expected file was not created: {file_path}"

    assert output_dir.joinpath("trainers.xlsx").stat().st_size > 0
    assert output_dir.joinpath("skills.xlsx").stat().st_size > 0
    assert output_dir.joinpath("courses.xlsx").stat().st_size > 0
    assert output_dir.joinpath("trainer_skills.xlsx").stat().st_size > 0
    assert output_dir.joinpath("course_skills.xlsx").stat().st_size > 0
