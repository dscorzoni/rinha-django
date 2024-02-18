from .models import Customer, Transaction
from .serializers import CustomerSerializer, TransactionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db import transaction
import datetime
# Create your views here.


class AddTransaction(APIView):
    def post(self, request, pk):
        with transaction.atomic():
            customer = get_object_or_404(
                Customer.objects.select_for_update(),
                id=pk
            )

            input_data = request.data
            input_data['cliente'] = customer.id
            input_serializer = TransactionSerializer(data=input_data)

            if input_serializer.is_valid():
                novo_valor = input_serializer.validated_data['valor']
                tipo = input_serializer.validated_data['tipo']

                if (tipo == 'd'):
                    novo_saldo = customer.saldo - novo_valor
                    if (novo_saldo < (-1 * customer.limite)):
                        return Response({"mensagem": "Limite insuficiente", "saldo": customer.saldo, "limite": customer.limite}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                else:
                    novo_saldo = customer.saldo + novo_valor

                input_serializer.save()
                customer.saldo = novo_saldo
                customer.save()
                return Response({"limite": customer.limite, "saldo": novo_saldo}, status=status.HTTP_200_OK)
            else:
                return Response(input_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class showExtract(APIView):
    def get(self, request, pk):
        customer = get_object_or_404(
            Customer,
            id=pk
        )

        transactions = Transaction.objects.filter(
            cliente__id=pk).order_by("-realizada_em")[:10]
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
