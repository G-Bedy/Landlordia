# Generated by Django 5.0.7 on 2024-08-09 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0002_alter_leasecontract_deposit_amount_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leasecontract',
            options={'verbose_name': 'Договор аренды', 'verbose_name_plural': 'Договора аренды'},
        ),
        migrations.AlterModelOptions(
            name='owner',
            options={'verbose_name': 'Собственник', 'verbose_name_plural': 'Собственники'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'Платеж', 'verbose_name_plural': 'Платежи'},
        ),
        migrations.AlterModelOptions(
            name='property',
            options={'verbose_name': 'Недвижимость', 'verbose_name_plural': 'Недвижимость'},
        ),
        migrations.AlterModelOptions(
            name='tenant',
            options={'verbose_name': 'Арендатор', 'verbose_name_plural': 'Арендаторы'},
        ),
    ]