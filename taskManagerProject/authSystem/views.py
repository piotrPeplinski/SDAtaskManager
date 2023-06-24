from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re
from verify_email.email_handler import send_verification_email
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'form': RegisterForm()})
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # sprawdzenie czy hasla sa takie same
        if password2 == password1:
            # sprawdzenie czy username, email jest wolny
            emailTaken = User.objects.filter(email=email).exists()
            usernameTaken = User.objects.filter(username=username).exists()

            if emailTaken:
                error = 'This email is already taken. Try again.'
            if usernameTaken:
                error = 'This username is already taken. Try again.'

            # walidacja hasla
            if not emailTaken and not usernameTaken:
                try:
                    validate_password(password2)
                except ValidationError as e:
                    return render(request, 'register.html', {'form': RegisterForm(), 'passError': e.messages})
                else:
                    # walidacja maila
                    emailValid = validate_email(email)
                    if emailValid:
                        # wyslanie potwierdzenia na maila
                        # stworzenie usera
                        user = User.objects.create_user(
                            username=username, email=email, password=password1)
                        return render(request, 'register.html', {'form': RegisterForm()})
                    else:
                        error = f'{email} is not a valid email. Try again.'
        else:
            error = 'Passwords did not match. Try again.'

        return render(request, 'register.html', {'form': RegisterForm(), 'error': error})


def logUser(request):
    if request.method == 'GET':
        return render(request, 'logUser.html', {'form': AuthenticationForm()})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:  # poprawne logowanie
            login(request, user)
            return redirect('home')
        else:
            usernameExists = User.objects.filter(username=username).exists()
            if usernameExists:
                error = 'Incorrect password.'
            else:
                error = f'User with username {username} could not be found.'
            return render(request, 'logUser.html', {'form': AuthenticationForm(),'error':error})
        
def logoutUser(request):
    logout(request)
    return redirect('home')