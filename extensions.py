import requests
import json
from config import keys


class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}. Введите целое число.')

        try:
            amount = str(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}. Введите целое число.')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/fc740ee612b30099c9c461c9/pair/{quote_ticker}/{base_ticker}')
        total_base = json.loads(r.content)[keys[base]]