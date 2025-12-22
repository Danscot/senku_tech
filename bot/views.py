from rest_framework.decorators import api_view

from rest_framework.response import Response

from rest_framework.exceptions import ValidationError

from rest_framework import status

from django.db import transaction

from datetime import datetime

import subprocess

import psutil

import platform

import re

import time

from auth_sys.models import CustomUser

# ----------------------------
# Utility functions
# ----------------------------
def clean_number(raw: str) -> str:

    cleaned = re.sub(r"[ \+\-\(\)]", "", raw)
    
    if not cleaned.isdigit():

        raise ValidationError("Invalid number: must contain digits only")
    
    if len(cleaned) < 7 or len(cleaned) > 15:

        raise ValidationError("Invalid number: length must be between 7 and 15 digits")
    
    return cleaned

def to_gb(bytes_value):

    return round(bytes_value / (1024 ** 3), 2)  # Convert bytes → GB


def get_user(username):

    user = CustomUser.objects.filter(username=username).first()

    if not user:

        return 0  # or None

    return user

# ----------------------------
# ----------------------------

@api_view(["GET"])

def root(request):

    return Response({"status": "Ok", "message": "Bot API System Is Running"})

@api_view(["POST"])

def pairing(request):

    target = clean_number(request.data.get("number"))

    if not target:

        return Response(

            {"status": "Failed", "message": "Missing username or number"},

            status=status.HTTP_400_BAD_REQUEST
        )

    user = request.user

    if not user:

        return Response(

            {"status": "Failed", "message": "User not found"},

            status=status.HTTP_404_NOT_FOUND
        )

    user.update()

    duration = int(time.time()) + 172800

    dt = datetime.fromtimestamp(duration)

    formatted = dt.strftime("%Y-%m-%d %H:%M:%S")

    bot_name = f"session-{target}"

    bot_path = "web-paire.js"

    cmd = (

        f'NUMBER="{target}" '

        f'PM2_PROCESS_NAME="{bot_name}" '

        f'DURATION="{duration}" '

        f'pm2 start {bot_path} --name "{bot_name}"'
    )

    try:

        with transaction.atomic():

            # Spend coins safely
            if not user.spend_coins(10):

                return Response(

                    {
                        "status": "Failed",

                        "message": "Insufficient coin balance (need 10 coins)"
                    },

                    status=status.HTTP_403_FORBIDDEN
                )

            result = subprocess.run(

                cmd,

                shell=True,

                cwd="wa_bot/senku",

                capture_output=True,

                text=True
            )

            if result.returncode != 0:

                raise RuntimeError(result.stderr)

    except Exception as e:

        return Response(

            {
                "status": "Error",

                "message": str(e)
            },

            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    user.bot_number = target

    user.bot_exp = formatted

    user.save()

    return Response(

        {
            "status": "Launched",

            "number": target,

            "process": bot_name,

            "expires_at": duration,

            "code":"DEVSENKU",

            "coins": user.coins
        },

        status=status.HTTP_201_CREATED
    )


@api_view(["GET"])

def list_sessions(request):

    try:

        result = subprocess.run(["pm2", "list"], capture_output=True, text=True)

        output = result.stdout

    except Exception:

        return Response({"error": "Failed to run PM2"}, status=500)

    sessions = []

    for line in output.splitlines():

        if "session-" in line:

            parts = line.split()

            if len(parts) >= 4:

                sessions.append({

                    "pm_id": parts[0],

                    "name": parts[1],

                    "status": parts[3]
                })

    return Response({"count": len(sessions), "sessions": sessions})

@api_view(["GET"])

def system_usage(request):

    # CPU
    cpu_percent = psutil.cpu_percent(interval=0.5)

    cpu_cores = psutil.cpu_count(logical=True)

    # RAM
    ram = psutil.virtual_memory()

    ram_total_gb = to_gb(ram.total)

    ram_used_gb = to_gb(ram.used)

    ram_percent = ram.percent

    # Disk
    disk = psutil.disk_usage('/')

    disk_total_gb = to_gb(disk.total)

    disk_used_gb = to_gb(disk.used)

    disk_percent = disk.percent

    # Network
    net = psutil.net_io_counters()
    
    bytes_sent = net.bytes_sent

    bytes_recv = net.bytes_recv

    # Uptime
    
    boot_time = psutil.boot_time()
    
    uptime_seconds = int(time.time() - boot_time)

    # System info
    
    system = platform.system()
    
    release = platform.release()
    
    machine = platform.machine()

    
    return Response({
    
        "cpu": {"usage_percent": cpu_percent, "cores": cpu_cores},
    
        "ram": {"total_gb": ram_total_gb, "used_gb": ram_used_gb, "usage_percent": ram_percent},
    
        "disk": {"total_gb": disk_total_gb, "used_gb": disk_used_gb, "usage_percent": disk_percent},
    
        "network": {"bytes_sent": bytes_sent, "bytes_received": bytes_recv},
    
        "uptime_seconds": uptime_seconds,
    
        "system_info": {"os": system, "release": release, "arch": machine}
    })
