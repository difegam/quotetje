from dataclasses import asdict, dataclass, field
from typing import List, Literal
from urllib.parse import urljoin

import api.v1.resources.request_handler as rest_conn

# import request_handler as rest_conn

base_url = "https://api.quotable.io"


def quote_source() -> str:
    return base_url or 'Unknown'


@dataclass()
class Quote:
    id: str = ''
    content: str = ''
    author: str = ''
    tags: List[str] = field(default_factory=list)
    length: int = 0
    source: str = field(default_factory=quote_source)

    def __repr__(self):
        return f"<Quote(id='{self.id}', content='{self.content}', author='{self.author}', tags={self.tags}, length={self.length}, source='{self.source}')>"

    def __bool__(self):
        return bool(self.content)

    def to_dict(self):
        return asdict(self)


def quote_formatter(quotable_quote: dict) -> List[Quote]:

    if not quotable_quote or not isinstance(quotable_quote, dict) and 'results' not in quotable_quote:
        return []

    # multiple quotes
    raw_quotes = [get_quote_object(quote) for quote in quotable_quote.get('results', [])]
    quotes = [quote for quote in raw_quotes if quote]

    return quotes


def get_quote_object(quote: dict):

    if not quote:
        return Quote()

    params = {
        'id': quote.get('_id', 0),
        'content': quote.get('content', ''),
        'author': quote.get('author', ''),
        'tags': quote.get('tags', []),
        'length': quote.get('length', [])
    }

    if not all(list(params.values())):
        return Quote()

    return Quote(**params)


def get_quote(quote_type: str = 'random', qry: dict | None = None) -> Quote:
    url = urljoin(base_url, quote_type)
    return get_quote_object(rest_conn._get(endpoint=url, params=qry, timeout=6))


def get_quotes(quote_type: str = 'quotes', qry: dict | None = None, limit=20) -> List[Quote]:
    url = urljoin(base_url, quote_type)
    qry_params = {'limit': limit}

    if qry:
        qry_params.update(qry)

    return quote_formatter(rest_conn._get(endpoint=url, params=qry_params, timeout=6))


def get_random_quote(by: Literal['tags', 'author'], qry_params: List[str], restriction: Literal['all', 'any'] = 'any'):

    if restriction == "all":
        sep = ','
    elif restriction == "any":
        sep = '|'
    else:
        return Quote()

    qry_tags = {by: sep.join(qry_params)} if qry_params else None
    return get_quote(qry=qry_tags)


# if __name__ == '__main__':
#     print('hello world')
#     # print(get_quote())
#     print(get_random_quote('tags', ['friendship', 'self-help'], 'any'))
#     # print(get_random_quote('author', ['Babe Ruth', 'Muhammad Ali'], 'all'))
#     # qs = get_quotes()
#     # print(qs)
