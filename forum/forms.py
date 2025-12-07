from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UploadItem, Category, Message, Comment

# -----------------------------
# SIGNUP FORM
# -----------------------------
class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter email'
    }))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter phone number'
    }))
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Choose username'
    }))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter password'
    }))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm password'
    }))

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password1", "password2"]

# -----------------------------
# UPLOAD ITEM FORM
# -----------------------------
class UploadItemForm(forms.ModelForm):
    class Meta:
        model = UploadItem
        fields = ["title", "description", "category", "image", "video", "link"]
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title'}),
            "description": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write description...', 'rows': 4}),
            "category": forms.Select(attrs={'class': 'form-select'}),
            "image": forms.ClearableFileInput(attrs={'class': 'form-control'}),
            "video": forms.ClearableFileInput(attrs={'class': 'form-control'}),
            "link": forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Optional URL'}),
        }

# -----------------------------
# CATEGORY FORM
# -----------------------------
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category name'}),
            "description": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe category...', 'rows': 3}),
        }

# -----------------------------
# CONTACT MESSAGE FORM
# -----------------------------
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "message"]
        widgets = {
            "subject": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            "message": forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your message...'}),
        }

# -----------------------------
# COMMENT FORM
# -----------------------------
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment...'
            }),
        }
