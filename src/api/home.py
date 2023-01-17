from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

# (Welcome page, API is running)
templates = Jinja2Templates(directory="api/views/templates/")


@router.get("/", tags=["root"])
async def root(request: Request):
    message = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return templates.TemplateResponse('index.html',
                                      context={
                                          'request': request,
                                          "client_host": request.url._url,
                                          'message': message
                                      })