from django.shortcuts import render, redirect
from account.models import KYC, Account
from account.forms import KYCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import CreditCardForm
from core.models import CreditCard
import datetime



def account(request): 
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.error(request,'You need to sumit your KYC!')
            return redirect('account:kyc_reg')
        
        account = Account.objects.get(user=request.user)
    else:
        messages.error(request,'You need to login to access the dashboard')
        return redirect('userauths:sign_in')
    context = {
        'kyc':kyc,
        'account':account
    }
    return render(request,'account/account.html',context)

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
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year + 5

    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.error(request,'You need to sumit your KYC!')
            return redirect('account:kyc_reg')
        
        account = Account.objects.get(user=request.user)
        credit_card = CreditCard.objects.filter(user=request.user)

        if request.method == 'POST':
            form = CreditCardForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.name = request.user.kyc.full_name
                # new_form.amount = request.user.account.account_balance
                new_form.save()

                card_id = new_form.card_id
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
    }
    return render(request,'account/dashboard.html',context)
