from django.db import models

# Create your models here.


class Customer(models.Model):
    limite = models.IntegerField()
    saldo = models.IntegerField()


class Transaction(models.Model):
    cliente = models.ForeignKey(
        Customer, on_delete=models.CASCADE, db_index=True, related_name="transactions")
    valor = models.PositiveIntegerField()
    tipo = models.CharField(
        choices=[('c', 'c'), ('d', 'd')], max_length=1)
    descricao = models.CharField(max_length=10)
    realizada_em = models.DateTimeField(auto_now_add=True, db_index=True)
