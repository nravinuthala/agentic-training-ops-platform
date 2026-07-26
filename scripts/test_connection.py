from src.database.session import SessionLocal


def main() -> None:
    db = SessionLocal()
    print("Database Connected Successfully")
    db.close()


if __name__ == "__main__":
    main()
