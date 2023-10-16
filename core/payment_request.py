from django.shortcuts import render, redirect
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from core.models import Transaction
import time
from decimal import Decimal





@login_required
def request_payment_search_account(request):
    account = Account.objects.all()
    query = request.POST.get('account_number')

    if query:
        account = account.filter(
            Q(account_number=query) |
            Q(account_id=query)
        ).distinct()

    context = {
        'account':account,
        'query':query
    }

    return render(request,'payment_request/search_users.html',context)


@login_required
def amount_request(request,account_number):
    account = Account.objects.get(account_number=account_number)

    context = {
        'account':account,
    }

    return render(request,'payment_request/amount_request.html',context)



def amount_request_process(request, account_number):
    account = Account.objects.get(account_number=account_number)

    sender = request.user
    reciever = account.user

    sender_account = request.user.account
    reciever_account = account

    if request.method == "POST":
        amount = request.POST.get("amount_request")
        description = request.POST.get("description")

        new_request = Transaction.objects.create(
            user=request.user,
            amount=amount,
            description=description,

            sender=sender,
            reciever=reciever,

            sender_account=sender_account,
            reciever_account=reciever_account,

            transaction_status="request_processing",
            transaction_type="request"
        )
        new_request.save()
        transaction_id = new_request.transaction_id
        return redirect("core:amount_request_confirmation", account.account_number, transaction_id)
    else:
        messages.warning(request, "Error Occured, try again later.")
        return redirect("account:dashboard")




def amount_request_confirmation(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except Transaction.DoesNotExist:
        messages.error(request,'Transaction does not exist')
        return redirect('core:request_payment_search_account')


    context = {
        "account":account,
        "transaction":transaction,
    }
    return render(request, "payment_request/amount_request_confirmation.html", context)



def amount_request_final_process(request, account_number,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    if request.method == 'POST':
        pin_number = request.POST.get('pin_number')
        if pin_number == request.user.account.pin_number:
            transaction.transaction_status = 'request_sent'
            transaction.save()

            messages.success(request,'Your payment request have been sent successfully. ')
            time.sleep(1)
            return redirect('core:amount_request_completed',account.account_number,transaction.transaction_id)
        else:
            messages.error(request,'Wrong Pin Number')
            return redirect('core:amount_request_confirmation',account.account_number,transaction.transaction_id)
        
    else:
        messages.error(request,'An Error Occured!,Try Again Later.')
        return redirect('account:dashboard')

    

def amount_request_completed(request,account_number,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    context = {
        "account":account,
        "transaction":transaction,
    }
    return render(request, "payment_request/amount_request_completed.html", context)


def request_details_sent(request,transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    context = {
        "transaction":transaction,
    }
    return render(request, "payment_request/request_details_sent.html", context)



def request_details_received(request,transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    context = {
        "transaction":transaction,
    }
    return render(request, "payment_request/request_details_received.html", context)

##################### Settle request ###################




def request_settlement_confirmation(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    sender_account = request.user.account
    payment_with_fee_decimal = Decimal(transaction.payment_with_fee())  # Convert to Decimal if necessary

    if sender_account.account_balance <= payment_with_fee_decimal:
        difference = payment_with_fee_decimal - sender_account.account_balance
        messages.error(request, f"You have insufficient balance. You need ₹{difference} more to process this payment.")
        return redirect('core:transactions')

    context = {
        "account": account,
        "transaction": transaction,
    }
    return render(request, "payment_request/request_settlement_confirmation.html", context)






def request_settlement_processing(request,account_number,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    sender_account = request.user.account

    if request.method == 'POST':
        pin_number = request.POST.get('pin_number')
        if pin_number == sender_account.pin_number:
            if sender_account.account_balance <= 0 or sender_account.account_balance < transaction.payment_with_fee():
                messages.error(request,'Insufficient Funds, Fund your accont and try agin.')
            else:
                sender_account.account_balance -= transaction.payment_with_fee()
                sender_account.save()

                account.account_balance += transaction.amount
                account.save()

                transaction.transaction_status = 'request_settled'
                transaction.save()
                messages.success(request,f"Settled to {account.user.kyc.full_name} was successful.")
                time.sleep(1)
                return redirect('core:request_settlement_completed',account.account_number,transaction.transaction_id)
        else:
            messages.error(request,'Incorrect Pin')
            return redirect('core:request_settlement_confirmation', account.account_number, transaction.transaction_id)
    else:
            messages.error(request,'Error Ocuured')
            return redirect('account:dashboard')

            




def request_settlement_completed(request,account_number,transaction_id):
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
    return render(request,'payment_request/request_settlement_completed.html',context)

