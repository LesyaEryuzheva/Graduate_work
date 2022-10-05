from rest_framework import serializers

from .models import Account, Receipt, Transaction, Transfer


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'balance', 'title')
        read_only_fields = ('id', 'balance')


class ReceiptSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(ReceiptSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['account'].queryset = self.fields['account']\
                .queryset.filter(user=self.context['view'].request.user)

    class Meta:
        model = Receipt
        fields = ('id', 'account', 'income_category', 'amount', 'date')
        read_only_fields = ('id', 'date')


class TransactionSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(TransactionSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['account'].queryset = self.fields['account']\
                .queryset.filter(user=self.context['view'].request.user)

    class Meta:
        model = Transaction
        fields = ('id', 'account', 'date', 'expense_category', 'amount')
        read_only_fields = ('id', )


class TransferSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(TransferSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['from_account'].queryset = self.fields['from_account'] \
                .queryset.filter(user=self.context['view'].request.user)
        if 'request' in self.context:
            self.fields['to_account'].queryset = self.fields['to_account'] \
                .queryset.filter(user=self.context['view'].request.user)

    class Meta:
        model = Transfer
        fields = ('id', 'from_account', 'to_account', 'amount')
        read_only_fields = ('id',)
