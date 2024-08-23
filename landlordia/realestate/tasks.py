from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_contract_email(tenant_email, contract_details):
    send_mail(
        'Договор аренды',
        f'Уважаемый арендатор, ваш договор аренды: {contract_details}',
        'bedy2bedy@gmail.com',
        [tenant_email],
        fail_silently=True,
    )
