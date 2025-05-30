from django.urls import path
from .views import MovieListView, MovieCreateView, MovieUpdateView, MovieDeleteView

urlpatterns = [
    path('', MovieListView.as_view(), name='movie_list'),
    path('create/', MovieCreateView.as_view(), name='movie_create'),
    path('update/<int:pk>/', MovieUpdateView.as_view(), name='movie_update'),
    path('delete/<int:pk>/', MovieDeleteView.as_view(), name='movie_delete'),
]
