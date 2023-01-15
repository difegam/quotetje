import pathlib

from fastapi import APIRouter, HTTPException, Path, Query, status

from api.consts import API_VERSION
from api.v1.resources import quotable

route = pathlib.Path(__file__).stem
router = APIRouter(prefix=f"{API_VERSION}/{route}", tags=[str(route)])


@router.get("/author/{author}", status_code=status.HTTP_200_OK)
async def get_quote_by_author(author: str = Path(min_length=3)):
    quote = quotable.get_random_quote('author', [author], 'all')

    if not quote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    return quote.to_dict()


@router.get("/random", status_code=status.HTTP_200_OK)
async def get_random_quote() -> dict:
    quote = quotable.get_quote()

    if not quote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")

    return quote.to_dict()


@router.get("/by/{id}", status_code=status.HTTP_200_OK)
async def get_quote_by_id(id: str = Path(min_length=3)):
    quote = quotable.get_quote(f'quotes/{id}')

    if not quote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found")

    return quote.to_dict()


@router.get("/tags/{tags}", status_code=status.HTTP_200_OK)
async def get_quote_by_tags(tags: str = Path(min_length=3)):
    quote = quotable.get_random_quote('tags', tags.split(','), 'any')

    if not quote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tags not found")

    return quote.to_dict()


@router.get("/authors", status_code=status.HTTP_200_OK)
async def get_quote_authors(limit: int = Query(default=20, gt=0, le=1000)):
    quotes = quotable.get_quotes(limit=limit)

    authors = [quote.author for quote in quotes]

    if not authors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    return authors


@router.get("/", status_code=status.HTTP_200_OK)
async def get_quote(limit: int = Query(default=20, gt=0, le=150)):
    quote = quotable.get_quotes(limit=limit)

    if not quote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    return quote
