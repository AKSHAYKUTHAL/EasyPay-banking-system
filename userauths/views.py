from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from userauths.models import User
from django.views.decorators.csrf import csrf_protect
from django.db import IntegrityError



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
            user = authenticate(request, email=email,password=password)

            if user is not None:
                login(request,user)
                messages.get_messages(request).used = True
                messages.success(request,'You are logged in successfully.')
                return redirect('account:account')
            else:
                messages.get_messages(request).used = True
                messages.error(request,'Incorrect Email or password.')
                return redirect('userauths:sign_in')
        except User.DoesNotExist:
            messages.error(request,'User does not exist.')
        except ValidationError as e:
            messages.error(request, str(e))
    if request.user.is_authenticated:
        messages.get_messages(request).used = True
        messages.error(request,'You are already logged in.')
        return redirect('account:account')

    return render(request,'userauths/sign_in.html')


def logout_view(request):
    logout(request)
    messages.get_messages(request).used = True
    messages.success(request,'You have been logged out.')
    return redirect('userauths:sign_in')