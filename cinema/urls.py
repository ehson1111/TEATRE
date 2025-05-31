from django.urls import path
from . import views
from django.urls import path
from .views import (
    register_view, login_view, logout_view, otziv_view,
    password_reset_done_view, password_reset_complete_view,
    UserForgotPasswordView, UserPasswordResetConfirmView
)
urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('password_reset/', views.password_reset_request_view, name='password_reset'),
    path('password_reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete_view, name='password_reset_complete'),

    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movies/<int:movie_id>/add_review/', views.add_review, name='add_review'),
    path('reviews/', views.otziv_view, name='otziv'),

    path('shows/<int:pk>/', views.show_detail, name='show_detail'),
    path('shows/<int:show_id>/book/', views.book_tickets, name='book_tickets'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),

    path('profile/', views.user_profile, name='user_profile'),
     path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('otziv/', otziv_view, name='otziv'),
    
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('password-reset/done/', password_reset_done_view, name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', password_reset_complete_view, name='password_reset_complete'),
]


