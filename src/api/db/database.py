import logging
import os
import sys
from typing import Any, Tuple

from dotenv import load_dotenv
from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

__all__ = ['get_db', 'insert', 'select_all', 'get_by_id', 'select_one', 'update', 'delete']

# Logging tools
_LOGGER: logging.Logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format="[%(asctime)s | %(levelname)s] %(module)-2s:%(funcName)-2s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

# load environment variables
load_dotenv()

SQLALCHEMY_DATABASE_URL = str(os.getenv('DB_PATH'))
if not SQLALCHEMY_DATABASE_URL:
    _LOGGER.error(f"DB Connection URL string is not defined. env DB_PATH: {SQLALCHEMY_DATABASE_URL}")

try:

    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()

except exc.SQLAlchemyError as e:
    _LOGGER.error(
        f"SQLAlchemy DB Connection Error:  {type(e).__name__}, Exception Message: {str(e)}, SQLAlchemy DB URL: {SQLALCHEMY_DATABASE_URL}"
    )
    sys.exit()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def insert(db: Session, db_model):
    status_code, status_msg = (100, 'record insert not done')

    try:
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        status_code, status_msg = (200, f"{db_model.__tablename__} record created")

    except exc.SQLAlchemyError as e:
        db.rollback()
        status_code, status_msg = (422, "Unprocessable Entity")
        _LOGGER.error(
            f"SQLAlchemy Create Error:  {type(e).__name__}, Exception Message: {str(e)}, Model: {db_model.__tablename__}"
        )

    finally:
        db.close()
        return status_code, status_msg


def select_all(db: Session, db_model, skip: int, limit: int):

    result = []
    try:
        result = db.query(db_model).offset(skip).limit(limit).all()

    except exc.SQLAlchemyError as e:
        # rolling back the transaction if any errors occur
        db.rollback()
        _LOGGER.error(
            f"SQLAlchemy Select all Error:  {type(e).__name__}, Exception Message: {str(e)}, Model: {db_model.__tablename__}"
        )

    finally:
        return result


def get_by_id(db: Session, db_model, _id: int):

    result = None

    if not _id or _id < 0:
        return result

    try:
        result = db.query(db_model).get(_id)

    except exc.SQLAlchemyError as e:
        # rolling back the transaction if any errors occur
        _LOGGER.error(
            f"SQLAlchemy Get by ID Error:  {type(e).__name__}, Exception Message: {str(e)}, Model: {db_model.__tablename__}"
        )

    finally:
        return result


def select_one(db: Session, db_model, query_args: Tuple[Any, Any]):

    result = None

    if not query_args and len(query_args) < 2:
        return result

    try:
        result = db.query(db_model).filter(query_args[0] == query_args[1]).first()

    except exc.SQLAlchemyError as e:
        _LOGGER.error(
            f"SQLAlchemy Select all Error:  {type(e).__name__}, Exception Message: {str(e)}, Model: {db_model.__tablename__}"
        )

    finally:
        return result


def update(db: Session, db_model, query_args: Tuple[Any, Any], changes: dict) -> Tuple[int, str]:

    result = False

    status_code, status_msg = (422, 'insufficient number of arguments')
    if not query_args and len(query_args) < 2:
        return status_code, status_msg

    try:
        result = db.query(db_model).filter(query_args[0] == query_args[1]).update(changes, synchronize_session=False)

        #  No matches
        if not result:
            status_code, status_msg = (404, "record does not exists")
            return status_code, status_msg

        db.commit()
        status_code, status_msg = (200, "record updated")

    except exc.SQLAlchemyError as e:
        # rolling back the transaction if any errors occur
        db.rollback()
        status_code, status_msg = (500, "Unprocessable Entity")
        _LOGGER.error(
            f"SQLAlchemy Update Error:  {type(e).__name__}, Exception Message: {str(e)}, Model: {db_model.__tablename__}"
        )

    finally:
        db.close()
        return status_code, status_msg


def delete(db: Session, db_model, query_args: Tuple[Any, Any]) -> Tuple[int, str]:

    result = False

    status_code, status_msg = (422, 'insufficient number of arguments')
    if not query_args and len(query_args) < 2:
        return status_code, status_msg

    try:
        result = db.query(db_model).filter(query_args[0] == query_args[1]).first()

        #  No matches
        if not result:
            status_code, status_msg = (404, "record does not exists")
            return status_code, status_msg

        db.delete(result)
        db.commit()
        status_code, status_msg = (200, "record updated")

    except exc.SQLAlchemyError as e:
        # rolling back the transaction if any errors occur
        db.rollback()
        status_code, status_msg = (500, "Unprocessable Entity")
        _LOGGER.error(
            f"SQLAlchemy Update Error:  {type(e).__name__}, Exception Message: {str(e)}, Model: {db_model.__tablename__}"
        )

    finally:
        db.close()
        return status_code, status_msg


if __name__ == "__main__":

    # Data base connection - testing
    from sqlalchemy import text

    with engine.connect() as connection:
        result = connection.execute(text("select * from configs"))
        print(result)
