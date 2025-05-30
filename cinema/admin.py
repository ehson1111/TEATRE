from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    CustomUser, Actors, Directors, Movie, 
    MovieActors, MovieDirector, Review,
    Hall, Show, SeatPlace, Trailer, Order
)

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'phone_number', 'age', 'is_staff')
    search_fields = ('email', 'full_name', 'phone_number')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone_number', 'age')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone_number', 'age', 'password1', 'password2'),
        }),
    )

class MovieActorsInline(admin.TabularInline):
    model = MovieActors
    extra = 1

class MovieDirectorInline(admin.TabularInline):
    model = MovieDirector
    extra = 1

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'rel_year', 'country', 'duration', 'is_active')
    list_filter = ('is_active', 'rel_year', 'country')
    search_fields = ('title', 'description')
    inlines = [MovieActorsInline, MovieDirectorInline]
    # Removed filter_horizontal since we're using through models

class ActorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'experience', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

class DirectorsAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'created_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('fullname',)

class ShowAdmin(admin.ModelAdmin):
    list_display = ('movie', 'showing_date', 'showing_time', 'hall')
    list_filter = ('showing_date', 'hall')
    search_fields = ('movie__title',)

class SeatPlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'hall', 'status', 'price')
    list_filter = ('hall', 'status')
    search_fields = ('name', 'hall__name')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('star_number', 'user_id', 'is_active', 'create_at')
    list_filter = ('is_active', 'star_number')
    search_fields = ('user_id__email', 'descriptions')

class HallAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class TrailerAdmin(admin.ModelAdmin):
    list_display = ('movie', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('movie__title',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'show', 'payment_status', 'created_at', 'seats')
    list_filter = ('payment_status', 'created_at')
    search_fields = ('user__email', 'show__movie__title')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Actors, ActorsAdmin)
admin.site.register(Directors, DirectorsAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Hall, HallAdmin)
admin.site.register(Show, ShowAdmin)
admin.site.register(SeatPlace, SeatPlaceAdmin)
admin.site.register(Trailer, TrailerAdmin)
admin.site.register(Order, OrderAdmin)