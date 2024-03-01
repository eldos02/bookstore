from django.contrib import admin
from .models import Order, Book, Genre, UserProfile
# Register your models here.
admin.site.register(Order)
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(UserProfile)