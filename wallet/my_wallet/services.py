from django.db import transaction

from .models import Transfer, Transaction, Receipt


def make_transfer(from_account, to_account, amount):
    if from_account.balance < amount:
        raise(ValueError('Not enough money'))
    if from_account == to_account:
        raise(ValueError('Chose another account'))
    if amount == 0:
        raise(ValueError('Transfer amount cannot be zero'))
    if amount < 0:
        raise(ValueError('Transfer amount must be at least zero'))

    with transaction.atomic():
        from_balance = from_account.balance - amount
        from_account.balance = from_balance
        from_account.save()

        to_balance = to_account.balance + amount
        to_account.balance = to_balance
        to_account.save()

        transfer = Transfer.objects.create(
            from_account=from_account,
            to_account=to_account,
            amount=amount
        )

    return transfer


def make_transaction(amount, account, expense_category):
    if account.balance < amount:
        raise(ValueError('Not enough money'))

    with transaction.atomic():
        if amount > 0:
            account.balance -= amount
        else:
            raise(ValueError('Incorrect amount of money'))
        account.save()
        tran = Transaction.objects.create(
            amount=amount,
            account=account,
            expense_category=expense_category
        )

    return account, tran


def make_receipt(amount, account, income_category):

    with transaction.atomic():
        if amount > 0:
            account.balance += amount
        else:
            raise(ValueError('Incorrect amount of money'))
        account.save()

        receipt = Receipt.objects.create(
            amount=amount,
            account=account,
            income_category=income_category
        )

    return account, receipt
