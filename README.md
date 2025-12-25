# Senku Tech Project

A Django-based bot management and coin reward system.

## Features

- Bot management (pairing, session management)
- Coin system with ad rewards
- API endpoints using Django REST Framework
- Daily ad limit and reward system
- Admin panel (under development)

## Requirements

- Python 
- Django 
- Node.js ( WhatsApp bot)

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Danscot/senku_tech.git
   cd senku_tech
```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup variables**:

   ```env
   DEBUG=0
   ALLOWED_HOSTS='yourdomain.com,127.0.0.1'
   ```

5. **Migrate the database:**

   ```bash
   python manage.py migrate
   ```

6. **Collect static files:**

   ```bash
   python manage.py collectstatic
   ```

7. **Run development server:**

   ```bash
   python manage.py runserver
   ```

## Deployment

* Use **Gunicorn** or **Daphne** to serve Django in production.
* Use **Nginx** as a reverse proxy to serve static files and handle HTTPS.
```