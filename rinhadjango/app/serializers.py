from .models import Customer, Transaction
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'limite', 'saldo']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['cliente', 'valor', 'tipo', 'descricao', 'realizada_em']

    # to_representation() is used to avoid returning cliente_id in the extrato endpoint
    def to_representation(self, instance):
        return {'valor': instance.valor, 'tipo': instance.tipo, 'descricao': instance.descricao, 'realizada_em': instance.realizada_em}
