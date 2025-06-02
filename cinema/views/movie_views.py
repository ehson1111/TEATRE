from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from cinema.forms import ReviewForm
from cinema.models import Movie, Show, Review

def home(request):
    featured_movies = Movie.objects.filter(is_active=True).order_by('-created_at')[:4]
    upcoming_shows = Show.objects.filter(showing_date__gte=timezone.now().date()).order_by('showing_date')[:5]
    return render(request, 'theater/home.html', {
        'featured_movies': featured_movies,
        'upcoming_shows': upcoming_shows,
        'now': timezone.now()
    })

def movie_list(request):
    movies = Movie.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'theater/movie_list.html', {
        'movies': movies,
        'now': timezone.now()
    })

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    shows = Show.objects.filter(movie=movie, showing_date__gte=timezone.now().date())
    trailers = movie.trailers.filter(is_active=True)
    reviews = Review.objects.filter(movie=movie, is_active=True).order_by('-create_at')
    
    average_rating = round(
        sum(review.star_number for review in reviews) / reviews.count(), 1
    ) if reviews.exists() else 0

    return render(request, 'theater/movie_detail.html', {
        'movie': movie,
        'shows': shows,
        'trailers': trailers,
        'reviews': reviews,
        'average_rating': average_rating
    })

@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            messages.success(request, "Review added successfully!")
    return redirect('movie_detail', pk=movie.pk)

def otziv_view(request):
    reviews = Review.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'theater/reviews.html', {"reviews": reviews})