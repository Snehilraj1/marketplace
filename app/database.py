from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings

# 1. Encode the password as a standalone statement
encoded_password = quote_plus(settings.database_password)

# 2. Build the connection string cleanly
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{settings.database_username}:{encoded_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()