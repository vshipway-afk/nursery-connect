from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# This creates a local SQLite file named 'nursery.db' right inside your project folder automatically
SQLALCHEMY_DATABASE_URL = "sqlite:///./nursery.db"

# Note: sqlite requires connect_args for threading, which FastAPI uses
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()