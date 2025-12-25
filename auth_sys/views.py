
from rest_framework.decorators import api_view

from rest_framework.response import Response

from rest_framework import status

from .models import CustomUser

from django.contrib.auth import authenticate, login, logout

from rest_framework.decorators import api_view

from rest_framework.response import Response

from rest_framework import status

from .emailer import Email

import random


def gen_code(user):

    code = random.randint(100000, 999999)

    try:
        
        emailer = Email(code, user.email)

        emailer.send_verification_code()

        return code

    except Exception as e:

        return str(e)

@api_view(["POST"])

def signin(request):

    username = request.data.get("username")

    email = request.data.get("email")

    password = request.data.get("password")

    # Validation
    if not username or not password:

        return Response(

            {
                "status": "error",

                "message": "Username and password are required"

            },

            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if user exists
    if (CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists()):

        return Response(

            {
                "status": "ok",

                "message": "User already exists"
            },

            status=status.HTTP_200_OK
        )

    try:

        user = CustomUser.objects.create_user(

            username=username,

            email=email,

            password=password
        )

        user.is_prem = False

        user.coins = 0

        user.ver_code = gen_code(user)

        user.attempts += 1

        user.save()

        user = authenticate(username=username, password=password)

        login(request, user)

        return Response(

            {
                "status": "created",

                "message": "User created successfully"

            },

            status=status.HTTP_201_CREATED
        )

    except Exception as e:

        return Response(


            {
                "status": "error",

                "message": str(e)
            },

            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])

def login_view(request):

    username = request.data.get("username")

    password = request.data.get("password")

    if not username or not password:

        return Response(

            {"status": "error", "message": "Username and password required"},

            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)
 
    if user is not None:

        login(request, user)

        return Response(

            {
                "status": "ok",

                "message": "Login successful",
            },

            status=status.HTTP_200_OK
        )

    else:

        return Response(

            {"status": "error", "message": "Invalid credentials"},

            status=status.HTTP_401_UNAUTHORIZED
        )



@api_view(["POST"])

def email_verification(request):

    code = request.data.get("code")

    user = request.user

    if user.attempts >= 4:

        user.delete()

        return Response({

            "status": "deleted",

            "message": "Your Account was deleted because you failed to verify your email"


            },
            status=status.HTTP_403_FORBIDDEN

        )
        
    try:

        if int(code) != user.ver_code:

            user.ver_code = gen_code(user)

            user.attempts += 1

            user.save()
            
            return Response({

                "status": "failed",

                "message":"Wrong code, A new code has been sent to your email.",

                "attempts": user.attempts

                },

            status=status.HTTP_200_OK
        )

        user.attempts = 0

        user.ver_code = None

        user.email_ver = True

        user.save()

        return Response({

            "status":"ok",

            "message": "Verification successful"
            },


            status=status.HTTP_200_OK
        )

    except Exception as e:

        return Response({

            "status":"error",

            "message": str(e)
            },


            status=status.HTTP_500_INTERNAL_SERVER_ERROR

        )


@api_view(["POST"])

def user_logout(request):

    try:
    
        logout(request)

        return Response({

            "status":"ok",

            "message":"User logout successfully"
            },

        status=status.HTTP_200_OK
    )

    except Exception as e:

        return Response({

            "status":"error",

            "message": str(e)
            },

        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )