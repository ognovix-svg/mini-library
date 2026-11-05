from django import forms
from .models import Book, Loan


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'published_year', 'copies_total', 'authors']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '13 цифр'}),
            'published_year': forms.TextInput(attrs={'class': 'form-control'}),
            'copies_total': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'authors': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
        }

        labels = {
            'title': 'Назва книги',
            'isbn': 'ISBN(13 cимволів)',
            'published_year': 'Рік видання',
            'copies_total': 'Кількість примірників',
            'authors': 'Автори (Затисніть Cmd/Cntrl для вибору кількох)'
        }