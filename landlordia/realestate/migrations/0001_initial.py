# Generated by Django 5.0.7 on 2024-07-31 14:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaseContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(help_text='Дата начала аренды')),
                ('end_date', models.DateField(help_text='Дата окончания аренды')),
                ('rent_amount', models.IntegerField(help_text='Сумма аренды')),
                ('rent_period', models.CharField(choices=[('Hour', 'Час'), ('Day', 'Сутки'), ('Month', 'Месяц')], help_text='Период аренды (часы, сутки, месяцы)', max_length=20)),
                ('deposit_amount', models.IntegerField(blank=True, help_text='Сумма депозита (необязательное поле)', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('address', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('payment_date', models.DateField()),
                ('lease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestate.leasecontract')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('property_type', models.CharField(choices=[('Apartment', 'Квартира'), ('House', 'Дом'), ('Commercial', 'Коммерческая недвижимость'), ('Land', 'Земельный участок')], max_length=20)),
                ('description', models.TextField(blank=True)),
                ('rental_type', models.CharField(choices=[('Hourly', 'Почасовая аренда'), ('Daily', 'Посуточная аренда'), ('LongTerm', 'Длительная аренда')], help_text='Тип ренты (почасовая, посуточная, длительная аренда)', max_length=20)),
                ('price', models.DecimalField(decimal_places=2, help_text='Стоимость аренды', max_digits=10)),
                ('price_period', models.CharField(choices=[('Hour', 'в час'), ('Day', 'в сутки'), ('Month', 'в месяц')], help_text='Стоимость за период: в час, в сутки или в месяц', max_length=20)),
                ('minimum_rental_value', models.IntegerField(help_text='Минимальный период сдачи')),
                ('minimum_rental_unit', models.CharField(choices=[('Hour', 'в час'), ('Day', 'в сутки'), ('Month', 'в месяц')], help_text='Единица измерения минимального периода сдачи (часы, дни, месяцы)', max_length=5)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestate.owner')),
            ],
        ),
        migrations.AddField(
            model_name='leasecontract',
            name='property',
            field=models.ForeignKey(help_text='Арендуемая недвижимость', on_delete=django.db.models.deletion.CASCADE, to='realestate.property'),
        ),
        migrations.AddField(
            model_name='leasecontract',
            name='tenant',
            field=models.ForeignKey(help_text='Арендатор', on_delete=django.db.models.deletion.CASCADE, to='realestate.tenant'),
        ),
    ]