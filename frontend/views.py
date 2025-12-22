from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

def index(request):

    return render(request, 'index.html')

@login_required(login_url='login')
def dashboard(request):

    user = request.user

    user.update()

    coins = user.coins

    return render(request, 'dashboard.html', {

        "coin":coins,
        
        })

@login_required(login_url='login')
def account(request):

    user = request.user
    
    user.update()

    return render(request, 'account.html', {

        "username":user.username,
        "email":user.email,
        "bot_num":user.bot_number,
        "bot_exp":user.bot_exp
        })


def login(request):
    return render(request, "login.html")

def signup(request):

	return render(request, 'signup.html')