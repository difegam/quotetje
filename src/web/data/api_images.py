import copy
import logging
import os
from functools import lru_cache
from typing import List, Literal

from data import request_handler as rest
from dotenv import load_dotenv

log = logging.getLogger("quotes")

load_dotenv()

# API Information
UNSPLASH_ACCESS_KEY = str(os.getenv('UNSPLASH_ACCESS_KEY'))
UNSPLASH_DFT_IMAGE = str(os.getenv('UNSPLASH_DFT_IMAGE', ''))

UNSPLASH_API_ROOT = "https://api.unsplash.com"
UNSPLASH_HEADERS = {'authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'}


def photos_formatter(photos: List[dict]):
    """Extract id and url from photos retrieved from unsplash api endpoint."""
    _photos = tuple()
    try:
        _photos = [(photo.get('id', ''), photo['urls'].get('regular', UNSPLASH_DFT_IMAGE)) for photo in photos]
    except Exception as err:
        log.warning(f"GET Method - Warning occurred: {type(err).__name__}, Message: {str(err)}")

    return _photos


def search_photos_formatter(photos: dict):
    """pre format unsplash photos retrieved with search type."""
    return photos_formatter(photos.get('results', []))


def get_photos_formatter(type: Literal['search', 'random']):
    """returns the unsplash photo formatter"""

    if type == 'search':
        return search_photos_formatter

    return photos_formatter


@lru_cache(maxsize=15)
def get_unsplash_images(search: str, count=2, _type: Literal['search', 'random'] = 'random'):
    '''Get a list of images from the unsplash api
       - Please visit unsplash api doc: https://unsplash.com/documentation#photos
    '''
    # url and parameters based on search type
    type_endpoint = {
        'random': {
            'endpoint': UNSPLASH_API_ROOT + '/photos/random',
            'headers': UNSPLASH_HEADERS,
            'params': {
                'query': search.replace('%20', '+'),
                'count': count,
                'orientation': 'landscape',
                'w': 1080
            }
        },
        'search': {
            'endpoint': UNSPLASH_API_ROOT + '/search/photos',
            'headers': UNSPLASH_HEADERS,
            'params': {
                'query': search.replace('%20', '+'),
                'per_page': count,
                'orientation': 'landscape',
                'w': 1080,
                'fit': 'max',
                'dpr': 2
            }
        }
    }

    # Get unsplash Photos
    photos = rest._get(**type_endpoint.get(_type, {}))

    # Get a formatter for the data retrieved from the unsplash API.
    photos_formatter = get_photos_formatter(_type)

    return photos_formatter(photos)


def add_images(*, quotes: List[dict] | dict, search: str, _type='random'):
    """
    add images to a quote

    Args:
        quotes (List[dict] | dict): quotes
        search (str): Limit selection to photos matching a search term.
        _type (str, optional): Select Unsplash endpoint random or photos. Defaults to 'random'.
            - search -> https://unsplash.com/documentation#photos
            - search -> https://unsplash.com/documentation#get-a-random-photo

    Returns:
        quotes_with_images: return quotes with and extra key images that contain images url
    """

    quotes_with_images = copy.deepcopy(quotes)
    count = len(quotes_with_images)
    images = get_unsplash_images(search=search, count=count)

    if not images:
        log.warning(f"Error retrieving and adding images")
        return quotes

    for index, _ in enumerate(images):
        _, im_url = images[index]
        quotes_with_images[index]['image'] = im_url

    return quotes_with_images


if __name__ == '__main__':
    ...