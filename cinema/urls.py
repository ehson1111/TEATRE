from django.urls import path
from .views import (
    register_view, login_view, logout_view, otziv_view,
    password_reset_request_view, password_reset_done_view,
    password_reset_confirm_view, password_reset_complete_view,
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('otziv/', otziv_view, name='otziv'),

    path('password_reset/', password_reset_request_view, name='password_reset'),
    path('password_reset/done/', password_reset_done_view, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),
    path('reset/done/', password_reset_complete_view, name='password_reset_complete'),
]
