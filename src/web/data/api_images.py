import copy
import logging
import os
import time
from typing import List

from dotenv import load_dotenv
from pyunsplash import PyUnsplash

log = logging.getLogger("quotes")

load_dotenv()

# API Information
UNSPLASH_ACCESS_KEY = str(os.getenv('UNSPLASH_ACCESS_KEY'))
UNSPLASH_DFT_IMAGE = str(os.getenv('UNSPLASH_DFT_IMAGE', ''))

pu = PyUnsplash(api_key=UNSPLASH_ACCESS_KEY)


def get_image(search: str, count=2):
    try:
        photos = pu.photos(type_='random', count=1, featured=True, query=str(search))

        if not photos:
            return 'unknown', UNSPLASH_DFT_IMAGE

        [photo] = photos.entries
        return photo.id, photo.link_download

    except Exception as err:
        log.warning(f"GET UNSPLASH Image - Error occurred: {type(err).__name__}, Message: {str(err)}")

    return 'unknown', UNSPLASH_DFT_IMAGE


def get_images(search: str, count=2):
    try:
        photos = pu.photos(type_='random', count=count, featured=True, query=search)

        if not photos:
            return [('unknown', UNSPLASH_DFT_IMAGE) for _ in range(count)]

        _photos = [(photo.id, photo.link_download) for photo in photos.entries]
        return _photos

    except Exception as err:
        log.warning(f"GET UNSPLASH Image - Error occurred: {type(err).__name__}, Message: {str(err)}")

    return [('unknown', UNSPLASH_DFT_IMAGE) for _ in range(count)]


def add_images(*, quotes: List[dict], search: str):

    quotes_with_images = copy.deepcopy(quotes)

    for index, _ in enumerate(quotes):
        _, im_url = get_image(search=search)
        quotes_with_images[index]['image'] = im_url
        time.sleep(0.2)

    return quotes_with_images


if __name__ == '__main__':
    print(get_images('Michael Jordan'))
    # print(pu.stats())
