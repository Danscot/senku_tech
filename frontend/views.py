from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout

from django.http import JsonResponse

def index(request):

    return render(request, 'index.html')

@login_required(login_url='signup')
def dashboard(request):

    user = request.user

    user.update()

    coins = user.coins

    return render(request, 'dashboard.html', {

        "coin":coins,
        
        })

@login_required(login_url='signup')
def account(request):

    user = request.user
    
    user.update()

    return render(request, 'account.html', {

        "username":user.username,
        "email":user.email,
        "bot_num":user.bot_number,
        "bot_exp":user.bot_exp,
        "is_verified": user.email_ver,
        })


def login_page(request):
    return render(request, "login.html")

def signup(request):

	return render(request, 'signup.html')

@login_required(login_url='signup')
def ver(request):

    user = request.user

    return render(request, 'ver.html', {

        "email":user.email

    })

@login_required

def web_logout(request):

    if request.method == "POST":

        logout(request)

    return redirect("login")