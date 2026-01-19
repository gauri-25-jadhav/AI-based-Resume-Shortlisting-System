from django.shortcuts import render, redirect

def welcome(request):
    return render(request, 'welcome.html')

def login_selection(request):
    return render(request, 'login_selection.html')

def candidate_login(request):
    if request.method == "POST":
        return redirect('candidate_dashboard')
    return render(request, 'login.html')

def hr_login(request):
    if request.method == "POST":
        return redirect('hr_dashboard')
    return render(request, 'login.html')

def candidate_dashboard(request):
    return render(request, 'candidate_dashboard.html')

def hr_dashboard(request):
    return render(request, 'hr_dashboard.html')
