from urllib.parse import urljoin

import data.request_handler as rest_conn

# import request_handler as rest_conn

base_url = "http://quotes-api:8831/api/v1/"


def quote_source() -> str:
    return base_url or 'Unknown'


def get_quote(quote_type: str = 'quotes/random', qry: dict | None = None) -> dict:
    url = urljoin(base_url, quote_type)
    return rest_conn._get(endpoint=url, params=qry, timeout=6)


def get_author_quotes(quote_type: str = 'quotes/author', qry: dict | None = None, sub_url: str = '') -> dict:
    url = urljoin(base_url, quote_type)

    if sub_url:
        url = urljoin(url, sub_url)

    return rest_conn._get(endpoint=url, params=qry, timeout=6)


def get_quotes(quote_type: str = 'quotes', qry: dict | None = None) -> dict:
    url = urljoin(base_url, quote_type)
    return rest_conn._get(endpoint=url, params=qry, timeout=6)


if __name__ == '__main__':
    print('hello world')
    print(get_quote())
