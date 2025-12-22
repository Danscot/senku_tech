from django.urls import path

from . import views

urlpatterns = [

	path("api/coins/add/", views.addcoin, name="addcoin"),

	path("api/coins/use/", views.usecoin, name="usecoin"),

]
