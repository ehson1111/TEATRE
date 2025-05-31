from django.urls import path
from . import views

urlpatterns = [
    path('', views.hall_list, name='hall_list'),
    path('halls/new/', views.hall_create, name='hall_create'),

    path('shows/', views.show_list, name='show_list'),
    path('shows/new/', views.show_create, name='show_create'),

    path('seats/', views.seat_list, name='seat_list'),
    path('seats/new/', views.seat_create, name='seat_create'),
    
    path('halls/<int:pk>/edit/', views.hall_edit, name='hall_edit'),
    path('halls/<int:pk>/delete/', views.hall_delete, name='hall_delete'),

    path('shows/<int:pk>/edit/', views.show_edit, name='show_edit'),
    path('shows/<int:pk>/delete/', views.show_delete, name='show_delete'),

    path('seats/<int:pk>/edit/', views.seat_edit, name='seat_edit'),
    path('seats/<int:pk>/delete/', views.seat_delete, name='seat_delete'),

]







# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),

#     path('register/', views.register_view, name='register'),
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),

#     path('password_reset/', views.password_reset_request_view, name='password_reset'),
#     path('password_reset/done/', views.password_reset_done_view, name='password_reset_done'),
#     path('reset/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
#     path('reset/done/', views.password_reset_complete_view, name='password_reset_complete'),

#     path('movies/', views.movie_list, name='movie_list'),
#     path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
#     path('movies/<int:pk>/add_review/', views.add_review, name='add_review'),  

#     path('reviews/', views.otziv_view, name='otziv'),

#     path('shows/<int:pk>/', views.show_detail, name='show_detail'),
#     path('shows/<int:pk>/book/', views.book_tickets, name='book_tickets'),  

#     path('orders/<int:pk>/', views.order_detail, name='order_detail'),

#     path('profile/', views.user_profile, name='user_profile'),
# ]


