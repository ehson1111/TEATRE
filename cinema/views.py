from django.shortcuts import render, redirect, get_object_or_404
from .models import Hall, Show, SeatPlace
from .forms import HallForm, ShowForm, SeatPlaceForm


def hall_list(request):
    halls = Hall.objects.all()
    return render(request, 'cinema/hall_list.html', {'halls': halls})


def hall_create(request):
    form = HallForm(request.POST or None)
    if form.is_valid():
        hall = form.save()
        for i in range(1, 21):
            SeatPlace.objects.create(
                seat_number=f"Seat {i}",
                hall=hall,
                price=50.00  
            )
        return redirect('hall_list')
    return render(request, 'cinema/form.html', {'form': form})



def show_list(request):
    shows = Show.objects.select_related('movie', 'hall').all()
    return render(request, 'cinema/show_list.html', {'shows': shows})


def show_create(request):
    form = ShowForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('show_list')
    return render(request, 'cinema/form.html', {'form': form})


def seat_list(request):
    hall_id = request.GET.get('hall')
    seats = SeatPlace.objects.select_related('hall')
    halls = Hall.objects.all()

    if hall_id:
        seats = seats.filter(hall__id=hall_id)

    return render(request, 'cinema/seat_list.html', {'seats': seats, 'halls': halls})



def seat_create(request):
    form = SeatPlaceForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('seat_list')
    return render(request, 'cinema/form.html', {'form': form})


# HALL
def hall_edit(request, pk):
    hall = get_object_or_404(Hall, pk=pk)
    form = HallForm(request.POST or None, instance=hall)
    if form.is_valid():
        form.save()
        return redirect('hall_list')
    return render(request, 'cinema/form.html', {'form': form})


def hall_delete(request, pk):
    hall = get_object_or_404(Hall, pk=pk)
    if request.method == 'POST':
        hall.delete()
        return redirect('hall_list')
    return render(request, 'cinema/confirm_delete.html', {'object': hall})


# SHOW
def show_edit(request, pk):
    show = get_object_or_404(Show, pk=pk)
    form = ShowForm(request.POST or None, instance=show)
    if form.is_valid():
        form.save()
        return redirect('show_list')
    return render(request, 'cinema/form.html', {'form': form})


def show_delete(request, pk):
    show = get_object_or_404(Show, pk=pk)
    if request.method == 'POST':
        show.delete()
        return redirect('show_list')
    return render(request, 'cinema/confirm_delete.html', {'object': show})


# SEAT
def seat_edit(request, pk):
    seat = get_object_or_404(SeatPlace, pk=pk)
    form = SeatPlaceForm(request.POST or None, instance=seat)
    if form.is_valid():
        form.save()
        return redirect('seat_list')
    return render(request, 'cinema/form.html', {'form': form})


def seat_delete(request, pk):
    seat = get_object_or_404(SeatPlace, pk=pk)
    if request.method == 'POST':
        seat.delete()
        return redirect('seat_list')
    return render(request, 'cinema/confirm_delete.html', {'object': seat})



















# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.utils import timezone

# from .forms0 import CustomUserCreationForm, ReviewForm, BookingForm
# from .models import Movie, Show, SeatPlace, Order, Review

# from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.utils.encoding import force_bytes, force_str
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.conf import settings
# from django.contrib.auth.models import User

# def password_reset_request_view(request):
#     if request.method == "POST":
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data["email"]
#             users = User.objects.filter(email=email)
#             for user in users:
#                 token = default_token_generator.make_token(user)
#                 uid = urlsafe_base64_encode(force_bytes(user.pk))
#                 reset_link = request.build_absolute_uri(f"/reset/{uid}/{token}/")
#                 subject = "Сброс пароля"
#                 message = render_to_string("email_reset.html", {
#                     "reset_link": reset_link,
#                     "user": user
#                 })
#                 send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
#             return redirect("password_reset_done")
#     else:
#         form = PasswordResetForm()
#     return render(request, "password_reset_form.html", {"form": form})

