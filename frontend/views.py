from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout

from django.http import JsonResponse

from auth_sys.views import gen_code 

from django.contrib import messages

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

    if request.method == "POST" and not user.email_ver:

        user.ver_code = gen_code(user)

        user.save()

        return redirect('ver') 

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

    try:

        return render(request, 'ver.html', {

            "email":user.email

        })
    
    except Exception as e:
        # Log error (important in prod)
        print("Verification error:", e)

        messages.error(request, "Something went wrong. Try again later.")

        return redirect("account")  # or any safe page

@login_required

def web_logout(request):

    if request.method == "POST":

        logout(request)

    return redirect("login")