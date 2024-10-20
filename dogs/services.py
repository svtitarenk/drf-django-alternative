import requests
from config import settings


def send_telegram_message(chat_id, message):
    """ Функция отправки сообщения в ТГ бот """

    params = {
        'text': message,
        'chat_id': chat_id
    }
    response = requests.get(f'{settings.TELEGRAM_URL}{settings.TG_BOT_TOKEN}/sendMessage', params=params)
    if response.status_code != 200:
        raise Exception(f'Failed to send Telegram message: {response.text}')
