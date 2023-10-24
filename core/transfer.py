from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from account.models import Account,KYC
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from core.models import Transaction,Notification,History
import time
from decimal import Decimal

import pdfkit

config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")




@login_required
def search_users_account_number(request):

    try:
        kyc = KYC.objects.get(user=request.user)
    except:
        messages.error(request,'You need to submit your KYC!')
        return redirect('account:kyc_reg')
    
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
        return redirect('account:dashboard')




def transfer_confirmation(request,account_number,transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.error(request,'Transaction does not Exist!!!')
        return redirect('account:dashboard')


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
        if transaction.transaction_status != 'completed':

            pin_number = request.POST.get('pin_number')

            if pin_number == sender_account.pin_number:
                transaction.transaction_status = "completed"
                transaction.save()

                # remove the money
                sender_account.account_balance -= transaction.amount
                sender_account.save()

                # add the monney to the reciever after the fee
                reciever_account.account_balance +=  transaction.receiving_amount()
                account.save()

                Notification.objects.create(
                    amount=transaction.receiving_amount(),
                    user=account.user,
                    notification_type="Credit Alert",
                    sender = request.user,
                    receiver = account.user,
                    transaction_id = transaction.transaction_id
                )
                History.objects.create(
                    amount=transaction.receiving_amount(),
                    user=account.user,
                    history_type="Credit Alert",
                    sender = request.user,
                    receiver = account.user,
                    transaction_id = transaction.transaction_id
                )
                
                Notification.objects.create(
                    user=sender,
                    notification_type="Debit Alert",
                    amount=transaction.amount,
                    sender = request.user,
                    receiver = account.user,
                    transaction_id = transaction.transaction_id
                )
                History.objects.create(
                    user=sender,
                    history_type="Debit Alert",
                    amount=transaction.amount,
                    sender = request.user,
                    receiver = account.user,
                    transaction_id = transaction.transaction_id
                )


                messages.success(request,'Transfer Successful')
                time.sleep(1)
                return redirect('core:transfer_completed',account.account_number, transaction.transaction_id)
            else:
                messages.error(request,'Incorrect Pin.')
                return redirect('core:transfer_confirmation',account.account_number, transaction.transaction_id)
        else:
            messages.error(request,'You already completed this transaction')
            return redirect('core:search_account')
    else:
        messages.error(request,'An Error Occcured, Try Again Later.')
        return redirect('account:account')


def cancel_transfer(request,account_number,transaction_id):
    try:
        account = Account.objects.get(user=request.user,account_number=account_number)
        transaction = Transaction.objects.get(user=request.user,transaction_id=transaction_id)

        transaction.transaction_status = 'cancelled'
        transaction.save()
        messages.success(request,'Transaction cancelled successfully')
        return redirect('account:dashboard')
    except:
        messages.error(request,'Error occured when obtaining transaction, Try again later.')
        return redirect('account:dashboard')




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



# def transfer_completed_pdf(request,transaction_id):
#     pdf = pdfkit.from_url(request.build_absolute_uri(reverse('core:transaction_detail_sent',args=[account_number,transaction_id])), False, configuration=config)
#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="request.user.kyc.full_name"'

#     return response