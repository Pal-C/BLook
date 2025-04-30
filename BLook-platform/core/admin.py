from django.contrib import admin

from .models import Book, Review, Comment

admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Comment)

# Register your models here.
