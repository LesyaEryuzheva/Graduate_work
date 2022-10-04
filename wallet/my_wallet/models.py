from django.db import models
from django.conf import settings


class Account(models.Model):
    title = models.CharField(max_length=20, blank=True)
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f'{self.title}'


class Income(models.Model):
    income_category = models.CharField(max_length=50)

    def __str__(self):
        return self.income_category


class Receipt(models.Model):
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    date = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='receipts',
    )
    income_category = models.ForeignKey('Income', on_delete=models.CASCADE)

    def __str__(self):
        return f'Account number {self.account.id} was replenished' +\
            f' with {str(self.amount)} for {str(self.income_category)}'


class Expense(models.Model):
    expense_category = models.CharField(max_length=50)

    def __str__(self):
        return self.expense_category


class Transaction(models.Model):
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    date = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
    expense_category = models.ForeignKey('Expense', on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.amount)} were spent from account ' +\
            f'number {self.account.id} for {self.expense_category.id}'


class Transfer(models.Model):
    from_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='from_account'
    )
    to_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='to_account'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    date = models.DateTimeField(auto_now_add=True)
