from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UploadItem, Category, Message, Comment

# -------------------------
# Signup Form (User registration)
# -------------------------
class SignupForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


# -------------------------
# Admin Post Upload Form
# -------------------------
class UploadItemForm(forms.ModelForm):
    class Meta:
        model = UploadItem
        fields = ['title', 'description', 'category', 'image', 'video', 'link']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Post description', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Optional link'}),
        }


# -------------------------
# Category Form (admin)
# -------------------------
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': 3}),
        }


# -------------------------
# Contact Admin Message Form (customer)
# -------------------------
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password", "confirm"]

class UploadItemForm(forms.ModelForm):
    class Meta:
        model = UploadItem
        fields = ["title", "description", "category", "link", "image", "video"]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "message"]  # <--- was 'content', fixed now

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
# -------------------------
# Comment Form (forum posts)
# -------------------------
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add a comment...', 'rows': 3}),
        }
