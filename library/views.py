from django.shortcuts import  render, get_object_or_404, redirect
from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Book, Loan, Reader, Author
from .forms import BookForm
from django.db.models import Count
from .structures import benchmark_search


def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()

    return render(request, 'library/book_form.html', {'form': form})


def book_detail(request, pk):
    book = get_object_or_404(Book.objects.prefetch_related('authors'), pk=pk)
    active_loans = book.loans.filter(returned_at__isnull=True).select_related('reader')
    loan_history = book.loans.filter(returned_at__isnull=False).select_related('reader').order_by('-returned_at')
    readers = Reader.objects.all().order_by('full_name')
    context = {
        'book': book,
        'active_loans': active_loans,
        'loan_history': loan_history,
        'readers': readers
    }
    return render(request, 'library/book_detail.html', context)


def book_list(request):
    books = Book.objects.prefetch_related('authors').order_by('title')

    paginator = Paginator(books, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request,'library/book_list.html', context)


def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)

    return render(request, 'library/book_form.html', {'form': form})

def loan_return(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == 'POST':
        loan.returned_at = timezone.now().date()
        loan.save()
    return redirect('book_detail', pk=loan.book.pk)

def loan_create(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST' and book.available_copies() > 0:
        reader_id = request.POST.get('reader_id')
        due_date = request.POST.get('due_date')
        if reader_id and due_date:
            Loan.objects.create(book=book, due_date=due_date, reader_id=reader_id)
    return redirect('book_detail', pk=book.pk)


def library_stats(request):
    # 1. Топ-3 найактивніших читачів
    top_readers = Reader.objects.annotate(
        total_loans=Count('loans')
    ).order_by('-total_loans')[:3]

    # 2. Прострочені позики
    today = timezone.now().date()
    overdue_loans = Loan.objects.filter(
        returned_at__isnull=True,
        due_date__lt=today
    ).select_related('book', 'reader')

    # 3. Кількість книг за авторами
    author_stats = Author.objects.annotate(
        total_books=Count('books')
    ).order_by('-total_books')

    # 4. Бенчмарк швидкості на 1 000 000 елементів
    benchmark_data = benchmark_search()

    context = {
        'top_readers': top_readers,
        'overdue_loans': overdue_loans,
        'author_stats': author_stats,
        'benchmark_data': benchmark_data,
    }
    return render(request, 'library/stats.html', context)



