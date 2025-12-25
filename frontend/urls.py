from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('account/', views.account, name='account'),

    path('login', views.login_page, name='login'),

    path('signup', views.signup, name='signup'),

    path('account/ver', views.ver, name='ver'),

    path("logout/", views.web_logout, name="web_logout"),

]
