from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.middleware.csrf import get_token
from django.http import HttpRequest

# User authentication - login
def login(request: HttpRequest, name: str, password: str) -> bool:
    user = authenticate(request, username=name, password=password)
    if user is not None:
        django_login(request, user)
        request.session["user_id"] = user.id
        request.session["user_name"] = user.username
        request.session["user_role"] = getattr(user, "role", 0)  # Optional: If role is implemented
        request.session["csrf_token"] = get_token(request)  # Set CSRF token in session
        return True
    return False

# User authentication - logout
def logout(request: HttpRequest) -> None:
    django_logout(request)
    request.session.flush()  # Clears all session data

# User registration
def register(request: HttpRequest, name: str, password: str, role: int = 0) -> bool:
    try:
        user = User.objects.create_user(username=name, password=password)
        user.role = role  # Optional: If role is implemented, extend User model
        user.save()
        # Automatically log in the user after registration
        login(request, name, password)
        return True
    except IntegrityError:
        return False

# Get user ID
def user_id(request: HttpRequest) -> int:
    return request.session.get("user_id", 0)

# Require a specific user role
def require_role(request: HttpRequest, role: int) -> None:
    user_role = request.session.get("user_role", 0)
    if not request.user.is_authenticated or role > user_role:
        raise PermissionDenied()

# Check CSRF token
def check_csrf(request: HttpRequest) -> None:
    session_token = request.session.get("csrf_token", "")
    form_token = request.POST.get("csrf_token", "")
    if session_token != form_token:
        raise PermissionDenied("CSRF token mismatch")
