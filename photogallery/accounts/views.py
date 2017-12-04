from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def signup(request):
    if request.method == 'POST':
        if request.POST['username'] != "":
            if request.POST['password1'] != "" and request.POST['password2'] != "":
                if request.POST['password1'] == request.POST['password2']:
                    try:
                        user = User.objects.get(username=request.POST['username'])
                        return render(request, 'accounts/signup.html', {'error':'Username has alredy been taken'})
                    except User.DoesNotExist:
                        user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                        login(request, user)
                        return redirect('home')
                else:
                    return render(request, 'accounts/signup.html', {'error':'Passwords didn\'t match'})
            else:
                return render(request, 'accounts/signup.html', {'error': 'Don\'t leave password fields blank'})
        else:
            return render(request, 'accounts/signup.html', {'error': 'Choose a user name'})
    else:
        return render(request, 'accounts/signup.html')


def loginview(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error':'The Username and Password didn\'t match'})
    else:
        return render(request, 'accounts/login.html')



def logoutview(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

