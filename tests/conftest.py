import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError
from sqlalchemy.pool import StaticPool
from app import create_app
from app import db


def pytest_addoption(parser):
    parser.addoption(
        "--dburl",  # For Postgres use "postgresql://user:password@localhost/dbname"
        action="store",
        default="sqlite:///:memory:",  # Default uses SQLite in-memory database
        help="Database URL to use for tests.",
    )


@pytest.fixture(scope="session")
def db_url(request):
    """Fixture to retrieve the database URL."""
    return request.config.getoption("--dburl")


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    db_url = session.config.getoption("--dburl")
    try:
        # Attempt to create an engine and connect to the database.
        engine = create_engine(
            db_url,
            poolclass=StaticPool,
        )
        connection = engine.connect()
        connection.close()  # Close the connection right after a successful connect.
        print("Using Database URL:", db_url)
        print("Database connection successful.....")
    except SQLAlchemyOperationalError as e:
        print(f"Failed to connect to the database at {db_url}: {e}")
        pytest.exit(
            "Stopping tests because database connection could not be established."
        )


@pytest.fixture(scope="session")
def app(db_url):
    # Using conf_test file for tests, with db sqlite in memory
    app = create_app('conf_test')

    with app.app_context():
        db.create_all()
        yield app

        # Close the database session and drop all tables after the session
        db.session.remove()
        db.drop_all()
        print("Destroying Database")
        print("Database disconnected successful.....")


@pytest.fixture
def client(app):
    """Test client for the app."""
    return app.test_client()


@pytest.fixture
def user_payload():
    return {
        "name": "test",
        "email": "test@example.com",
        "password": "123456",
        "confirm": "123456"
    }

@pytest.fixture
def user_login():
    return {
        "email": "test@example.com",
        "password": "123456",
    }    