from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Owner(models.Model):
    """
    Модель Owner, создание собственника недвижимости.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='Номер телефона владельца'
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Адрес владельца'
    )

    def __str__(self):
        return self.user.username


class Property(models.Model):
    """
    Модель Property, создание объекта недвижимости, принадлежащей собственнику.
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

    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        verbose_name='Владелец недвижимости'
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Адрес недвижимости'
    )
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPE_CHOICES,
        verbose_name='Тип недвижимости'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание недвижимости'
    )
    rental_type = models.CharField(
        max_length=20,
        choices=RENTAL_TYPE_CHOICES,
        help_text="Тип ренты (почасовая, посуточная, длительная аренда)",
        verbose_name='Тип ренты'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Стоимость аренды",
        verbose_name='Стоимость аренды')
    price_period = models.CharField(
        max_length=20,
        choices=PERIOD_CHOICES,
        help_text="Стоимость за период: в час, в сутки или в месяц",
        verbose_name='Стоимость за период'
    )
    minimum_rental_value = models.IntegerField(
        help_text="Минимальный период сдачи",
        verbose_name='Минимальный период сдачи'
    )
    minimum_rental_unit = models.CharField(
        max_length=5,
        choices=PERIOD_CHOICES,
        help_text="Единица измерения минимального периода сдачи "
                  "(часы, дни, месяцы)",
        verbose_name='Единица измерения'
    )

    def __str__(self):
        return f"{self.owner} - {self.property_type} - {self.address}"


class Tenant(models.Model):
    """
    Модель Tenant (Арендатор), создание объекта арендатора.
    """
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя арендатора')
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия арендатора')
    email = models.EmailField(
        verbose_name='Электронная почта арендатора')
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='Номер телефона арендатора'
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Адрес арендатора'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class LeaseContract(models.Model):
    """
    Модель LeaseContract, создание договора аренды недвижимости.
    """
    PERIOD_CHOICES = [
        ('Hour', 'Час'),
        ('Day', 'Сутки'),
        ('Month', 'Месяц')
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        help_text="Арендуемая недвижимость",
        verbose_name='Ссылка на арендуемую недвижимость'
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        help_text="Арендатор",
        verbose_name='Ссылка на арендатора'
    )
    start_date = models.DateTimeField(
        help_text="Дата и время начала аренды",
        verbose_name='Дата начала аренды'
    )
    end_date = models.models.DateTimeField(
        help_text="Дата и время окончания аренды",
        verbose_name='Дата окончания аренды'
    )
    rent_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Сумма аренды",
        verbose_name='Сумма аренды'
    )
    rent_period = models.CharField(
        max_length=20,
        choices=PERIOD_CHOICES,
        help_text=("Период аренды (часы, сутки, месяцы)"),
        verbose_name='Период аренды'
    )
    deposit_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=("Сумма депозита (необязательное поле)"),
        verbose_name='Сумма депозита'
    )

    def clean(self):
        """
        Валидация дат начала и окончания аренды.
        """
        if self.end_date < self.start_date:
            raise ValidationError("Дата окончания аренды не может "
                                  "быть раньше даты начала аренды")

    def __str__(self):
        return (f"Договор аренды недвижимости по адресу: "
                f"{self.property.address} с {self.start_date} "
                f"по {self.end_date}, {self.rent_amount} рублей "
                f"за {self.rent_period}, "
                f"арендатор {self.tenant.first_name}")


class Payment(models.Model):
    """
    Модель Payment, платежи по договору аренды.
    """
    lease = models.ForeignKey(
        LeaseContract,
        on_delete=models.CASCADE,
        verbose_name='Ссылка на договор аренды'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма платежа'
    )
    payment_date = models.models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время совершения платежа'
    )
    def __str__(self):
        return (f"Оплата в размере {self.amount} рублей "
                f"{self.payment_date} по {self.lease}")
