from core.models import Transaction
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect


@login_required
def transaction_list(request):
    sent_transaction = Transaction.objects.filter(sender=request.user,transaction_type='transfer').order_by('-id')
    recieved_transaction = Transaction.objects.filter(reciever=request.user,transaction_type='transfer').order_by('-id')


    request_sent_transaction = Transaction.objects.filter(sender=request.user, transaction_type="request")
    request_recieved_transaction = Transaction.objects.filter(reciever=request.user, transaction_type="request")

    context = {
        "sent_transaction":sent_transaction,
        "recieved_transaction":recieved_transaction,

        'request_sent_transaction':request_sent_transaction,
        'request_recieved_transaction':request_recieved_transaction,
    }


    return render(request,'transaction/transaction_list.html',context)


@login_required
def transaction_detail_sent(request, transaction_id):
    try:
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except Transaction.DoesNotExist:
        transaction = None

    context = {'transaction': transaction}
    return render(request, 'transaction/transaction_detail_sent.html', context)


@login_required
def transaction_detail_received(request, transaction_id):
    try:
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except Transaction.DoesNotExist:
        transaction = None

    context = {'transaction': transaction}
    return render(request, 'transaction/transaction_detail_received.html', context)
