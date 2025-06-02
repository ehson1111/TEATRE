from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from cinema.forms import HallForm, ShowForm, SeatPlaceForm
from cinema.models import Hall, Show, SeatPlace

def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)

@login_required
@staff_required

def hall_list(request):
    halls = Hall.objects.all()
    return render(request, 'cinema/hall_list.html', {'halls': halls})


@login_required
@staff_required
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


# Similar improvements for other management views...
@login_required
@staff_required
def hall_update(request, pk):
    hall = get_object_or_404(Hall, pk=pk)
    if request.method == 'POST':
        form = HallForm(request.POST, instance=hall)
        if form.is_valid():
            form.save()
            messages.success(request, "Hall updated successfully!")
            return redirect('hall_list')
    else:
        form = HallForm(instance=hall)
    return render(request, 'cinema/hall_form.html', {'form': form})

@login_required
@staff_required
def hall_delete(request, pk):
    hall = get_object_or_404(Hall, pk=pk)
    if request.method == 'POST':
        hall.delete()
        messages.success(request, "Hall deleted successfully!")
        return redirect('hall_list')
    return render(request, 'cinema/hall_confirm_delete.html', {'hall': hall})


@login_required
@staff_required
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








