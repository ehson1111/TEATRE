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



    