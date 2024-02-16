from ...models import Customer
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):

        limites = [100000, 80000, 1000000, 10000000, 500000]

        for lim in limites:
            cliente = Customer(limite=lim, saldo=0)
            cliente.save()

        verificar = Customer.objects.all()
        print(verificar)
