from database import Base, SessionLocal, engine


def test_database_objects_exist():
    assert Base is not None
    assert SessionLocal is not None
    assert engine is not None
