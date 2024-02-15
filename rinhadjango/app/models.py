from django.db import models

# Create your models here.


class Clientes(models.Model):
    limite = models.IntegerField()
    saldo_inicial = models.IntegerField()


class Transacoes(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    valor = models.IntegerField()
    tipo = models.CharField(max_length=1)
    descricao = models.CharField(max_length=150)
    realizada_em = models.DateField()
