from django.urls import path
from . import views

urlpatterns = [
    # -------------------- AUTH --------------------
    path('signup/', views.signup, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # -------------------- CUSTOMER --------------------
    path('profile/', views.profile, name='profile'),
    path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),
    path('contact-admin/', views.contact_admin, name='contact_admin'),

    # -------------------- SUPERADMIN DASHBOARD --------------------
    path('superadmin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Manage Users
    path('superadmin/users/', views.manage_users, name='manage_users'),
    path('superadmin/users/<int:pk>/edit/', views.edit_user, name='edit_user'),
    path('superadmin/users/<int:pk>/delete/', views.delete_user, name='delete_user'),

    # Manage Posts
    path('superadmin/posts/', views.manage_posts, name='manage_posts'),
    path('superadmin/posts/add/', views.post_add, name='post_add'),
    path('superadmin/posts/<int:pk>/edit/', views.post_edit, name='edit_post'),
    path('superadmin/posts/<int:pk>/delete/', views.post_delete, name='delete_post'),

    # Uploads
    path('superadmin/uploads/', views.admin_uploads, name='admin_uploads'),

    # Customer Messages
    path('superadmin/messages/', views.admin_messages, name='admin_messages'),
    path('superadmin/messages/delete/<int:pk>/', views.delete_message, name='delete_message'),

    # -------------------- FORUM --------------------
    path('forum/', views.forum_index, name='forum_index'),
    path('forum/<int:pk>/', views.forum_detail, name='forum_detail'),
]
