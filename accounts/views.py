from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Profile

def candidate_register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        user.profile.role = 'CANDIDATE'
        user.profile.save()

        return redirect('login')

    return render(request, 'candidate_register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.profile.role == 'CANDIDATE':
                return redirect('candidate_dashboard')
            else:
                return redirect('hr_dashboard')

    return render(request, 'login.html')
