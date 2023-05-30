from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import settings

Base = declarative_base()

engine = None
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if not settings.TEST_MODE:
    engine = create_engine(settings.DB_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def setup_db_conn():
    Base.metadata.create_all(bind=engine)


# Single session dependency
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
