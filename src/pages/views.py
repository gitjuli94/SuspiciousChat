from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied
from django.middleware.csrf import get_token
from django.http import HttpRequest

# Login view
def login_view(request: HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            request.session["user_id"] = user.id
            request.session["user_name"] = user.username
            request.session["user_role"] = getattr(user, "role", 0)  # Optional: If role is implemented
            request.session["csrf_token"] = get_token(request)  # Set CSRF token in session
            return redirect("/")  # Redirect to the homepage
        else:
            return render(request, "error.html", {"message": "Invalid username or password."})
    return render(request, "index.html")  # Render the login page for GET requests

# Logout view
def logout_view(request: HttpRequest):
    django_logout(request)
    request.session.flush()  # Clears all session data
    return redirect("/")  # Redirect to the homepage after logout

# Registration view
def register_view(request: HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 != password2:
            return render(request, "error.html", {"message": "Passwords do not match."})
        try:
            user = User.objects.create_user(username=username, password=password1)
            # Automatically log in the user after registration
            django_login(request, user)
            return redirect("/")  # Redirect to the homepage after successful registration
        except IntegrityError:
            return render(request, "error.html", {"message": "Username already exists."})
    return render(request, "register.html")  # Render the registration page for GET requests

# Require a specific user role (utility function)
def require_role(request: HttpRequest, role: int) -> None:
    user_role = request.session.get("user_role", 0)
    if not request.user.is_authenticated or role > user_role:
        raise PermissionDenied()

# Check CSRF token (utility function)
def check_csrf(request: HttpRequest) -> None:
    session_token = request.session.get("csrf_token", "")
    form_token = request.POST.get("csrf_token", "")
    if session_token != form_token:
        raise PermissionDenied("CSRF token mismatch")
