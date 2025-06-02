from django.urls import path, include
from django.contrib.auth import views as auth_views

from cinema.views import booking_views, cinema_management_views, movie_views
from .views import auth_views

urlpatterns = [
    # Auth
    path('register/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    
    # Password reset
    path('password-reset/', auth_views.password_reset_request_view, name='password_reset'),
    path('password-reset/done/', auth_views.password_reset_done_view, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.password_reset_confirm_view, name='password_reset_confirm'),
    path('reset/done/', auth_views.password_reset_complete_view, name='password_reset_complete'),
    
    # Movies
    path('', movie_views.home, name='home'),
    path('movies/', movie_views.movie_list, name='movie_list'),
    path('movies/<int:pk>/', movie_views.movie_detail, name='movie_detail'),
    path('movies/<int:movie_id>/review/', movie_views.add_review, name='add_review'),
    path('reviews/', movie_views.otziv_view, name='reviews'),
    
    # Booking
    path('shows/<int:pk>/', booking_views.show_detail, name='show_detail'),
    path('shows/<int:pk>/book/', booking_views.book_tickets, name='book_tickets'),
    path('orders/<int:pk>/', booking_views.order_detail, name='order_detail'),
    
    # User
    path('profile/', booking_views.user_profile, name='user_profile'),
    
    # Cinema Management
    path('cinema/halls/', cinema_management_views.hall_list, name='hall_list'),
    path('cinema/halls/create/', cinema_management_views.hall_create, name='hall_create'),
    path('cinema/halls/<int:pk>/edit/', cinema_management_views.hall_edit, name='hall_edit'),
    path('cinema/halls/<int:pk>/delete/', cinema_management_views.hall_delete, name='hall_delete'),
    
    path('cinema/shows/', cinema_management_views.show_list, name='show_list'),
    path('cinema/shows/create/', cinema_management_views.show_create, name='show_create'),
    path('cinema/shows/<int:pk>/edit/', cinema_management_views.show_edit, name='show_edit'),
    path('cinema/shows/<int:pk>/delete/', cinema_management_views.show_delete, name='show_delete'),
    
    path('cinema/seats/', cinema_management_views.seat_list, name='seat_list'),
    path('cinema/seats/create/', cinema_management_views.seat_create, name='seat_create'),
    path('cinema/seats/<int:pk>/edit/', cinema_management_views.seat_edit, name='seat_edit'),
    path('cinema/seats/<int:pk>/delete/', cinema_management_views.seat_delete, name='seat_delete'),
]