# Generated by Django 4.2.10 on 2024-02-18 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_transaction_realizada_em'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'default_related_name': 'transactions'},
        ),
    ]