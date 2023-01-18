from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api.db import database, db
from api.schemas.quote import QuoteCreate


def create_quote(new_quote: QuoteCreate):
    query = db.quote.insert()
    # values = new_quote.json()
    print(new_quote)
    return new_quote
    # await db.database.execute(query=query, values=values)

    return {"status": 'ok'}


def create_quote(db: Session, new_quote: QuoteCreate):

    db_device = models.Device(**device.dict())
    db_status_code, db_status_detail = database.insert(db, db_device)

    return {"status": db_status_code, "message": db_status_detail, "model": db_device}