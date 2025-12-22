from django.urls import path

from . import views

urlpatterns = [

    path('api', views.root, name='root'),

    path('specs', views.system_usage, name="specs"),

    path('list', views.list_sessions, name="list"),

    path('pair', views.pairing, name="pairing")

]
