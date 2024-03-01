

# Create your models here.
from django.db import models

from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Book(models.Model):
    title = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    description = models.TextField()
    photo = models.ImageField(upload_to='book_photos')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    author = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return self.title


class Order(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} - {self.price}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    age = models.IntegerField()
    def __str__(self):
        return self.user.username
