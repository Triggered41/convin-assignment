from django.urls import path

from . import views
from . import api

urlpatterns = [
    # path("", views.home, name='index'),
    # path("login", views.user_login, name='index'),
    # path("register", views.register_user, name='register user'),
    # path("expense", views.add_expense, name='register user'),

    path("user_login", api.user_login, name='user_login'),
    path("create_user", api.create_user, name='create_user'),
    path("get_user", api.get_user, name='get_user'),
    path("add_expense", api.add_expense, name='add_expense'),
    path("get_expenses/<str:mail>", api.get_user_expenses, name='get_expenses'),
    path("get_all_expenses", api.get_all_expenses, name='get_all_expenses'),
    path("get_overall_expense", api.get_overall_expense, name='get_all_expenses'),
    path("get_balance_sheet", api.get_balance_sheet, name='get_all_expenses'),

]