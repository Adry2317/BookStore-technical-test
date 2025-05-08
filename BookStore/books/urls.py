from django.contrib import admin
from django.urls import path
from books import views, api_views


urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.sign_in, name='signin'),
    path('signout/', views.sign_out, name='signout'),
    path('book_list', views.book_list, name='book_list'),
    path('book/<int:book_id>/delete', views.book_delete, name='delete_book'),
    path('book/<int:book_id>/edit', views.book_edit, name='edit_book'),
    path('book/new', views.buy_new_book, name='buy_new_book'),
    path('book/<int:book_id>/buy', views.buy_book_stock, name='buy_book_stock'),
    path('event_list', views.event_list, name='event_list'),

    # API URLs
    path('book/buy/<int:book_id>', api_views.buyClientBookView.as_view(), name='buy_client_book'),
]