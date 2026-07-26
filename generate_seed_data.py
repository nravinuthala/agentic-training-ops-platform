#!/usr/bin/env python3
"""Generate realistic seed datasets for the EdTech training operations platform."""

from __future__ import annotations

import random
from pathlib import Path
from typing import List

import pandas as pd


RANDOM_SEED = 42


def generate_trainers(output_path: Path, count: int = 50) -> pd.DataFrame:
    """Generate trainer records with realistic names, emails, and availability."""
    random.seed(RANDOM_SEED)

    first_names = [
        "Aarav",
        "Anika",
        "Arjun",
        "Bhavya",
        "Chaitanya",
        "Deepa",
        "Diya",
        "Esha",
        "Harini",
        "Ishaan",
        "Jaya",
        "Kavya",
        "Krish",
        "Meera",
        "Nikhil",
        "Pooja",
        "Pranav",
        "Rhea",
        "Rohan",
        "Saanvi",
        "Sanjay",
        "Sanya",
        "Shreya",
        "Siddharth",
        "Tanvi",
        "Varun",
        "Vikram",
        "Yash",
        "Zara",
    ]
    last_names = [
        "Agarwal",
        "Bhatia",
        "Chopra",
        "Desai",
        "Gupta",
        "Iyer",
        "Jain",
        "Kapoor",
        "Kulkarni",
        "Malhotra",
        "Mehta",
        "Nair",
        "Patel",
        "Reddy",
        "Sharma",
        "Singh",
        "Soni",
        "Tiwari",
        "Verma",
        "Yadav",
    ]
    locations = [
        "New York",
        "London",
        "Singapore",
        "Toronto",
        "Sydney",
        "Dubai",
        "Amsterdam",
        "Bengaluru",
        "Chicago",
        "Berlin",
    ]
    statuses = ["Active", "On Leave", "Inactive"]

    trainers = []
    for index in range(1, count + 1):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        trainers.append(
            {
                "trainer_code": f"TR{index:03d}",
                "trainer_name": f"{first_name} {last_name}",
                "email": f"{first_name.lower()}.{last_name.lower()}{index}@example.com",
                "experience_years": random.randint(3, 20),
                "primary_location": random.choice(locations),
                "availability_percentage": random.randint(40, 95),
                "status": random.choice(statuses),
            }
        )

    dataframe = pd.DataFrame(trainers)
    dataframe.to_excel(output_path, index=False)
    return dataframe


def generate_skills(output_path: Path, count: int = 100) -> pd.DataFrame:
    """Generate a rich skill catalog aligned to technology domains."""
    skill_templates = {
        "Cloud": [
            "AWS Fundamentals",
            "Azure Architecture",
            "Google Cloud Platform",
            "Kubernetes",
            "Terraform",
            "Cloud Security",
        ],
        "DevOps": [
            "CI/CD Pipelines",
            "GitOps",
            "Docker",
            "Ansible",
            "Jenkins",
            "Release Management",
        ],
        "Data Engineering": [
            "ETL/ELT",
            "Spark",
            "Data Modeling",
            "Delta Lake",
            "Airflow",
            "Warehouse Design",
        ],
        "AI/ML": [
            "Machine Learning",
            "Deep Learning",
            "Natural Language Processing",
            "Computer Vision",
            "MLOps",
            "Prompt Engineering",
        ],
        "Programming": [
            "Python",
            "Java",
            "Go",
            "C#",
            "JavaScript",
            "TypeScript",
            "SQL",
            "Scala",
        ],
        "Security": [
            "Identity and Access Management",
            "Threat Modeling",
            "Application Security",
            "Security Automation",
            "Compliance",
        ],
        "Observability": [
            "Monitoring",
            "Logging",
            "Tracing",
            "Metrics",
            "Incident Management",
            "SRE Practices",
        ],
    }

    skills: List[dict[str, object]] = []
    for category, names in skill_templates.items():
        for name in names:
            skills.append(
                {
                    "skill_code": f"SK{len(skills) + 1:03d}",
                    "skill_name": name,
                    "skill_category": category,
                }
            )

    while len(skills) < count:
        category = random.choice(list(skill_templates.keys()))
        skill_name = f"{category} Specialty {len(skills) + 1}"
        skills.append(
            {
                "skill_code": f"SK{len(skills) + 1:03d}",
                "skill_name": skill_name,
                "skill_category": category,
            }
        )

    dataframe = pd.DataFrame(skills[:count])
    dataframe.to_excel(output_path, index=False)
    return dataframe


