# Generated by Django 5.0.7 on 2024-08-22 13:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LeaseContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(help_text='Дата и время начала аренды', verbose_name='Дата начала аренды')),
                ('end_date', models.DateTimeField(help_text='Дата и время окончания аренды', verbose_name='Дата окончания аренды')),
                ('rent_amount', models.DecimalField(decimal_places=2, help_text='Сумма аренды', max_digits=10, verbose_name='Сумма аренды')),
                ('rent_period', models.CharField(choices=[('Hour', 'Час'), ('Day', 'Сутки'), ('Month', 'Месяц')], help_text='Период аренды (часы, сутки, месяцы)', max_length=20, verbose_name='Период аренды')),
                ('deposit_amount', models.DecimalField(blank=True, decimal_places=2, help_text='Сумма депозита (необязательное поле)', max_digits=10, null=True, verbose_name='Сумма депозита')),
            ],
            options={
                'verbose_name': 'Договор аренды',
                'verbose_name_plural': 'Договора аренды',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес недвижимости')),
                ('property_type', models.CharField(choices=[('Apartment', 'Квартира'), ('House', 'Дом'), ('Commercial', 'Коммерческая недвижимость'), ('Land', 'Земельный участок')], max_length=20, verbose_name='Тип недвижимости')),
                ('description', models.TextField(blank=True, verbose_name='Описание недвижимости')),
                ('rental_type', models.CharField(choices=[('Hourly', 'Почасовая аренда'), ('Daily', 'Посуточная аренда'), ('LongTerm', 'Длительная аренда')], help_text='Тип ренты (почасовая, посуточная, длительная аренда)', max_length=20, verbose_name='Тип ренты')),
                ('price', models.DecimalField(decimal_places=2, help_text='Стоимость аренды', max_digits=10, verbose_name='Стоимость аренды')),
                ('price_period', models.CharField(choices=[('Hour', 'в час'), ('Day', 'в сутки'), ('Month', 'в месяц')], help_text='Стоимость за период: в час, в сутки или в месяц', max_length=20, verbose_name='Стоимость за период')),
                ('minimum_rental_value', models.IntegerField(help_text='Минимальный период сдачи', verbose_name='Минимальный период сдачи')),
                ('minimum_rental_unit', models.CharField(choices=[('Hour', 'в час'), ('Day', 'в сутки'), ('Month', 'в месяц')], help_text='Единица измерения минимального периода сдачи (часы, дни, месяцы)', max_length=5, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Недвижимость',
                'verbose_name_plural': 'Недвижимость',
            },
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя арендатора')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия арендатора')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта арендатора')),
                ('phone_number', models.CharField(blank=True, max_length=15, verbose_name='Номер телефона арендатора')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Адрес арендатора')),
            ],
            options={
                'verbose_name': 'Арендатор',
                'verbose_name_plural': 'Арендаторы',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма платежа')),
                ('payment_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время совершения платежа')),
                ('lease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestate.leasecontract', verbose_name='Ссылка на договор аренды')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
            },
        ),
    ]