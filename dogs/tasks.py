from celery import shared_task
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, send_mass_mail, EmailMessage
from dogs.models import Dog
from dogs.services import send_telegram_message
from users.models import User


@shared_task
def send_information_about_like(email):
    """ Отправляет сообщение владельцу собаки о поставленном лайке """

    message = 'Вашей собеке поставили лайк'
    send_mail(
        'Новый лайк',
        'Вашей собеке поставили лайк',
        EMAIL_HOST_USER,
        [email]
    )
    """ дополняем функционал отправкой сообщения через tg_bot """
    user = User.objects.get(email=email)
    if user.tg_chat_id:
        send_telegram_message(user.tg_chat_id, message)


@shared_task
def send_mail_about_birthday():
    """ отправляет сообщения о дне рождения собаки через почту и tg """

    today = timezone.now()
    # Нужно написать запрос, который достает из БД всех собак, у которых ДР сегодня.
    # Эту задачу мы сделаем на ежедневной основе, она будет просыпаться 1/день и проверять, нужно ли отправить
    # письмо о ДР собаке.
    # Для этого нужно использовать celery beat, который позволяет регулярно запускать задачи.
    # Напишем такую задачу в tasks.py и добавим ее в celery beat.
    # Проверяем, что у собаки есть хозяин (__isnull=False) и дату рождения
    dogs = Dog.objects.filter(owner__isnull=False, date_born=today)
    # нужно получить emails пользователей, у которых ДР собаки.
    # email_list = []
    email_list_tuple = ()
    message = """У вашей собаки сегодня день рождения.
             Поздравляем!"""
    # если делать без списка, то тогда функция запускалась бы много раз
    for dog in dogs:
        # email_list.append(dog.owner.email)
        email_list_tuple += (dog.owner.email,)
        if dog.owner.tg_chat_id:
            send_telegram_message(dog.owner.tg_chat_id, message)
    if email_list_tuple:
        # send_mass_mail(
        #     'С днем рождения собаки',
        #     """У вашей собаки сегодня день рождения.
        #     Поздравляем!""",
        #     EMAIL_HOST_USER,
        #     [email_list],
        #     fail_silently=True
        # )
        EmailMessage(
            'С днем рождения собаки',
            message,
            EMAIL_HOST_USER,
            [],
            [email_list_tuple],
        ).send(fail_silently=True)
