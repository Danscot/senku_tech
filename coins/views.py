from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from rest_framework import status


@api_view(["POST"])

@permission_classes([IsAuthenticated])

def addcoin(request):

    user = request.user

    success, msg = user.add_coins(amount=1)

    if not success:
  
        return Response({

            "status": "limit",

            "message": msg,

            "coins": user.coins,

            "remaining": max(0, 10 - user.daily_ad_count),

            "reset_at": user.daily_ad_reset
        })

    return Response({

        "status": "ok",

        "coins": user.coins,

        "remaining": 10 - user.daily_ad_count,
        
        "reset_at": user.daily_ad_reset
    })


@api_view(["POST"])

@permission_classes([IsAuthenticated])

def usecoin(request):

    user = request.user

    amount = request.data.get("amount")

    try:

        amount = int(amount)

        if amount <= 0:

            raise ValueError

    except (TypeError, ValueError):

        return Response(

            {"status": "error", "message": "Invalid amount"},

            status=status.HTTP_400_BAD_REQUEST
        )

    user.spend_coins(amount)

    return Response(
        {
            "status": "ok",

            "message": "Coins updated successfully",

            "coins": user.coins
        },
        
        status=status.HTTP_200_OK
    )
