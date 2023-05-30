import pytest
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from database.entity.base_entity import Base, get_db_session
from main import app

db = factories.postgresql_proc(
    port=None, dbname="test_db", load=["tests/api/schema_def.sql"]
)


@pytest.fixture(scope="function")
def db_session(db):
    host = db.host
    port = db.port
    user = db.user
    password = db.password
    dbname = db.dbname

    with DatabaseJanitor(user, host, port, dbname, db.version, password):
        conn_url = (
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
        )
        engine = create_engine(conn_url)
        with engine.connect() as connection:
            Base.metadata.create_all(connection)
            yield sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def override_db(request, db_session):
    def test_session():
        test_db = db_session()
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db_session] = test_session

    def teardown():
        app.dependency_overrides = {}

    request.addfinalizer(teardown)
