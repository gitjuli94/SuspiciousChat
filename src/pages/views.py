from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .models import ChatMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index(request):
    #  hard-coded users for db
    admin_user, created_admin = User.objects.get_or_create(
        username="admin",
        defaults={"is_staff": True, "is_superuser": True}
    )
    if created_admin:
        admin_user.set_password("admin")
        admin_user.save()

    normal_user, created_user = User.objects.get_or_create(
        username="pasi",
        defaults={"is_staff": False, "is_superuser": False}
    )
    if created_user:
        normal_user.set_password("pasi")
        normal_user.save()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "error.html", {"message": "Incorrect username or password"})
    return render(request, "index.html")



def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to the index page after logout


@login_required
def forum(request):
    """
    Forum main page where users can view messages.
    """
    # Fetch all chat messages from the database
    messages = ChatMessage.objects.all().order_by('-sent_at')  # Order by newest first
    return render(request, "forum.html", {"messages": messages})


@login_required
def new_chat(request):
    """
    Render the page to add a new chat message.
    """
    return render(request, "new_chat.html")


@login_required
def send_chat(request):
    """
    Handle posting of a new chat message.
    """
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if content:
            # Create a new ChatMessage instance
            ChatMessage.objects.create(user=request.user, content=content)
            return redirect("forum")  # Redirect to the forum page
        else:
            return render(request, "error.html", {"message": "Message content cannot be empty"})
    return redirect("forum")


@login_required
def delete_chat(request, message_id):
    """
    Allow an admin user to delete a chat message.
    """
    if request.user.is_staff:  # Ensure only admin users can delete messages
        try:
            message = ChatMessage.objects.get(id=message_id)
            message.delete()
            return redirect("forum")
        except ChatMessage.DoesNotExist:
            return render(request, "error.html", {"message": "Message not found"})
    else:
        return render(request, "error.html", {"message": "Only admin users can delete messages"})
