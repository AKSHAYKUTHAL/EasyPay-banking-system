from core.models import Transaction
from account.models import Account,KYC
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect



def all_transactions(request):
    transactions = Transaction.objects.all()

    context = {
        'transactions':transactions
    }

    return render(request,'transaction/all_transactions.html',context)

@login_required
def transaction_list(request):
    try:
        kyc = KYC.objects.get(user=request.user)
    except:
        messages.error(request,'You need to submit your KYC!')
        return redirect('account:kyc_reg')
    
    sent_transaction = Transaction.objects.filter(sender=request.user,transaction_type='transfer').order_by('-id')
    recieved_transaction = Transaction.objects.filter(reciever=request.user,transaction_type='transfer').order_by('-id')


    request_sent_transaction = Transaction.objects.filter(sender=request.user, transaction_type="request").order_by('-id')
    request_recieved_transaction = Transaction.objects.filter(reciever=request.user, transaction_type="request").order_by('-id')

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
