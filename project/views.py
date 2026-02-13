from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    """Главная страница"""
    return render(request, 'home.html')

def login_view(request):
    """Обработка входа"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
            return redirect('home')
    
    return redirect('home')

def logout_view(request):
    """Обработка выхода"""
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы')
    return redirect('home')