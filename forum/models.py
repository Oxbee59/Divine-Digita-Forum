from django.db import models
from django.contrib.auth.models import User

# ---- CATEGORY ----
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ---- POSTS / UPLOADS (admin only) ----
class UploadItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploads")  # admin who posted
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True, null=True)  # optional external link

    # These fields will now be stored on Cloudinary automatically
    image = models.ImageField(upload_to='uploads/images/', blank=True, null=True)
    video = models.FileField(upload_to='uploads/videos/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ---- MESSAGES from customers to admin ----
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} - {self.user.username}"


# ---- COMMENTS on posts ----
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(UploadItem, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
