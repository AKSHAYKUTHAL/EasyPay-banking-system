from django.shortcuts import render, redirect
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from core.models import Transaction
import time
from decimal import Decimal




@login_required
def search_users_account_number(request):
    # account = Account.objects.filter(account_status='active')
    account = Account.objects.all()
    query = request.POST.get('account_number')

    if query:
        account = account.filter(
            Q(account_number=query) | Q(account_id=query)
        ).distinct()

    context = {
        'account':account,
        'query':query,
    }

    return render(request,'transfer/search_users_by_account_number.html',context)




def amount_transfer(request,account_number):
    try:
        account = Account.objects.get(account_number=account_number)
    except:
        messages.error(request,'Account Does Not Exist.')
        return redirect('core:search_account')
    context = {
        'account':account,
    }
    return render(request,'transfer/amount_transfer.html',context)




def amount_transfer_process(request, account_number):
    account = Account.objects.get(account_number=account_number)
    sender = request.user
    reciever = account.user 

    sender_account = request.user.account
    reciever_account = account

    if request.method == 'POST':
        amount = request.POST.get('amount_send')
        description = request.POST.get('description')

        print(amount)
        print(description)

        if sender_account.account_balance >= Decimal(amount):
            new_transation = Transaction.objects.create(
                user = request.user,
                amount = Decimal(amount),
                description = description,
                reciever = reciever,
                sender = sender,
                sender_account = sender_account,
                reciever_account = reciever_account,
                transaction_status = 'processing',
                transaction_type = 'transfer'
            )
            new_transation.save()
            # Get the id of the transaction
            transaction_id = new_transation.transaction_id
            return redirect('core:transfer_confirmation',account.account_number,transaction_id)
        else:
            messages.error(request,'Insufficient Funds.')
            return redirect('core:amount_transfer',account.account_number)
    else:
        messages.error(request,'Error Occured.Try again later!!!')
        return redirect('account:account')




def transfer_confirmation(request,account_number,transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.error(request,'Transaction does not Exist!!!')
        return redirect('account:account')


    context = {
        'account':account,
        'transaction':transaction,
    }
    return render(request,'transfer/transfer_confirmation.html',context)



def transfer_process(request,account_number,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    # admin_account = Account.objects.get

    sender = request.user
    reciever = account.user 

    sender_account = sender.account
    reciever_account = account

    completed = False
    if request.method == 'POST':
        pin_number = request.POST.get('pin_number')
        print(f" pin_numer = {pin_number}")

        if pin_number == sender_account.pin_number:
            transaction.transaction_status = "completed"
            transaction.save()

            # remove the money
            sender_account.account_balance -= transaction.amount
            sender_account.save()

            # add the monney to the reciever after the fee
            reciever_account.account_balance +=  transaction.receiving_amount()
            account.save()

            messages.success(request,'Transfer Successful')
            time.sleep(1)
            return redirect('core:transfer_completed',account.account_number, transaction.transaction_id)
        else:
            messages.error(request,'Incorrect Pin.')
            return redirect('core:transfer_confirmation',account.account_number, transaction.transaction_id)
    else:
        messages.error(request,'An Error Occcured, Try Again Later.')
        return redirect('account:account')


def transfer_completed(request,account_number,transaction_id):
    sender = request.user
    sender_account = sender.account

    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.error(request,'Transfer does not Exist!!!')
        return redirect('account:account')


    context = {
        'account':account,
        'transaction':transaction,
        'sender_account':sender_account
    }
    return render(request,'transfer/transfer_completed.html',context)
