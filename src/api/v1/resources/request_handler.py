import logging

import requests
from requests.exceptions import HTTPError

log = logging.getLogger("quotes")

# A few handy JSON types
JSON = int | str | float | bool | None | dict[str, "JSON"] | list["JSON"]
JSONObject = dict[str, JSON]
JSONList = list[JSON]

__all__ = ['_get']


def _get(*, endpoint: str, params: dict | None = None, timeout=10) -> JSONObject:

    if not params:
        params = dict()

    request_response: JSONObject = {}

    if not endpoint:
        return request_response

    try:

        response = requests.get(endpoint, params, timeout=timeout)

        # raise exception response is not success
        response.raise_for_status()

        request_response = response.json()

    except HTTPError as http_err:
        log.error(f"GET Method - HTTP error occurred: {type(http_err).__name__}, Message: {str(http_err)}")

    except Exception as err:
        log.warning(f"GET Method - Warning occurred: {type(err).__name__}, Message: {str(err)}")

    return request_response