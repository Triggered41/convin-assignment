from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

# Create your views here.

def home(request: HttpRequest):
    print(request.session.get('user_info', False))
    if not request.session.get('user_info', False): 
        return redirect('/register')   
    return render(request, "index.html")

def user_login(request):
    return render(request, "login.html")

def register_user(request):
    return render(request, "register.html")

def add_expense(request):
    return render(request, 'expense.html')