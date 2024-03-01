from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegistrationForm, UserProfileForm, UserForm
from .models import Genre, Book, Order, UserProfile

from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request):
    genres = Genre.objects.all()
    books = Book.objects.all()
    return render(request, 'home.html', {'genres': genres, 'books': books})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def genre_books(request, genre_id):
    genre = Genre.objects.get(pk=genre_id)
    genres = Genre.objects.all()
    books = Book.objects.filter(genre=genre)
    return render(request, 'genre_books.html', {'genres': genres, 'genre': genre, 'books': books})


def book_details(request, book_id):
    book = Book.objects.get(pk=book_id)
    return render(request, 'book_details.html', {'book': book})


@login_required
def add_to_cart(request, book_id):
    book = Book.objects.get(pk=book_id)
    order = Order(book=book, price=book.price)
    order.save()
    return redirect('cart')


@login_required
def cart(request):
    orders = Order.objects.all()
    total_amount = sum(order.price for order in orders)
    return render(request, 'cart.html', {'orders': orders, 'total_amount': total_amount})


@login_required
def delete_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.delete()
    messages.success(request, 'Order deleted successfully.')
    return redirect('cart')


@login_required
def make_payment(request):
    if request.method == 'POST':
        # Perform the payment processing logic here
        # Update order status or perform any necessary actions
        messages.success(request, 'Payment successful.')
        return redirect('cart')
    return render(request, 'make_payment.html')


@login_required
def account(request):
    user = request.user

    try:
        user_profile = user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_profile:
            form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        else:
            form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and form.is_valid():
            user_form.save()
            if form:
                form.instance.user = user
                form.save()

            messages.success(request, 'Account information updated successfully.')
            update_session_auth_hash(request, user_form.instance)  # Update session with new password if changed
            return redirect('account')
    else:
        user_form = UserForm(instance=user)
        if user_profile:
            form = UserProfileForm(instance=user_profile)
        else:
            form = UserProfileForm()

    return render(request, 'account.html', {'user_form': user_form, 'form': form})


def search_books(request):
    query = request.GET.get('search_query')
    books = Book.objects.filter(title__icontains=query)
    genres = Genre.objects.all()
    return render(request, 'search_results.html', {'books': books, 'genres': genres})
