# Agentic Training Operations Platform

This project provides a production-style foundation for an agentic training operations platform built with Python 3.12, SQLAlchemy 2.x, PostgreSQL, and a small natural-language assistant layer.

It includes:
- Seed data generation and Excel-based ingestion
- PostgreSQL schema creation and ORM models
- Validation and reporting
- Trainer search and profile access
- Course search and profile access
- Trainer recommendation engine
- Natural-language assistant that routes user questions to existing business services

## Project structure

- data/ - generated seed Excel files and validation reports
- database/ddl/ - PostgreSQL DDL scripts
- src/models/ - SQLAlchemy ORM models
- src/repositories/ - repository layer for database access
- src/services/ - business services for trainers, courses, and recommendations
- src/ai/ - natural-language intent classification, routing, and assistant flow
- scripts/ - runnable demos and utility scripts

## Prerequisites

- Python 3.12
- Docker Desktop or Docker Engine
- PostgreSQL 16 (run via Docker Compose)

## Environment setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start PostgreSQL:

```bash
docker compose up -d postgres
```

4. Confirm the database is available:

```bash
python scripts/test_connection.py
```

## Data pipeline

### Generate seed data

```bash
python generate_seed_data.py
```

### Run ingestion

```bash
python scripts/run_ingestion.py
```

This loads the generated Excel data into PostgreSQL.

### Run validation

```bash
python scripts/run_validation.py
```

This validates the ingested datasets and writes reports under data/reports.

## Search and recommendation demos

### Trainer search demo

```bash
python scripts/trainer_search_demo.py
```

This shows example trainer searches by skill, expert search, availability filtering, and trainer profile lookups.

### Course search demo

```bash
python scripts/course_search_demo.py
```

This demonstrates course search by name, skill-based course lookup, and course profile/skill-requirement retrieval.

### Recommendation demo

```bash
python scripts/recommendation_demo.py
```

This runs the recommendation engine and prints ranked trainer recommendations for a course.

### Natural-language assistant demo

```bash
python scripts/chatbot_demo.py
```

This lets you try natural-language questions such as:
- Who can teach Kubernetes?
- Who are the experts in Kubernetes?
- Show Terraform courses.
- Recommend trainer for CRS004.
- Show profile for TR001.

The assistant classifies the user intent and routes the request through the existing business services.

## Optional: OpenAI-compatible model

The natural-language assistant can optionally use an OpenAI-compatible model if you provide environment variables:

```bash
export OPENAI_API_KEY=your-api-key
export OPENAI_BASE_URL=https://api.openai.com/v1
```

If these are not set, the assistant uses a deterministic local heuristic classifier so the demo still runs without external dependencies.

## Development notes

- The application uses SQLAlchemy 2.x and PostgreSQL.
- The assistant layer never queries the database directly; it routes requests through services.
- For local development, the default database URL is:

```bash
postgresql+psycopg2://postgres:postgres@localhost:5432/training_ops
```

## Summary

You can use this project to:
- generate and load training data
- validate data quality
- search trainers and courses
- recommend trainers for courses
- ask natural-language questions against the platform services
