from django.contrib import admin
from core.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_editable = ['amount', 'transaction_status', 'transaction_type']
    list_display = ['user', 'amount', 'transaction_status', 'transaction_type', 'reciever', 'sender']

admin.site.register(Transaction,TransactionAdmin)