# def password_reset_done_view(request):
#     return render(request, "password_reset_done.html")

# def otziv_view(request):
#     reviews = Review.objects.filter(is_active=True).order_by('-created_at')
#     return render(request, 'reviews.html', {'reviews': reviews})

# def password_reset_confirm_view(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (User.DoesNotExist, ValueError, TypeError):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         if request.method == "POST":
#             form = SetPasswordForm(user, request.POST)
#             if form.is_valid():
#                 form.save()
#                 return redirect("password_reset_complete")
#         else:
#             form = SetPasswordForm(user)
#         return render(request, "password_reset_confirm.html", {"form": form})
#     else:
#         return render(request, "password_reset_invalid.html")

# def password_reset_complete_view(request):
#     return render(request, "password_reset_complete.html")

# def register_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Регистрация прошла успешно! Войдите в аккаунт.')
#             return redirect('login')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'register.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})

# def logout_view(request):
#     logout(request)
#     return redirect('login')

# def home(request):
#     movies = Movie.objects.filter(is_active=True).order_by('-created_at')[:4]
#     upcoming_shows = Show.objects.filter(showing_date__gte=timezone.now().date()).order_by('showing_date')[:5]
#     return render(request, 'home.html', {'movies': movies, 'upcoming_shows': upcoming_shows})

# def movie_list(request):
#     movies = Movie.objects.filter(is_active=True).order_by('-created_at')
#     return render(request, 'movie_list.html', {'movies': movies})

# def movie_detail(request, pk):
#     movie = get_object_or_404(Movie, pk=pk)
#     shows = movie.shows.filter(showing_date__gte=timezone.now().date())
#     reviews = Review.objects.filter(user__is_active=True, is_active=True, movie=movie).order_by('-created_at')
#     average_rating = round(sum(r.star for r in reviews) / reviews.count(), 1) if reviews.exists() else 0
#     review_form = ReviewForm()

#     return render(request, 'movie_detail.html', {
#         'movie': movie,
#         'shows': shows,
#         'reviews': reviews,
#         'average_rating': average_rating,
#         'review_form': review_form,
#     })

# @login_required
# def add_review(request, pk):
#     movie = get_object_or_404(Movie, pk=pk)
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.user = request.user
#             review.movie = movie
#             review.is_active = True
#             review.save()
#             messages.success(request, 'Спасибо за ваш отзыв!')
#         else:
#             messages.error(request, 'Ошибка при отправке отзыва.')
#     return redirect('movie_detail', pk=movie.pk)

# @login_required
# def show_detail(request, pk):
#     show = get_object_or_404(Show, pk=pk)
#     form = BookingForm(show=show)
#     booked_seats = Order.objects.filter(show=show).values_list('seats_booked', flat=True)
#     return render(request, 'show_detail.html', {
#         'show': show,
#         'form': form,
#         'booked_seats': booked_seats,
#     })

# @login_required
# def book_tickets(request, pk):
#     show = get_object_or_404(Show, pk=pk)
#     if request.method == 'POST':
#         form = BookingForm(request.POST, show=show)
#         if form.is_valid():
#             seats = form.cleaned_data['seats']
#             total_price = sum(seat.price for seat in seats)
#             order = Order.objects.create(
#                 user=request.user,
#                 show=show,
#                 payment_status='P',
#                 total_price=total_price,
#             )
#             order.seats_booked.set(seats)
#             seats.update(is_available=False)
#             messages.success(request, 'Билеты успешно забронированы!')
#             return redirect('order_detail', pk=order.pk)
#         else:
#             messages.error(request, 'Ошибка при бронировании билетов.')
#     else:
#         form = BookingForm(show=show)
#     return render(request, 'book_tickets.html', {'form': form, 'show': show})

# @login_required
# def order_detail(request, pk):
#     order = get_object_or_404(Order, pk=pk, user=request.user)
#     return render(request, 'order_detail.html', {'order': order})

# # === Добавленная функция user_profile ===

# @login_required
# def user_profile(request):
#     return render(request, 'user_profile.html', {'user': request.user})
