from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect,get_object_or_404
from userauths.forms import UserRegisterForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from userauths.models import User
from django.views.decorators.csrf import csrf_protect
from django.db import IntegrityError
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage




@csrf_protect
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already taken.')
                else:
                    try:
                        User.objects.create_user(username=username, email=email, password=password1)
                        messages.success(request, f"Hey {username}, your account is created successfully")
                        new_user = authenticate(username=email, password=password1)
                        login(request, new_user)
                        return redirect('account:account')
                    except IntegrityError as e:
                        messages.error(request, 'Email is already taken.')
            else:
                messages.error(request, "Passwords do not match")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == 'password1':
                        messages.error(request, f"Password: {error}")
                    elif field == 'password2':
                        if error == 'The two password fields didn’t match.' or error == 'This password is too short. It must contain at least 8 characters.' or error == 'This password is too common.' or error == 'This password is entirely numeric.' :
                            messages.error(request, f"{error}")
                        else:
                            messages.error(request, f"Confirm password: {error}")
                    else:
                        messages.error(request, f"{field}: {error}")


    if request.user.is_authenticated:
        messages.error(request, "You are already logged in.")
        return redirect("account:account")
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'userauths/sign_up.html', context)



@csrf_protect
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                account = Account.objects.get(user=user)
                if account.deleted_account:
                    messages.error(request, 'The account is not usable anymore. Please contact customer service for any assistance.')
                    return redirect('userauths:sign_in')

                login(request, user)
                messages.get_messages(request).used = True
                messages.success(request, 'You are logged in successfully.')
                return redirect('account:account')
            else:
                messages.get_messages(request).used = True
                messages.error(request, 'Incorrect Email or password.')
                return redirect('userauths:sign_in')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
        except ValidationError as e:
            messages.error(request, str(e))

    if request.user.is_authenticated:
        messages.get_messages(request).used = True
        messages.error(request, 'You are already logged in.')
        return redirect('account:account')

    return render(request, 'userauths/sign_in.html')


def logout_view(request):
    logout(request)
    messages.get_messages(request).used = True
    messages.success(request,'You have been logged out.')
    return redirect('userauths:sign_in')


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request,'Password updated successfully.')
                return redirect('account:account')   
            else:
                messages.error(request,'Please enter a valid current password')  
                return redirect('account:account')   
        else:
            messages.error(request,'The new passwords do not match')
            return redirect('account:account')   



def forgot_password(request):

    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = 'Resest Your Password'
            message = render_to_string('userauths/reset_password_email.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Password reset email has been sent to your email address.')
            return redirect('userauths:sign_in')
        else:
            messages.error(request,'Account Does Not Exist.')
            return redirect('userauths:forgot_password')


    return render(request,'userauths/forgot_password.html')



def reset_password_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request,'Please Reset Your Password')
        return redirect('userauths:reset_password')
    else:
        messages.error(request,'This link has been expired')
        return redirect('userauths:sign_in')
    



def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(new_password)
            user.save()
            messages.success(request,'Password changed successfully')
            return redirect('userauths:sign_in')
        else:
            messages.error(request,'Passwords do not match!')
            return redirect('reset_password')
        
    else:
        return render(request,'userauths/reset_password.html')
