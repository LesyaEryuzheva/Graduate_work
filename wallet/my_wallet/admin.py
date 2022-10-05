from django.contrib import admin

from .models import (Account, Income, Receipt,
                     Expense, Transaction, Transfer)


class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'balance',
    )
    search_fields = ('title',)


class IncomeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'income_category',
    )
    search_fields = ('income_category',)
    ordering = ('income_category',)


class ReceiptAdmin(admin.ModelAdmin):
    list_display = (
        'account',
        'income_category',
        'amount',
        'date',
    )
    search_fields = ('income_category',)
    ordering = ('account', 'date',)


class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'expense_category',
    )
    search_fields = ('expense_category',)
    ordering = ('expense_category',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'account',
        'expense_category',
        'amount',
        'date',
    )
    search_fields = ('expense_category',)
    ordering = ('account', 'date',)


class TransferAdmin(admin.ModelAdmin):
    list_display = (
        'from_account',
        'to_account',
        'amount',
        'date',
    )
    ordering = ('from_account', 'date',)


admin.site.register(Account, AccountAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Transfer, TransferAdmin)
