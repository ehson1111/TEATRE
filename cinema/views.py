from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .forms import CustomUserCreationForm, ReviewForm, BookingForm
from .models import Movie, Show, Hall, SeatPlace, Order, Review, CustomUser



def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') 
    else:
        form = AuthenticationForm()  
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')



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
    reviews = Review.objects.filter(movie=movie, is_active=True).order_by('-created_at')
    review_form = ReviewForm()

    average_rating = round(
        sum(review.star_number for review in reviews) / reviews.count(), 1
    ) if reviews.exists() else 0

    return render(request, 'theater/movie_detail.html', {
        'movie': movie,
        'shows': shows,
        'trailers': trailers,
        'reviews': reviews,
        'review_form': review_form,
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
            messages.success(request, "Баррасиатон бо муваффақият илова шуд!")
    return redirect('movie_detail', pk=movie.pk)


def otziv_view(request):
    otzivs = Review.objects.all()
    return render(request, 'otziv.html', {"otzivs": otzivs})



@login_required
def show_detail(request, pk):
    show = get_object_or_404(Show, pk=pk)
    seats = SeatPlace.objects.filter(hall=show.hall)
    booked_seats = Order.objects.filter(show=show).values_list('seats', flat=True)
    form = BookingForm()
    return render(request, 'theater/show_detail.html', {
        'show': show,
        'seats': seats,
        'booked_seats': booked_seats,
        'booking_form': form
    })


@login_required
def book_tickets(request, show_id):
    show = get_object_or_404(Show, pk=show_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            selected_seats = form.cleaned_data['seats']
            seat_count = len(selected_seats)
            order = Order.objects.create(
                user=request.user,
                show=show,
                seats=seat_count,
                total_price=seat_count * SeatPlace.objects.get(pk=selected_seats[0]).price
            )
            order.seats_booked.set(selected_seats)
            messages.success(request, "Билетҳо бо муваффақият брон шуданд!")
            return redirect('order_detail', pk=order.pk)
    else:
        form = BookingForm()
    return render(request, 'theater/booking.html', {
        'show': show,
        'form': form
    })


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'theater/order_detail.html', {
        'order': order
    })


@login_required
def user_profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'theater/user_profile.html', {
        'user_profile': request.user,
        'orders': orders
    })



def password_reset_request_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            users = User.objects.filter(email=email)
            for user in users:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(f"/reset/{uid}/{token}/")
                subject = "Барқароркунии парол"
                message = render_to_string("email_reset.html", {
                    "reset_link": reset_link,
                    "user": user
                })
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            return redirect("password_reset_done")
    else:
        form = PasswordResetForm()
    return render(request, "password_reset_form.html", {"form": form})


def password_reset_done_view(request):
    return render(request, "password_reset_done.html")


def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect("password_reset_complete")
        else:
            form = SetPasswordForm(user)
        return render(request, "password_reset_confirm.html", {"form": form})
    else:
        return render(request, "password_reset_invalid.html")


def password_reset_complete_view(request):
    return render(request, "password_reset_complete.html")






def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie.objects.prefetch_related('actors', 'directors', 'reviews'), pk=movie_id)
    reviews = movie.reviews.filter(is_active=True)  
    context = {
        'movie': movie,
        'reviews': reviews
    }
    return render(request, 'theater/movie_detail.html', context)    