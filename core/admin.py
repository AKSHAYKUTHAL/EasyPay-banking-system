from django.contrib import admin
from core.models import Transaction,CreditCard


class TransactionAdmin(admin.ModelAdmin):
    list_editable = ['amount', 'transaction_status', 'transaction_type']
    list_display = ['id','user', 'amount', 'transaction_status', 'transaction_type', 'reciever', 'sender']


class CreditCardAdmin(admin.ModelAdmin):
    list_editable = ['amount', 'card_type','card_tier','card_status']
    list_display = ['user', 'amount','number','name','month','year', 'card_type','card_tier','card_status']


admin.site.register(Transaction,TransactionAdmin)
admin.site.register(CreditCard,CreditCardAdmin)

