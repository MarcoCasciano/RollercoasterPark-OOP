import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.app import app
from app.db.base import Base
from app.db.database import get_db
from app.db.models import attrazione, famiglia, visitatore, giro  # noqa: F401


engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def attrazione_data():
    return {
        "nome": "Montagne Russe",
        "per_bambini": False,
        "capienza_massima": 10,
        "durata_giro": 3,
        "posizione_x": 1.0,
        "posizione_y": 2.0,
    }


@pytest.fixture()
def famiglia_data():
    return {
        "cognome": "Rossi",
        "num_adulti": 2,
        "num_bambini": 1,
        "num_ragazzi": 1,
    }


@pytest.fixture()
def visitatore_data():
    return {
        "nome": "Marco",
        "cognome": "Rossi",
        "tipo": "adulto",
        "posizione_x": 0,
        "posizione_y": 0,
    }


@pytest.fixture()
def giro_data():
    return {
        "ciclo": 1,
    }