def generate_courses(output_path: Path, count: int = 50) -> pd.DataFrame:
    """Generate course catalog entries with varied durations and technology areas."""
    random.seed(RANDOM_SEED + 1)

    course_templates = [
        ("Cloud Foundations", 5, "Beginner", "Cloud"),
        ("Advanced Kubernetes Operations", 10, "Intermediate", "Cloud"),
        ("Azure Solution Design", 7, "Advanced", "Cloud"),
        ("AWS Platform Engineering", 14, "Advanced", "Cloud"),
        ("DevOps Engineering Essentials", 6, "Beginner", "DevOps"),
        ("CI/CD Automation", 8, "Intermediate", "DevOps"),
        ("Platform Reliability", 12, "Advanced", "DevOps"),
        ("Data Pipelines with Spark", 9, "Intermediate", "Data Engineering"),
        ("Modern Data Warehouse Design", 11, "Advanced", "Data Engineering"),
        ("Streaming Data Platforms", 10, "Advanced", "Data Engineering"),
        ("Applied Machine Learning", 8, "Intermediate", "AI/ML"),
        ("Deep Learning for Practitioners", 12, "Advanced", "AI/ML"),
        ("MLOps Foundations", 7, "Intermediate", "AI/ML"),
        ("Secure Python Development", 6, "Intermediate", "Programming"),
        ("Modern Java Applications", 8, "Intermediate", "Programming"),
        ("Go for Cloud Native Development", 7, "Intermediate", "Programming"),
        ("Application Security Bootcamp", 6, "Intermediate", "Security"),
        ("Threat Modeling Workshop", 5, "Beginner", "Security"),
        ("Cloud Security Architecture", 9, "Advanced", "Security"),
        ("SRE and Observability", 8, "Intermediate", "Observability"),
        ("Distributed Tracing", 6, "Advanced", "Observability"),
        ("Service Monitoring at Scale", 7, "Intermediate", "Observability"),
    ]

    rows = []
    for index in range(1, count + 1):
        course_name, duration_days, level, technology_area = course_templates[(index - 1) % len(course_templates)]
        if index > len(course_templates):
            course_name = f"{course_name} - Module {index}"
        rows.append(
            {
                "course_code": f"CR{index:03d}",
                "course_name": course_name,
                "duration_days": duration_days + ((index - 1) % 3),
                "level": level,
                "technology_area": technology_area,
            }
        )

    dataframe = pd.DataFrame(rows)
    dataframe.to_excel(output_path, index=False)
    return dataframe


def generate_trainer_skills(output_path: Path, trainers: pd.DataFrame, skills: pd.DataFrame) -> pd.DataFrame:
    """Generate realistic trainer-skill proficiency mappings."""
    random.seed(RANDOM_SEED + 2)

    proficiency_levels = ["Beginner", "Intermediate", "Advanced", "Expert"]
    rows: List[dict[str, object]] = []

    for trainer in trainers.itertuples(index=False):
        trainer_skills = random.sample(list(skills["skill_code"]), k=random.randint(5, 15))
        for skill_code in trainer_skills:
            rows.append(
                {
                    "trainer_code": trainer.trainer_code,
                    "skill_code": skill_code,
                    "proficiency": random.choice(proficiency_levels),
                }
            )

    dataframe = pd.DataFrame(rows)
    dataframe.to_excel(output_path, index=False)
    return dataframe


def generate_course_skills(output_path: Path, courses: pd.DataFrame, skills: pd.DataFrame) -> pd.DataFrame:
    """Generate realistic course-skill importance mappings."""
    random.seed(RANDOM_SEED + 3)

    importance_levels = ["Mandatory", "Recommended"]
    rows: List[dict[str, object]] = []

    for course in courses.itertuples(index=False):
        required_skills = random.sample(list(skills["skill_code"]), k=random.randint(3, 8))
        for skill_code in required_skills:
            rows.append(
                {
                    "course_code": course.course_code,
                    "skill_code": skill_code,
                    "importance": random.choice(importance_levels),
                }
            )

    dataframe = pd.DataFrame(rows)
    dataframe.to_excel(output_path, index=False)
    return dataframe


def generate_all_datasets(output_dir: str | Path | None = None) -> List[Path]:
    """Create all requested Excel files under the given output directory."""
    output_dir = Path(output_dir or Path(__file__).resolve().parent / "data")
    output_dir.mkdir(parents=True, exist_ok=True)

    file_paths = [
        output_dir / "trainers.xlsx",
        output_dir / "skills.xlsx",
        output_dir / "courses.xlsx",
        output_dir / "trainer_skills.xlsx",
        output_dir / "course_skills.xlsx",
    ]

    generate_trainers(file_paths[0])
    generate_skills(file_paths[1])
    generate_courses(file_paths[2])
    generate_trainer_skills(file_paths[3], generate_trainers(file_paths[0]), generate_skills(file_paths[1]))
    generate_course_skills(file_paths[4], generate_courses(file_paths[2]), generate_skills(file_paths[1]))

    return file_paths


def main() -> None:
    """Entry point for generating the seed data package."""
    generated_files = generate_all_datasets()
    print("Created Excel files:")
    for file_path in generated_files:
        print(f"- {file_path}")


if __name__ == "__main__":
    main()
