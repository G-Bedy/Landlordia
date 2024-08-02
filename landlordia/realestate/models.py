from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


class Owner(models.Model):
    """
    Модель Owner, создание собственника недвижимости.

    Атрибуты:
        user (OneToOneField): Связь один-к-одному с моделью User.
        phone_number (CharField): Номер телефона владельца (необязательное поле).
        address (CharField): Адрес владельца (необязательное поле).
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


class Property(models.Model):
    """
    Модель Property, создание объекта недвижимости, принадлежащей собственнику.

    Атрибуты:
        owner (ForeignKey): Владелец недвижимости, связь с моделью Owner.
        address (CharField): Адрес недвижимости.
        property_type (CharField): Тип недвижимости (квартира, дом, коммерческая недвижимость, земельный участок).
        description (TextField): Описание недвижимости (необязательное поле).
        purchase_date (DateField): Дата покупки недвижимости.
        price (DecimalField): Стоимость аренды.
        price_period (CharField): Период аренды (часы, сутки, месяц).
        rental_type (CharField): Признак сдачи недвижимости (почасовая, посуточная, длительная аренда).
        minimum_rental_value (IntegerField): Значение минимального периода сдачи.
        minimum_rental_unit (CharField): Единица измерения минимального периода сдачи (часы, дни, месяцы).
    """
    PROPERTY_TYPE_CHOICES = [
        ('Apartment', 'Квартира'),
        ('House', 'Дом'),
        ('Commercial', 'Коммерческая недвижимость'),
        ('Land', 'Земельный участок')
    ]

    PERIOD_CHOICES = [
        ('Hour', 'в час'),
        ('Day', 'в сутки'),
        ('Month', 'в месяц')
    ]

    RENTAL_TYPE_CHOICES = [
        ('Hourly', 'Почасовая аренда'),
        ('Daily', 'Посуточная аренда'),
        ('LongTerm', 'Длительная аренда')
    ]

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    description = models.TextField(blank=True)
    rental_type = models.CharField(max_length=20, choices=RENTAL_TYPE_CHOICES,
                                   help_text=("Тип ренты (почасовая, посуточная, длительная аренда)"))
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text=("Стоимость аренды"))
    price_period = models.CharField(max_length=20, choices=PERIOD_CHOICES,
                                    help_text=("Стоимость за период: в час, в сутки или в месяц"))
    minimum_rental_value = models.IntegerField(help_text=("Минимальный период сдачи"))
    minimum_rental_unit = models.CharField(max_length=5,
                                           choices=PERIOD_CHOICES,
                                           help_text=(
                                               "Единица измерения минимального периода сдачи (часы, дни, месяцы)")
                                           )

    def __str__(self):
        return f"{self.owner} - {self.property_type} - {self.address}"


class Tenant(models.Model):
    """
    Модель Tenant (Арендатор), создание объекта арендатора.

    Атрибуты:
        first_name (CharField): Имя арендатора.
        last_name (CharField): Фамилия арендатора.
        email (EmailField): Электронная почта арендатора.
        phone_number (CharField): Номер телефона арендатора (необязательное поле).
        address (CharField): Адрес арендатора (необязательное поле).
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class LeaseContract(models.Model):
    """
    Модель LeaseContract, создание договора аренды недвижимости.

    Атрибуты:
        property (ForeignKey): Ссылка на арендуемую недвижимость.
        tenant (ForeignKey): Ссылка на арендатора.
        start_date (DateField): Дата начала аренды.
        end_date (DateField): Дата окончания аренды.
        rent_amount (DecimalField): Сумма аренды.
        rent_period (CharField): Период аренды (часы, сутки, месяцы).
        deposit_amount (DecimalField): Сумма депозита (необязательное поле).
    """
    PERIOD_CHOICES = [
        ('Hour', 'Час'),
        ('Day', 'Сутки'),
        ('Month', 'Месяц')
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, help_text=("Арендуемая недвижимость"))
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, help_text=("Арендатор"))
    start_date = models.DateField(help_text=("Дата начала аренды"))
    end_date = models.DateField(help_text=("Дата окончания аренды"))
    rent_amount = models.IntegerField(help_text=("Сумма аренды"))
    rent_period = models.CharField(max_length=20, choices=PERIOD_CHOICES, help_text=("Период аренды (часы, сутки, месяцы)"))
    deposit_amount = models.IntegerField(blank=True, null=True, help_text=("Сумма депозита (необязательное поле)"))

    def clean(self):
        """
        Валидация дат начала и окончания аренды.
        """
        if self.end_date < self.start_date:
            raise ValidationError("Дата окончания аренды не может быть раньше даты начала аренды")

    def __str__(self):
        return f"Договор аренды недвижимости по адресу: {self.property.address} с {self.start_date} по {self.end_date}, {self.rent_amount} рублей за {self.rent_period}, арендатор {self.tenant.first_name}"


class Payment(models.Model):
    """
    Модель Payment, платежи по договору аренды.

    Атрибуты:
        lease (ForeignKey): Связь с моделью Lease, представляющая договор аренды, по которому осуществляется платеж.
        amount (DecimalField): Сумма платежа.
        payment_date (DateField): Дата совершения платежа.
    """
    lease = models.ForeignKey(LeaseContract, on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_date = models.DateField()

    def __str__(self):
        return f"Оплата в размере {self.amount} рублей {self.payment_date} по {self.lease}"
