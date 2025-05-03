from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import get_messages
from .models import Book, Review, Comment
from django.db.models import Q, Avg, Count
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta


# Book categories
LIT_GROUPS = {    
    'Novels': ['Novel', 'Lightnovel'],
    'Comics': ['Comic', 'Graphic Novel'],    # I'm imagining like Marvel and stuff, idk how to name non-asian ones man XD
    "Manga_plus": ['Manga', 'Manwha', 'Manhua'],
    'WebComics': ['WebToon', 'Fanfiction']
}

def home(request):
    top_books = Book.objects.annotate(ave_rating=Avg('review__rating')).order_by('-ave_rating')[:10]
    last_7_days = timezone.now() - timedelta(days=7)
    
    trending_books = Book.objects.annotate(
        recent_count=Count('review', filter=Q(review__created_at__gte=last_7_days)),
        recent_avg=Avg('review__rating', filter=Q(review__created_at__gte=last_7_days))
    ).filter(recent_count__gt=0).order_by('-recent_count', '-recent_avg')[:6]

    top_reviewers = User.objects.annotate(
        review_count=Count('review')
    ).filter(review_count__gt=0).order_by('-review_count')[:5]

    novels = Book.objects.filter(lit_type__in=LIT_GROUPS['Novels'])
    comics = Book.objects.filter(lit_type__in=LIT_GROUPS['Comics'])
    manga_plus = Book.objects.filter(lit_type__in=LIT_GROUPS['Manga_plus'])
    webcomics = Book.objects.filter(lit_type__in=LIT_GROUPS['WebComics'])

    return render(request, 'main/home.html', {
        'top_books': top_books,
        'trending_books': trending_books,
        'top_reviewers': top_reviewers,
        'novel_books': novels,
        'comic_books': comics,
        'manga_plus_books': manga_plus,
        'webcomic_books': webcomics
        })

def auth_screen(request):
# Clear stale messages if user is not authenticated (i.e. just logged out)
    if not request.user.is_authenticated:
        list(get_messages(request))  # Clears the messages

    login_form = AuthenticationForm()
    register_form = UserCreationForm()
    password_reset_form = PasswordResetForm()   

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'login':
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid login credentials.")

        elif action == 'register':
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, f"Account created for {user.username}!")
                return redirect('home')
            else:
                messages.error(request, "Please correct the registration errors.")

    context = {
        'login_form': login_form,
        'register_form': register_form,
        'password_reset_form': password_reset_form,
    }

    return render(request, 'main/auth.html', context)

def browse(request):
    query = request.GET.get('q')
    books = Book.objects.all()
    lit_group = request.GET.get('lit_group')

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genre__icontains=query) |
            Q(added_by__username__icontains=query)
        )
    
    if lit_group:
         books = books.filter(lit_type__in=LIT_GROUPS[lit_group])

    return render(request, 'book/browse.html', {'books': books})

def upload_review(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        synopsis = request.POST.get('synopsis')
        genre = request.POST.get('genre')
        lit_type = request.POST.get('lit_type')
        cover_image_url = request.POST.get('cover_image_url')
        

        rating = request.POST.get('rating')
        review_text = request.POST.get('review')

        book = Book.objects.create(
            title=title,
            author=author,
            synopsis=synopsis,
            genre=genre,
            added_by=request.user,
            lit_type=lit_type,
            cover_image_url=cover_image_url)
        
        Review.objects.create(book=book,
                              user=request.user,
                              text=review_text,
                              rating=rating)

        return redirect('home')

    return render(request, 'review/upload.html')

def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        title = request.POST.get('title')
        text = request.POST.get('review')
        Review.objects.create(
            book=book,
            user=request.user,
            rating=rating,
            title=title,
            text=text
        )
        return redirect('book_detail', book.id)
    return render(request, 'review/add.html', {'book': book})

def view_profile(request):
    return render(request, 'main/profile.html')

def search_book(request):
    return render(request, 'review/search.html')

def ajax_search_books(request):
    query = request.GET.get("q", "")
    books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    data = [{"id": b.id, "title": b.title, "author": b.author} for b in books]

    return JsonResponse({"results": data})

def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        title = request.POST.get('title')
        text = request.POST.get('review')
        Review.objects.create(
            book=book,
            user=request.user,
            rating=rating,
            title=title,
            text=text
        )
        return redirect('book_detail', book.id)
    return render(request, 'review/add.html', {'book': book})

def my_reviews(request):
    user = request.user
    reviews = Review.objects.filter(user=user)

    return render(request, 'review/my_reviews.html', {'reviews': reviews})


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = Review.objects.filter(book=book)
    comments = Comment.objects.filter(review__book=book)
    ave_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    return render(request, 'book/detail.html', {
        'book': book,
        'reviews': reviews,
        'comments': comments,
        'ave_rating': ave_rating,
        }
    )

def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        review.title = request.POST.get('title')
        review.rating = request.POST.get('rating')
        review.text = request.POST.get('review')
        review.save()
        return redirect('my_reviews')

    return render(request, 'review/edit_review.html', {'review': review})

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == "POST":
        review.delete()
        return redirect('my_reviews')

def add_comment(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, pk=review_id)
        Comment.objects.create(
            review = review,
            user = request.user,
            text = request.POST['comment']
        )

    return redirect('book_detail', book_id=review.book.id)
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        comment.delete()
    
    return redirect('book_detail', comment.review.book.id)
