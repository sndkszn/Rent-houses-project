import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("DB_USER") or os.getenv("POSTGRES_USER", "")
db_password = os.getenv("DB_PASSWORD") or os.getenv("POSTGRES_PASSWORD", "")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT") or os.getenv("POSTGRES_PORT", "5432")
db_name = os.getenv("DB_NAME") or os.getenv("POSTGRES_DB", "")

DEFAULT_LOCAL_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_LOCAL_URL)

engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()