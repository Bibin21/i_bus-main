from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from apps.user.forms import UserSignUpForm, UserLoginForm
from apps.college.models import CollegeStudent, CollegeStaff

# Create your views here.


def landing_page(request):
    """View to display landing page"""

    return render(
        request, 'index.html',
    )


def signup(request):
    """View for signup."""
    form = UserSignUpForm()

    if request.method == "POST":
        form = UserSignUpForm(request.POST)

        if form.is_valid():
            user_type = form.cleaned_data['user_type']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # If user is a student
            if user_type == 0:
                student = CollegeStudent.objects.filter(email=email)

                if student.count():
                    form.save()
                    user = authenticate(email=email, password=password)
                    dj_login(request, user)

                    return redirect("home")
                else:
                    messages.error(request, "Sorry! You are not a student of this college.")

                    return redirect("signup")
            # If user is a staff
            elif user_type == 1:
                staff = CollegeStaff.objects.filter(email=email)

                if staff.count():
                    form.save()
                    user = authenticate(email=email, password=password)
                    dj_login(request, user)

                    return redirect("home")
                else:
                    messages.error(request, "Sorry! You are not a staff of this college.")

                    return redirect("signup")

    return render(
        request, 'signup.html', {'form': form}
    )


def login(request):
    """View for login."""
    form = UserLoginForm()

    if request.method == "POST":        
        form = UserLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(email=email, password=password)

            if user:
                dj_login(request, user)

                return redirect("home")
            else:
                messages.error(request, "Invalid password")

                return redirect("login")
            
    return render(
        request, 'login.html', {'form': form}
    )

