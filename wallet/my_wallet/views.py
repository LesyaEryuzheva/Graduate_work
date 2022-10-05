from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status, filters
# from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (AccountSerializer,
                          ReceiptSerializer, TransactionSerializer,
                          TransferSerializer)
from .models import Account, Receipt, Transaction, Transfer
from .services import make_transfer, make_transaction, make_receipt


class AccountViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin):
    serializer_class = AccountSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Account.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReceiptViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin):
    serializer_class = ReceiptSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Receipt.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'income_category': ['exact'],
        'account': ['exact'],
        'date': ['gte', 'lte']
    }
    ordering_fields = ('date',)

    def get_queryset(self):
        accounts = Account.objects.filter(user=self.request.user)
        date_from = self.request.query_params.get('date_from', 0)
        date_to = self.request.query_params.get('date_to', 0)
        inc_id = self.request.query_params.get('inc_id', 0)

        queryset = self.queryset.filter(account__in=accounts)
        if date_from:
            queryset = queryset.filter(date__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__date__lte=date_to)
        if inc_id:
            queryset = queryset.filter(income_category=inc_id)

        return queryset.order_by('account')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            make_receipt(**serializer.validated_data)
        except ValueError as exc:
            content = {'error': str(exc)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class TransactionViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin):
    serializer_class = TransactionSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'expense_category': ['exact'],
        'account': ['exact'],
        'date': ['gte', 'lte']
    }
    ordering_fields = ('date',)

    def get_queryset(self):
        accounts = Account.objects.filter(user=self.request.user)
        date_from = self.request.query_params.get('date_from', 0)
        date_to = self.request.query_params.get('date_to', 0)
        exp_id = self.request.query_params.get('exp_id', 0)

        queryset = self.queryset.filter(account__in=accounts)
        if date_from:
            queryset = queryset.filter(date__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__date__lte=date_to)
        if exp_id:
            queryset = queryset.filter(expense_category=exp_id)

        return queryset.order_by('account')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            make_transaction(**serializer.validated_data)
        except ValueError as exc:
            content = {'error': str(exc)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class TransferViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin):
    serializer_class = TransferSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Transfer.objects.all()

    def get_queryset(self):
        accounts = Account.objects.filter(user=self.request.user)
        return self.queryset.filter(from_account__in=accounts).order_by('from_account')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            make_transfer(**serializer.validated_data)
        except ValueError as exc:
            content = {'error': str(exc)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)
