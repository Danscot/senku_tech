
from rest_framework.decorators import api_view

from rest_framework.response import Response

from rest_framework import status

from .models import CustomUser

from django.contrib.auth import authenticate, login

from rest_framework.decorators import api_view

from rest_framework.response import Response

from rest_framework import status



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

        user.save()

        login(request, user)

        user = authenticate(username=username, password=password)

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
