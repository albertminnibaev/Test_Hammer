import os

import requests


SMS_KEY = os.getenv('SMS_KEY')
EMAIL = os.getenv('EMAIL')


def send_sms(phone_number, code):
    data = {
        'number': phone_number,
        'sign': 'SMS Aero',
        'text': code
    }

    try:
        requests.post(f"https://{EMAIL}:{SMS_KEY}@gate.smsaero.ru/v2/sms/send", data=data)
    except Exception:
        raise Exception(f"Ошибка отправки сообщения пользователю {phone_number}")
