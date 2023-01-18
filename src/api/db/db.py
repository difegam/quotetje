import sys

from databases import Database
from sqlalchemy import (ARRAY, Column, DateTime, ForeignKey, ForeignKeyConstraint, Integer, MetaData, String, Table,
                        create_engine)
from sqlalchemy.sql import func

from api.shared import DB_CONNECTION_STRING, logger


class InvalidConnectionStringException(Exception):
    "Raised when the connection string is not valid"
    ...


# SQLAlchemy
try:
    if not DB_CONNECTION_STRING:
        raise InvalidConnectionStringException("Invalid connection string. Connection is empty.")

    engine = create_engine(DB_CONNECTION_STRING)
    metadata = MetaData()

except InvalidConnectionStringException as db_conn_err:
    logger.warning(f"Database connection problem occurred: {type(db_conn_err).__name__}, Message: {str(db_conn_err)}")
    sys.exit()
except Exception as err:
    logger.warning(f"Database problem occurred: {type(err).__name__}, Message: {str(err)}")

quote = Table(
    "quote",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("quote_id", String, unique=True, nullable=False, index=True),
    Column("content", String),
    Column("author", String(60)),
    Column("tags", ARRAY(String)),
    Column("length", Integer),
    Column("created_at", DateTime(timezone=False), server_default=func.now()),
    Column("updated_at", DateTime(timezone=False), server_default=func.now(), onupdate=func.now()),
    Column("likes", Integer, ForeignKey("like.id")),
)

like = Table(
    "like",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("likes", Integer),
    Column("dislikes", Integer),
    Column("quote_id", Integer),
    ForeignKeyConstraint(["quote_id"], ["quote.id"], name="fk_like_quote_id"),
)


def create_tables():

    try:
        metadata.create_all(engine)
    except Exception as e:
        logger.error(f"Error On Tables Create - {type(e).__name__}, Message: {str(e)}")


# databases query builder
database = Database(DB_CONNECTION_STRING)

# https://www.encode.io/databases/
# https://www.encode.io/databases/database_queries/