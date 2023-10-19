from django.contrib import admin
from core.models import Transaction,CreditCard,Notification,History


class TransactionAdmin(admin.ModelAdmin):
    list_editable = ['amount', 'transaction_status', 'transaction_type']
    list_display = ['id','user', 'amount', 'transaction_status', 'transaction_type', 'reciever', 'sender']


class CreditCardAdmin(admin.ModelAdmin):
    list_editable = ['amount', 'card_type','card_tier','card_status']
    list_display = ['user', 'amount','format_card_number','name','month','year', 'card_type','card_tier','card_status']


class NotificationAdmin(admin.ModelAdmin):
    list_editable = ['is_read']
    list_display = ['user', 'notification_type', 'amount' ,'date','sender','receiver','is_read']

class HistoryAdmin(admin.ModelAdmin):
    list_editable = ['is_read']
    list_display = ['user', 'history_type', 'amount' ,'date','sender','receiver','is_read']


admin.site.register(Transaction,TransactionAdmin)
admin.site.register(CreditCard,CreditCardAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(History, HistoryAdmin)


