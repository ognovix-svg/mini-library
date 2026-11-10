from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/new/', views.book_create, name='book_create'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('loans/<int:pk>/return/', views.loan_return, name='loan_return'),
    path('books/<int:pk>/loan/', views.loan_create, name='loan_create'),
    path('stats/', views.library_stats, name='stats'),  # <-- НОВИЙ РЯДОК
]