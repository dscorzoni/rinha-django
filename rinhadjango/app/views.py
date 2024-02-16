from .models import Customer, Transaction
from .serializers import CustomerSerializer, TransactionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404
import datetime
# Create your views here.


class CustomerListView(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


class AddTransaction(APIView):
    def get_customer(self, pk):
        try:
            return Customer.objects.get(id=pk)
        except Customer.DoesNotExist:
            raise Http404

    def get_transactions(self, pk):
        try:
            return Transaction.objects.filter(cliente__id=pk)
        except Transaction.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        customer = self.get_customer(pk)
        limite = customer.limite
        saldo_atual = customer.saldo
        input_data = request.data
        input_data['cliente'] = customer.id
        input_serializer = TransactionSerializer(data=input_data)

        if input_serializer.is_valid():
            novo_valor = input_serializer.validated_data['valor']
            tipo = input_serializer.validated_data['tipo']

            if (tipo == 'd'):
                novo_saldo = saldo_atual - novo_valor
                if (novo_saldo < (-1 * limite)):
                    return Response({"mensagem": "Limite insuficiente", "saldo": saldo_atual, "limite": limite}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                else:
                    input_serializer.save()
                    customer.saldo = novo_saldo
                    customer.save()
                    return Response({"limite": limite, "saldo": novo_saldo}, status=status.HTTP_200_OK)
            else:
                novo_saldo = saldo_atual + novo_valor
                input_serializer.save()
                customer.saldo = novo_saldo
                customer.save()
                return Response({"limite": limite, "saldo": novo_saldo}, status=status.HTTP_200_OK)

        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class showExtract(APIView):
    def get_transactions(self, pk):
        try:
            return Transaction.objects.filter(cliente__id=pk)
        except Transaction.DoesNotExist:
            raise Http404

    def get_customer(self, pk):
        try:
            return Customer.objects.get(id=pk)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        customer = self.get_customer(pk)

        transactions = self.get_transactions(pk)
        transaction_serializer = TransactionSerializer(transactions, many=True)

        saida = {
            "saldo": {
                "total": customer.saldo,
                "data_extrato": datetime.datetime.now(),
                "limite": customer.limite
            },
            "ultimas_transacoes": transaction_serializer.data
        }

        return Response(saida, status=status.HTTP_200_OK)
