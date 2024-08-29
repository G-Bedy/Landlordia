from datetime import date

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from realestate.models import LeaseContract


@shared_task
def send_contract_email(tenant_email, contract_details):
    """
    Отправляет арендатору электронное письмо с деталями договора аренды.
    """
    send_mail(
        'Договор аренды',
        f'Уважаемый арендатор, ваш договор аренды: {contract_details}',
        settings.DEFAULT_FROM_EMAIL,
        [tenant_email],
        fail_silently=True,
    )


@shared_task
def check_and_send_payment_reminders():
    """
    Проверяет даты платежа и отправляет напоминания арендаторам.
    После обновляет дату следующего платежа.
    """
    today = date.today()
    lease_contracts = LeaseContract.objects.filter(next_payment_date__date=today)

    for contract in lease_contracts:
        tenant_email = contract.tenant.email
        payment_details = f"Сумма аренды: {contract.rent_amount} за {contract.rent_period}"
        send_payment_email.delay(tenant_email, payment_details)
        contract.update_next_payment_date()


@shared_task
def send_payment_email(tenant_email, payment_details):
    """
    Отправляет арендатору электронное письмо с напоминанием об оплате.
    """
    send_mail(
        'Платеж за аренду',
        f'Уважаемый арендатор, пришло время следующего платежа: {payment_details}',
        settings.DEFAULT_FROM_EMAIL,
        [tenant_email],
        fail_silently=True,
    )
