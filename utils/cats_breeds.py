import requests
from django.core.cache import cache

from sca.settings import CATS_API_KEY


def get_cats_breeds() -> set[str]:
    if breeds := cache.get("cat_breeds"):
        return breeds
    url = "https://api.thecatapi.com/v1/breeds"
    headers = {"x-api-key": CATS_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        breeds = {breed['name'] for breed in response.json()}
        cache.set("cat_breeds", breeds, timeout=60 * 60)
        return breeds
    raise Exception('Failed to fetch breeds data')
