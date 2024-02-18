# Generated by Django 4.2.10 on 2024-02-18 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_transaction_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={},
        ),
        migrations.AlterField(
            model_name='transaction',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='app.customer'),
        ),
    ]
