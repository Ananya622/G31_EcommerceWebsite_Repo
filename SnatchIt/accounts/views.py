from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Redirect based on group
            if user.groups.filter(name__in=['Admin', 'Approved Brand']).exists():
                return redirect('admin_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        country = request.POST.get('country')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = full_name
        user.save()

        # Optionally assign a group
        default_group, created = Group.objects.get_or_create(name='Normal User')
        user.groups.add(default_group)

        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login')

    return render(request, 'accounts/register.html')


def logout_view(request):
    logout(request)
    return redirect('dashboard')
