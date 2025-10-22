import requests

from environs import Env

from pprint import pprint

env = Env()
env.read_env()


def get_supported_currencies() -> list[list[str]]:
    api_key = env.str('RATE_API_KEY')
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/codes'
    r = requests.get(url)
    return r.json()['supported_codes']


pprint(get_supported_currencies())