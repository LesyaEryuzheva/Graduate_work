from django.db.models import Sum

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer

from my_wallet.serializers import ReceiptSerializer, TransactionSerializer
from my_wallet.models import Account, Receipt, Transaction, Transfer, Expense, Income


class StatisticsReceiptViewSet(viewsets.GenericViewSet):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, *args, **kwargs):
        accounts = Account.objects.filter(user=self.request.user)
        date_from = self.request.query_params.get('date_from', 0)
        date_to = self.request.query_params.get('date_to', 0)

        queryset = Receipt.objects.filter(account__in=accounts)

        if date_from:
            queryset = queryset.filter(date__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__date__lte=date_to)

        queryset = queryset.values('income_category').annotate(total=(Sum('amount')))

        response_dict = {}
        for item in queryset:
            income_category = str(Income.objects.filter(id=item['income_category']).get())
            response_dict[income_category] = item['total']

        return Response(response_dict)


class StatisticsTransactionViewSet(viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, *args, **kwargs):
        accounts = Account.objects.filter(user=self.request.user)
        date_from = self.request.query_params.get('date_from', 0)
        date_to = self.request.query_params.get('date_to', 0)

        queryset = Transaction.objects.filter(account__in=accounts)

        if date_from:
            queryset = queryset.filter(date__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__date__lte=date_to)

        queryset = queryset.values('expense_category').annotate(total=(Sum('amount')))

        response_dict = {}
        for item in queryset:
            expense_category = str(Expense.objects.filter(id=item['expense_category']).get())
            response_dict[expense_category] = item['total']

        return Response(response_dict)


class StatisticsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, *args, **kwargs):
        accounts = Account.objects.filter(user=self.request.user)
        receipts = Receipt.objects.filter(account__in=accounts)
        transactions = Transaction.objects.filter(account__in=accounts)
        date_from = self.request.query_params.get('date_from', 0)
        date_to = self.request.query_params.get('date_to', 0)

        if date_from:
            receipts = receipts.filter(date__date__gte=date_from)
            transactions = transactions.filter(date__date__gte=date_from)
        if date_to:
            receipts = receipts.filter(date__date__lte=date_to)
            transactions = transactions.filter(date__date__lte=date_to)

        response_dict = {
            'Receipt_sum': receipts.aggregate(Sum('amount'))['amount__sum'],
            'Transaction_sum': transactions.aggregate(Sum('amount'))['amount__sum']
        }

        return Response(response_dict)


class ExportReceiptToExcelViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ReceiptSerializer
    renderer_classes = [XLSXRenderer]
    filename = 'receipt.xlsx'

    def get_queryset(self):
        accounts = Account.objects.filter(user=self.request.user)
        return Receipt.objects.filter(account__in=accounts)


class ExportTransactionsToExcelViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer
    renderer_classes = [XLSXRenderer]
    filename = 'transactions.xlsx'

    def get_queryset(self):
        accounts = Account.objects.filter(user=self.request.user)
        return Transaction.objects.filter(account__in=accounts).all()
