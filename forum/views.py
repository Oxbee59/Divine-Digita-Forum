from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import UploadItem, Category, Message, Comment
from .forms import SignupForm, UploadItemForm, CategoryForm, MessageForm, CommentForm


## ----------------- AUTH -----------------
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            password = form.cleaned_data["password1"]

            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Store phone in last_name field
            user.last_name = phone
            user.save()

            messages.success(request, "Account created successfully! You can now log in.")
            return redirect("login")

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = SignupForm()

    return render(request, "forum/register.html", {"form": form})



def login_view(request):
    if request.method == "GET":
        return render(request, "forum/login.html")

    identifier = request.POST.get("identifier", "").strip()
    password = request.POST.get("password", "").strip()

    user = None

    # Try username
    try:
        u = User.objects.get(username=identifier)
        user = authenticate(request, username=u.username, password=password)
    except User.DoesNotExist:
        pass

    # Try phone number (stored in last_name)
    if user is None:
        try:
            u = User.objects.get(last_name=identifier)
            user = authenticate(request, username=u.username, password=password)
        except User.DoesNotExist:
            pass

    if user:
        login(request, user)
        if user.is_staff:
            return redirect("admin_dashboard")
        return redirect("customer_dashboard")

    messages.error(request, "Invalid login credentials.")
    return redirect("login")


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")

# ----------------- SUPERADMIN -----------------
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_posts = UploadItem.objects.count()
    total_categories = Category.objects.count()
    total_messages = Message.objects.count()

    context = {
        "total_users": total_users,
        "total_posts": total_posts,
        "total_categories": total_categories,
        "total_messages": total_messages,
    }
    return render(request, "forum/admin_dashboard.html", context)

@user_passes_test(lambda u: u.is_staff)
def manage_users(request):
    users = User.objects.all().order_by("id")
    return render(request, "forum/admin_manage_users.html", {"users": users})


# Manage Posts
@user_passes_test(lambda u: u.is_staff)
def manage_posts(request):
    uploads = UploadItem.objects.select_related('user', 'category').all()
    return render(request, "forum/admin_manage_posts.html", {"uploads": uploads})

@user_passes_test(lambda u: u.is_staff)
def post_add(request):
    if request.method == "POST":
        form = UploadItemForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Post created successfully.")
            return redirect("manage_posts")
    else:
        form = UploadItemForm()
    return render(request, "forum/post_form.html", {"form": form, "title": "Create Post"})

@user_passes_test(lambda u: u.is_staff)
def post_edit(request, pk):
    post = get_object_or_404(UploadItem, pk=pk)
    
    if request.method == "POST":
        form = UploadItemForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect("manage_posts")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UploadItemForm(instance=post)

    # Pass categories queryset separately if needed in template
    categories = Category.objects.all()
    
    return render(
        request, 
        "forum/post_edit.html", 
        {
            "form": form,
            "title": "Edit Post",
            "categories": categories,
        }
    )

@user_passes_test(lambda u: u.is_staff)
def post_delete(request, pk):
    post = get_object_or_404(UploadItem, pk=pk)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect("manage_posts")
    return render(request, "forum/post_confirm_delete.html", {"post": post})

@user_passes_test(lambda u: u.is_staff)
def admin_messages(request):
    messages_list = Message.objects.select_related('user').all()
    return render(request, "forum/admin_messages.html", {"messages": messages_list})


# ----------------- ADMIN -----------------
@user_passes_test(lambda u: u.is_staff)
def admin_uploads(request):
    categories = Category.objects.all()
    uploads = UploadItem.objects.select_related('user', 'category').all().order_by('-created_at')

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id) if category_id else None
        link = request.POST.get('link')
        image = request.FILES.get('image')  # CloudinaryField handles this automatically
        video = request.FILES.get('video')  # CloudinaryField handles this automatically

        UploadItem.objects.create(
            user=request.user,
            title=title,
            description=description,
            category=category,
            link=link,
            image=image,
            video=video
        )
        messages.success(request, "Upload added successfully.")
        return redirect("admin_uploads")

    context = {
        "uploads": uploads,
        "categories": categories
    }
    return render(request, "forum/admin_uploads.html", context)
# ----------------- CUSTOMER -----------------
@login_required
def customer_dashboard(request):
    # Only active uploads (optional filter)
    uploads = UploadItem.objects.select_related('user', 'category').all().order_by('-created_at')
    context = {"uploads": uploads}
    return render(request, "forum/customer_dashboard.html", context)  


@login_required
def profile(request):
    return render(request, "forum/profile.html")

@login_required
def contact_admin(request):
    admin_whatsapp = "+233556025786"

    if request.method == "POST":
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Message.objects.create(user=request.user, subject=subject, message=message)
        messages.success(request, "Message sent to admin successfully!")
        return redirect("contact_admin")

    return render(request, "forum/contact_admin.html", {
        "admin_whatsapp": admin_whatsapp
    })


# ----------------- FORUM -----------------
def forum_index(request):
    posts = UploadItem.objects.select_related('user', 'category').all().order_by('-created_at')[:6]
    return render(request, "forum/index.html", {"posts": posts})


# ----------------- POST DETAILS -----------------
@login_required
def forum_detail(request, pk):
    post = get_object_or_404(UploadItem.objects.select_related('user', 'category'), pk=pk)
    comments = post.comments.select_related('user').all()
    context = {
        "post": post,
        "comments": comments
    }
    return render(request, "forum/detail.html", context)

@user_passes_test(lambda u: u.is_staff)
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        user.username = request.POST.get("username", "").strip()
        user.email = request.POST.get("email", "").strip()
        user.last_name = request.POST.get("phone", "").strip()  # UPDATE PHONE
        user.is_staff = True if request.POST.get("is_staff") == "on" else False
        user.save()

        messages.success(request, "User updated successfully.")
        return redirect("manage_users")

    return render(request, "forum/admin_edit_user.html", {"user": user})

@user_passes_test(lambda u: u.is_staff)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        messages.success(request, "User deleted successfully.")
    return redirect("manage_users")


@user_passes_test(lambda u: u.is_staff)
def delete_message(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    if request.method == "POST":
        msg.delete()
        messages.success(request, "Message deleted successfully.")
        return redirect("admin_messages")
    return redirect("admin_messages")