from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name='index'),
    path("login", views.user_login, name='index'),
    path("register", views.register_user, name='register user'),
    path("expense", views.add_expense, name='register user'),
]