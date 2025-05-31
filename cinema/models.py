from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class Actors(models.Model):
    name = models.CharField(max_length=20)
    experience = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Directors(models.Model):
    fullname = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.fullname


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    age_limit = models.CharField(max_length=255)
    image = models.ImageField(upload_to='movie_poster/')
    duration = models.PositiveIntegerField()
    country = models.CharField(max_length=50)
    rel_year = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    actors = models.ManyToManyField(Actors, through='MovieActors', related_name='movies')
    directors = models.ManyToManyField(Directors, through='MovieDirector', related_name='movies')

    def __str__(self):
        return self.title


class MovieActors(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actors, on_delete=models.CASCADE)
    is_hero = models.BooleanField(default=False)

    class Meta:
        unique_together = ('movie', 'actor')


class MovieDirector(models.Model):
    director = models.ForeignKey(Directors, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('director', 'movie')


class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, phone_number, age, password=None, **extra_fields):
        if not email:
            raise ValueError("Email бояд пурра шавад")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, phone_number=phone_number, age=age, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, phone_number, age, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser бояд is_staff=True бошад')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser бояд is_superuser=True бошад')

        return self.create_user(email, full_name, phone_number, age, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    age = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number', 'age']

    def __str__(self):
        return self.email


class Review(models.Model):
    star = models.IntegerField()
    description = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.star} stars by {self.user.email}"


class Hall(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Show(models.Model):
    movie = models.ForeignKey(Movie, related_name='shows', on_delete=models.CASCADE)
    showing_date = models.DateField()
    showing_time = models.TimeField()
    hall = models.ForeignKey(Hall, related_name='shows', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie.title} {self.showing_date} {self.showing_time}"


class SeatPlace(models.Model):
    seat_number = models.CharField(max_length=50)
    hall = models.ForeignKey(Hall, related_name='seat_places', on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Seat {self.seat_number} in {self.hall.name}"


class Trailer(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='trailers')
    video_url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trailer for {self.movie.title}"


class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('F', 'Failed'),
        ('R', 'Refunded'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)
    seats_booked = models.ManyToManyField(SeatPlace)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} by {self.user.full_name}"
