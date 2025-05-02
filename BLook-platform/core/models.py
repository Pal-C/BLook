from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    synopsis = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    lit_type = models.CharField(max_length=100)  # e.g. Manga, Novel
    cover_image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1,6)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s review of {self.book.title}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey('Review', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} by {self.review.title or self.review.book.title}"