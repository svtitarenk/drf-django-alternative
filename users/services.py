import stripe
import os
from dotenv import load_dotenv
from config import settings
from forex_python.converter import CurrencyRates

load_dotenv()
stripe.api_key = settings.STRIPE_API_KEY


# возьмем сторонний сервис forex-python
def convert_rub_to_usd(amount):
    """ Конвертируем в base_cur (руб)  в dest_cur (доллары) """

    # currency = CurrencyRates()
    # rate = currency.get_rate('RUB', "USD")
    # return int(amount * rate)
    return int(amount * 100)


def create_stripe_price(amount):
    """ Создает цену в stripe """

    return stripe.Price.create(
        # если мы хотим оставить доллары, тогда нужно написать функцию на конвертацию
        # + stripe принимает с центами, поэтому сумму нужно умножать на 100 (amount * 100,)
        currency="usd",
        unit_amount=amount * 100,
        # повторяющихся платежей у нас не будет, поэтому убираем recurring
        # recurring={"interval": "month"},
        product_data={"name": "Donation"},
    )


def create_stripe_session(price):
    """ Создаем сессию в stripe"""

    session = stripe.checkout.Session.create(
        # success_url - куда мы перенаправим пользователя после успешной оплаты.
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
