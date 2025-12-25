from django.urls import path

from . import views

urlpatterns = [

    path('api/signin/', views.signin, name='signin'),

    path('api/login/', views.login_view, name='login'),

    path('api/logout/', views.user_logout, name="logout"),

    path('api/email/ver', views.email_verification, name="email_ver")
]
