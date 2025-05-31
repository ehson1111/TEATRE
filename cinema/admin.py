from django.contrib import admin
from .models import Order, Trailer, SeatPlace, Show, Hall, Review, CustomUser, CustomUserManager, MovieDirector, MovieActors, Movie, Directors, Actors
# Register your models here.


admin.site.register(Order)
admin.site.register(Trailer)
admin.site.register(SeatPlace)
admin.site.register(Show)
admin.site.register(Hall)
admin.site.register(Review)
admin.site.register(CustomUser)
admin.site.register(Movie)
admin.site.register(MovieDirector)
admin.site.register(MovieActors)
admin.site.register(Directors)
admin.site.register(Actors)