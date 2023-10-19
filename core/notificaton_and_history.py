from django.shortcuts import render, redirect
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from core.models import Transaction,Notification,CreditCard,History
import time
from decimal import Decimal


def notification_detail(request,nid):
    try:
        notification = Notification.objects.get(nid=nid, user=request.user)

        notification.delete()
    except Notification.DoesNotExist:
        messages.error(request, 'Your Notification is removed,For more information check the History')
        return redirect('account:dashboard')

    if notification.transaction_id:
        transaction = Transaction.objects.get(transaction_id=notification.transaction_id)
    else:
        transaction = None

    # if notification.card_number:
    #     credit_card = CreditCard.objects.get(number=notification.card_number)
    # else:
    #     credit_card = None

    
    context = {
        'notification':notification,
        'transaction':transaction,
        # 'credit_card':credit_card,
    }
    
    return render(request,'notificaton_and_history/notification_detail.html',context)
    

def history_detail(request,nid):
    try:
        history = History.objects.get(nid=nid, user=request.user)
        history.is_read = True
        history.save()       
    except:
        messages.error(request, 'An Error Occured')
        return redirect('account:dashboard')

    if history.transaction_id:
        transaction = Transaction.objects.get(transaction_id=history.transaction_id)
    else:
        transaction = None

    # if notification.card_number:
    #     credit_card = CreditCard.objects.get(number=notification.card_number)
    # else:
    #     credit_card = None

    
    context = {
        'history':history,
        'transaction':transaction,
        # 'credit_card':credit_card,
    }
    
    return render(request,'notificaton_and_history/history_detail.html',context)