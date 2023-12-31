from django.db import models
from userauths.models import User
from account.models import Account
from shortuuid.django_fields import ShortUUIDField
from decimal import Decimal,ROUND_HALF_UP
import datetime


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
    ('cancelled','Cancelled'),
    ('processing','Processing'),
    ('request_sent' ,'Request Sent'),
    ('request_processing' ,'Request Processing'),
    ('request_settled' ,'Request Settled' ),
    ('request_declined' ,'Request Declined' ),

)

CARD_TYPE = (
    ("master", "Master"),
    ("visa", "Visa"),
    ("rupay", "Rupay"),

)

CARD_TIER = (
    ("classic","Classic"),
    ("gold","Gold"),
    ("platinum","Platinum"),
    ("signature","Signature"),
    ("infinite","Infinite"),

)


NOTIFICATION_TYPE = (
    ("None", "None"),
    ("Transfer", "Transfer"),
    ("Credit Alert", "Credit Alert"),
    ("Debit Alert", "Debit Alert"),
    ("Sent Payment Request", "Sent Payment Request"),
    ("Recieved Payment Request", "Recieved Payment Request"),
    ("Settled Payment Request To", "Settled Payment Request To"),
    ("Settled Payment Request From", "Settled Payment Request From"),
    ("Funded Credit Card", "Funded Credit Card"),
    ("Withdrew Credit Card Funds", "Withdrew Credit Card Funds"),
    ("Deleted Credit Card", "Deleted Credit Card"),
    ("Added Credit Card", "Added Credit Card"),
    ("Activated Credit Card", "Activated Credit Card"),
    ("De-Activated Credit Card", "De-Activated Credit Card"),

)
# NOTIFICATION_CATEGORY =(
#     ("annoucements", "Annoucements"),
#     ("None", "None"),
#     ("None", "None"),
#     ("None", "None"),
#     ("None", "None"),
#     ("None", "None"),
#     ("None", "None"),
#     ("None", "None"),
#     ("None", "None"),
# )

HISTORY_TYPE = (
    ("None", "None"),
    ("Transfer", "Transfer"),
    ("Credit Alert", "Credit Alert"),
    ("Debit Alert", "Debit Alert"),
    ("Sent Payment Request", "Sent Payment Request"),
    ("Recieved Payment Request", "Recieved Payment Request"),
    ("Settled Payment Request To", "Settled Payment Request To"),
    ("Settled Payment Request From", "Settled Payment Request From"),
    ("Funded Credit Card", "Funded Credit Card"),
    ("Withdrew Credit Card Funds", "Withdrew Credit Card Funds"),
    ("Deleted Credit Card", "Deleted Credit Card"),
    ("Added Credit Card", "Added Credit Card"),
    ("Activated Credit Card", "Activated Credit Card"),
    ("De-Activated Credit Card", "De-Activated Credit Card"),



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
        fee = self.amount * Decimal('.0')  # Using Decimal('0.035') instead of 3.5 / 100
        return fee.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)  # Rounding to 2 decimal places


    def transaction_year(self):
        return self.date.year
    
    def transaction_month(self):
        return self.date.month

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
        

class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credit_card_id = ShortUUIDField(unique=True, length=5, max_length=20, prefix="CARD", alphabet="1234567890")
    card_pin_number = ShortUUIDField(length=4, max_length=4, alphabet="1234567890")


    name = models.CharField(max_length=100)
    number = ShortUUIDField(length=14, max_length=14,prefix="47", alphabet="1234567890")
    month = models.IntegerField(default=datetime.datetime.now().month)
    year = models.IntegerField(default=datetime.datetime.now().year + 5)
    cvv = ShortUUIDField(length=3, max_length=3, alphabet="1234567890")

    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    card_type = models.CharField(choices=CARD_TYPE, max_length=20, default="master")
    card_tier = models.CharField(choices=CARD_TIER, max_length=20, default="classic")
    card_status = models.BooleanField(default=True)

    date = models.DateTimeField(auto_now_add=True)

    def format_card_number(self):
        formatted_number  = ' '.join([self.number[i:i + 4] for i in range(0, len(self.number), 4)])
        return formatted_number 

    def year_in_two_digits(self):
        year_in_two_digits = self.year % 100
        return year_in_two_digits

    def __str__(self):
        return f"{self.user}"
    


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notification_type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE, default="none")
    amount = models.IntegerField(default=0)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    nid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='reciever_details')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='sender_details')
    card_number = models.CharField(max_length=100,null=True,blank=True)
    card_type = models.CharField(max_length=50,blank=True,null=True)
    card_tier = models.CharField(max_length=50,blank=True,null=True)
    transaction_id = models.CharField(max_length=100,blank=True,null=True)


    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Notification"

    def __str__(self):
        return f"{self.user} - {self.notification_type}"
    

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    history_type = models.CharField(max_length=100, choices=HISTORY_TYPE, default="none")
    amount = models.IntegerField(default=0)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    nid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='reciever_details_history')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='sender_details_history')
    card_number = models.CharField(max_length=100,null=True,blank=True)
    card_type = models.CharField(max_length=50,blank=True,null=True)
    card_tier = models.CharField(max_length=50,blank=True,null=True)
    transaction_id = models.CharField(max_length=100,blank=True,null=True)



    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "History"

    def __str__(self):
        return f"{self.user} - {self.history_type}"