from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('genre/<int:genre_id>/', views.genre_books, name='genre_books'),
    path('book/<int:book_id>/', views.book_details, name='book_details'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('make_payment/', views.make_payment, name='make_payment'),
    path('account/', views.account, name='account'),
    path('search/', views.search_books, name='search_books'),

]
