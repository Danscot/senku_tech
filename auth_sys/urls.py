from django.urls import path

from . import views

urlpatterns = [

    path('api/signin/', views.signin, name='signin'),

    path('api/login/', views.login_view, name='login'),  # assuming your login view is called login_view
]
