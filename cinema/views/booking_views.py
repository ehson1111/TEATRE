from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from cinema.forms import BookingForm
from cinema.models import Show, SeatPlace, Order

@login_required
def show_detail(request, pk):
    show = get_object_or_404(Show, pk=pk)
    seats = SeatPlace.objects.filter(hall=show.hall).order_by('name')
    booked_seats = Order.objects.filter(show=show).values_list('seats', flat=True)
    
    # Create seat grid visualization
    seat_rows = {}
    for seat in seats:
        row = seat.seat_number.split()[0]  # Assuming format like "A1", "A2", etc.
        if row not in seat_rows:
            seat_rows[row] = []
        seat_rows[row].append({
            'id': seat.id,
            'number': seat.seat_number,
            'price': seat.price,
            'is_booked': seat.id in booked_seats
        })
    
    return render(request, 'theater/show_detail.html', {
        'show': show,
        'seat_rows': seat_rows,
        'booking_form': BookingForm()
    })

@login_required
def book_tickets(request, pk):
    show = get_object_or_404(Show, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            selected_seats = form.cleaned_data['seats']
            seat_count = len(selected_seats)
            total_price = sum(SeatPlace.objects.get(pk=seat_id).price for seat_id in selected_seats)
            
            order = Order.objects.create(
                user=request.user,
                show=show,
                seats=seat_count,
                total_price=total_price
            )
            order.seats_booked.set(selected_seats)
            
            messages.success(request, f"Successfully booked {seat_count} ticket(s)!")
            return redirect('order_detail', pk=order.pk)
    
    return redirect('show_detail', pk=pk)

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'user/order_detail.html', {'order': order})

@login_required
def user_profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user/profile.html', {'orders': orders})