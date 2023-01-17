import logging
from typing import Dict

import requests
from requests.exceptions import HTTPError

log = logging.getLogger("quotes")

# A few handy JSON types
JSON = int | str | float | bool | None | dict[str, "JSON"] | list["JSON"]
JSONObject = dict[str, JSON]
JSONList = list[JSON]

__all__ = ['_get']


def _get(*, endpoint: str, headers: Dict[str, str] | None = None, params: dict | None = None, timeout=6) -> JSONObject:
    """
    requests get wrapper for data validation and error handling.

    Args:
        endpoint (str): api endpoint
        headers (Dict[str, str] | None, optional). Defaults to None.
        params (dict | None, optional): Query parameters. {'parameter': value }Defaults to None.
        timeout (int, optional). Defaults to 10.

    Returns:
        JSONObject: _description_
    """

    if not params:
        params = dict()

    if not headers:
        headers = dict()

    request_response: JSONObject = {}

    if not endpoint:
        return request_response

    try:

        response = requests.get(endpoint, params, headers=headers, timeout=timeout)

        # raise exception response is not success
        response.raise_for_status()

        request_response = response.json()

        log.debug(f"endpoint url: {response.url}")

    except HTTPError as http_err:
        log.error(f"GET Method - HTTP error occurred: {type(http_err).__name__}, Message: {str(http_err)}")

    except Exception as err:
        log.warning(f"GET Method - Warning occurred: {type(err).__name__}, Message: {str(err)}")

    return request_response