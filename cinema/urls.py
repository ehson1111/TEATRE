from django.urls import path
from . import views

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
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movies/<int:movie_id>/add_review/', views.add_review, name='add_review'),
    path('reviews/', views.otziv_view, name='otziv'),

    path('shows/<int:pk>/', views.show_detail, name='show_detail'),
    path('shows/<int:show_id>/book/', views.book_tickets, name='book_tickets'),

    path('orders/<int:pk>/', views.order_detail, name='order_detail'),

    path('profile/', views.user_profile, name='user_profile'),
]

