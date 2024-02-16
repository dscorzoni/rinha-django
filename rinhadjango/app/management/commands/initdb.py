from ...models import Customer
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):

        limites = [1000 * 100, 800 * 100,
                   10000 * 100, 100000 * 100, 5000 * 100]

        for lim in limites:
            cliente = Customer(limite=lim, saldo=0)
            cliente.save()

        verificar = Customer.objects.all()
        print(verificar)
