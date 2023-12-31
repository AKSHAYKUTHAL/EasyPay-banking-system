from django.shortcuts import render, redirect
from account.models import KYC, Account
from account.forms import KYCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import CreditCardForm
from core.models import CreditCard,Notification,History,Transaction
import datetime
from django.contrib.auth import authenticate,login,logout
from userauths.models import User




def account(request): 
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.error(request,'You need to submit your KYC!')
            return redirect('account:kyc_reg')
        
        account = Account.objects.get(user=request.user)
        credit_card = CreditCard.objects.filter(user=request.user).order_by('-id')

        form = CreditCardForm(request.POST)


        month = datetime.datetime.now().month
        year = datetime.datetime.now().year + 5

        if request.method == 'POST':
            form = CreditCardForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.name = request.user.kyc.full_name
                # new_form.amount = request.user.account.account_balance
                new_form.save()

                credit_card_id = new_form.credit_card_id

                Notification.objects.create(
                    user=request.user,
                    notification_type="Added Credit Card",
                    card_number = new_form.format_card_number(),
                    card_type = new_form.card_type,
                    card_tier = new_form.card_tier
                )
                History.objects.create(
                    user=request.user,
                    history_type="Added Credit Card",
                    card_number = new_form.format_card_number(),
                    card_type = new_form.card_type,
                    card_tier = new_form.card_tier
                )

                messages.success(request,'Card Added Successfully.')
                return redirect('account:account')
        else:
            form = CreditCardForm()

    else:
        messages.error(request,'You need to login to access the dashboard')
        return redirect('userauths:sign_in')
    context = {
        'kyc':kyc,
        'account':account,
        'credit_card':credit_card,
        'month':month,
        'year':year,
        'form':form
    }
    return render(request,'account/account.html',context)



def delete_account(request,id):
    account = Account.objects.get(id=id, user=request.user)
    credit_card = CreditCard.objects.filter(user=request.user)

    credit_card_balance = 0

    if request.method == 'POST':
        pin_number = request.POST.get('pin_number')
        
        try:
            for c in credit_card :
                credit_card_balance += c.amount 
        except:
            credit_card_balance = 0


        if account.account_balance <= 0 and account.deleted_account == False :
            if credit_card_balance == 0:

                if pin_number == account.pin_number:
                    account.deleted_account = True
                    account.save()
                    logout(request)
                    messages.success(request,'Your Account has been deleted, For any assistance please contact the Customer Service')
                    return redirect('core:index')
                else:
                    messages.error(request,'Incorrect pin number')
                    return redirect('account:account')
            else:
                messages.error(request,'You have balance amount in one of your cards, Please move the money first,then only try to delete account.')
                return redirect('account:account')
            
        else:
            messages.error(request,'You have balance amount in one your account, Please move the money first.')
            return redirect('')




@login_required
def kyc_registration(request):
    user = request.user
    account = Account.objects.get(user=user)

    try:
        kyc = KYC.objects.get(user=user)
    except:
        kyc = None

    if request.method == 'POST':
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            messages.success(request, 'KYC Form submitted successsfully. In review now!')
            return redirect('core:index')
    else:
        form = KYCForm(instance=kyc)
    context = {
        'account':account,
        'form':form,
        'kyc':kyc,
    }
    return render(request, 'account/kyc_form.html',context)



def dashboard(request):
    sent_transaction = Transaction.objects.filter(sender=request.user,transaction_type='transfer').order_by('-id')
    recieved_transaction = Transaction.objects.filter(reciever=request.user,transaction_type='transfer').exclude(transaction_status='cancelled').order_by('-id')

    sent_transaction_count = sent_transaction.count()
    recieved_transaction_count = recieved_transaction.count()

    request_sent_transaction = Transaction.objects.filter(sender=request.user, transaction_type="request").order_by('-id')
    request_recieved_transaction = Transaction.objects.filter(reciever=request.user, transaction_type="request").exclude(transaction_status='request_processing').order_by('-id')

    request_sent_transaction_count = request_sent_transaction.count()
    request_recieved_transaction_count = request_recieved_transaction.count()

    month = datetime.datetime.now().month
    year = datetime.datetime.now().year + 5
    

    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.error(request,'You need to sumbit your KYC!')
            return redirect('account:kyc_reg')
        
        account = Account.objects.get(user=request.user)
        credit_card = CreditCard.objects.filter(user=request.user).order_by('-id')

        if request.method == 'POST':
            form = CreditCardForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.name = request.user.kyc.full_name
                # new_form.amount = request.user.account.account_balance
                new_form.save()

                credit_card_id = new_form.credit_card_id

                Notification.objects.create(
                    user=request.user,
                    notification_type="Added Credit Card",
                    card_number = new_form.format_card_number(),
                    card_type = new_form.card_type,
                    card_tier = new_form.card_tier
                )
                History.objects.create(
                    user=request.user,
                    history_type="Added Credit Card",
                    card_number = new_form.format_card_number(),
                    card_type = new_form.card_type,
                    card_tier = new_form.card_tier
                )

                messages.success(request,'Card Added Successfully.')
                return redirect('account:dashboard')
        else:
            form = CreditCardForm()

    else:
        messages.error(request,'You need to login to access the dashboard')
        return redirect('userauths:sign_in')
    
    context = {
        'kyc':kyc,
        'account':account,
        'form':form,
        'month':month,
        'year':year,
        'credit_card':credit_card,
        "sent_transaction":sent_transaction,
        "recieved_transaction":recieved_transaction,
        'request_sent_transaction':request_sent_transaction,
        'request_recieved_transaction':request_recieved_transaction,

        'sent_transaction_count':sent_transaction_count,
        'recieved_transaction_count':recieved_transaction_count,
        'request_sent_transaction_count':request_sent_transaction_count,
        'request_recieved_transaction_count':request_recieved_transaction_count


    }
    return render(request,'account/dashboard.html',context)


def is_2fa(request):
    user = request.user
    
    if user.is_2fa == True:
        user.is_2fa = False
        user.save()
        messages.success(request,'You disabled the 2FA')
        return redirect('account:account')
    else:
        user.is_2fa = True
        user.save()
        messages.success(request,'You Enabled the 2FA')
        return redirect('account:account')

