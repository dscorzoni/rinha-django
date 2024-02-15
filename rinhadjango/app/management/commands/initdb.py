from ...models import Clientes
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):

        limites = [100000, 80000, 1000000, 10000000, 500000]

        for lim in limites:
            cliente = Clientes(limite=lim, saldo_inicial=0)
            cliente.save()

        verificar = Clientes.objects.all()
        print(verificar)
