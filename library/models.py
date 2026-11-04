
from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Reader(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    registered_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.full_name} ({self.email})'


class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    published_year = models.IntegerField()
    copies_total = models.PositiveIntegerField(default=1)
    authors = models.ManyToManyField(Author, related_name='books')

    def __str__(self):
        return f'{self.title} ({self.published_year})'

    def available_copies(self):
        active_loans = self.loans.filter(returned_at__isnull=True).count()
        return self.copies_total - active_loans


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='loans')
    issued_at = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.reader.full_name} взяв ({self.book.title} до {self.due_date})'