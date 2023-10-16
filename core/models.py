from django.db import models
from userauths.models import User
from account.models import Account
from shortuuid.django_fields import ShortUUIDField
from decimal import Decimal,ROUND_HALF_UP


TRANSACTION_TYPE = (
    ('none','None'),
    ('transfer','Transfer'),
    ('recieved','Recieved'),
    ('withdraw','Withdraw'),
    ('refund','Refund'),
    ('request','Payment Request'),
    
)

TRANSACTION_STATUS = (
    ('none','None'),
    ('failed','Failed'),
    ('completed','Completed'),
    ('pending','Pending'),
    ('processing','Processing'),
    ('request_sent' ,'Request Sent'),
    ('request_processing' ,'Request Processing'),
    ('request_settled' ,'Request Settled' ),
)


class Transaction(models.Model):
    transaction_id = ShortUUIDField(unique=True, length=15, max_length=20, prefix='TRN')

    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name='user')
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    description = models.CharField(max_length=1000, null=True, blank=True)

    reciever = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reciever')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sender')

    reciever_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='reciever_account')
    sender_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='sender_account')

    transaction_status = models.CharField(choices=TRANSACTION_STATUS, max_length=100, default='None')    
    transaction_type = models.CharField(choices=TRANSACTION_TYPE,max_length=100, default='None')

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False,null=True, blank=True)

    def fee(self):
        fee = self.amount * Decimal('.03')  # Using Decimal('0.035') instead of 3.5 / 100
        return fee.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)  # Rounding to 2 decimal places
        # fee = 0
        # return fee

    def receiving_amount(self):
        receiving_amount = self.amount - self.fee()
        return receiving_amount.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)  # Rounding to 2 decimal places
    

    def payment_with_fee(self):
        payment_with_fee = self.amount + self.fee()
        return payment_with_fee.quantize(Decimal('.01'), rounding=ROUND_HALF_UP) 


    def __str__(self):
        try:
            return f"{self.user}"
        except:
            return f"Transaction"