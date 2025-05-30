from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models



class Actors(models.Model):
    name = models.CharField(max_length=20)
    experience = models.PositiveBigIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Directors(models.Model):
    fullname = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.fulname

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    age_limit = models.CharField(max_length=255)
    image = models.ImageField(upload_to='movie_poster/')
    duration = models.PositiveBigIntegerField()
    country = models.CharField(max_length=50)
    rel_year = models.PositiveBigIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    actors = models.ManyToManyField(Actors, through='MovieActors')
    directors = models.ManyToManyField(Directors, through='MovieDirector')

    def __str__(self):
        return self.title
    
class MovieActors(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actors, on_delete=models.CASCADE)
    is_hero = models.BooleanField(default=False)


class MovieDirector(models.Model):
    director = models.ForeignKey(Directors, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)



    
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
    star_number=models.IntegerField()
    descriptions=models.TextField()
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=False)
    create_at=models.DateField()
    def __str__(self):
        return self.star_number
