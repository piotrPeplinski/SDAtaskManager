from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.models import User


def fieldTaken(fieldName):
    return User.objects.filter(fieldName=fieldName).exists()


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
                
            if not emailTaken and not usernameTaken:
                return render(request, 'register.html', {'form': RegisterForm(), 'data': [emailTaken, usernameTaken]})
        else:
            error = 'Passwords did not match. Try again.'
        return render(request, 'register.html', {'form': RegisterForm(), 'error': error})
        # walidacja hasla
        # walidacja maila
        # wyslanie potwierdzenia na maila
