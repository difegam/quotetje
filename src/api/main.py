from fastapi import FastAPI

from api import home, ping
from api.consts import API_DESCRIPTION, API_TITLE, API_VERSION_NUMBER
from api.db.db import create_tables, database
from api.v1.routes import quotes

app = FastAPI(title=API_TITLE, description=API_DESCRIPTION, version=API_VERSION_NUMBER)

# Create tables
create_tables()

# API Routes (endpoints)
api_routes = {ping, home, quotes}

# Add api routes
for api_router in api_routes:
    app.include_router(api_router.router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
