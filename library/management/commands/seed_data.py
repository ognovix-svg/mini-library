import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from library.models import Author, Book, Reader, Loan


class Command(BaseCommand):
    help = "Наповнює базу даних тестовими даними (Seed Data) для демонстрації"

    def handle(self, *args, **options):
        self.stdout.write("Початок наповнення бази даних...")

        # 1. Створення суперкористувача admin / admin1234
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@library.com", "admin1234")
            self.stdout.write(self.style.SUCCESS("✓ Суперкористувач створений (admin / admin1234)"))
        else:
            self.stdout.write("Суперкористувач admin вже існує.")

        # 2. Автори
        authors_data = [
            {"first_name": "Тарас", "last_name": "Шевченко", "birth_year": 1814},
            {"first_name": "Іван", "last_name": "Франко", "birth_year": 1856},
            {"first_name": "Леся", "last_name": "Українка", "birth_year": 1871},
            {"first_name": "Джордж", "last_name": "Орвелл", "birth_year": 1903},
            {"first_name": "Стівен", "last_name": "Кінг", "birth_year": 1947},
        ]
        authors = {}
        for a_data in authors_data:
            author, created = Author.objects.get_or_create(
                first_name=a_data["first_name"],
                last_name=a_data["last_name"],
                defaults={"birth_year": a_data["birth_year"]}
            )
            authors[f"{author.first_name} {author.last_name}"] = author
        self.stdout.write(self.style.SUCCESS(f"✓ Додано {len(authors)} авторів"))

        # 3. Книги
        books_data = [
            {"title": "Кобзар", "isbn": "9789660370011", "year": 1840, "copies": 4, "authors": ["Тарас Шевченко"]},
            {"title": "Гайдамаки", "isbn": "9789660370028", "year": 1841, "copies": 3, "authors": ["Тарас Шевченко"]},
            {"title": "Захар Беркут", "isbn": "9789660370035", "year": 1883, "copies": 3, "authors": ["Іван Франко"]},
            {"title": "Украдене щастя", "isbn": "9789660370042", "year": 1893, "copies": 2, "authors": ["Іван Франко"]},
            {"title": "Борислав сміється", "isbn": "9789660370059", "year": 1882, "copies": 2, "authors": ["Іван Франко"]},
            {"title": "Лісова пісня", "isbn": "9789660370066", "year": 1911, "copies": 4, "authors": ["Леся Українка"]},
            {"title": "Бояриня", "isbn": "9789660370073", "year": 1910, "copies": 2, "authors": ["Леся Українка"]},
            {"title": "1984", "isbn": "9780451524935", "year": 1949, "copies": 5, "authors": ["Джордж Орвелл"]},
            {"title": "Колгосп тварин", "isbn": "9780451526342", "year": 1945, "copies": 4, "authors": ["Джордж Орвелл"]},
            {"title": "Сяйво", "isbn": "9780307743657", "year": 1977, "copies": 3, "authors": ["Стівен Кінг"]},
        ]
        books = {}
        for b_data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=b_data["isbn"],
                defaults={
                    "title": b_data["title"],
                    "published_year": b_data["year"],
                    "copies_total": b_data["copies"],
                }
            )
            for a_name in b_data["authors"]:
                if a_name in authors:
                    book.authors.add(authors[a_name])
            books[book.isbn] = book
        self.stdout.write(self.style.SUCCESS(f"✓ Додано {len(books)} книг"))

        # 4. Читачі
        readers_data = [
            {"full_name": "Олег Петренко", "email": "oleg.petrenko@example.com"},
            {"full_name": "Марія Коваль", "email": "maria.koval@example.com"},
            {"full_name": "Іван Сидоренко", "email": "ivan.sydorenko@example.com"},
        ]
        readers = []
        for r_data in readers_data:
            reader, created = Reader.objects.get_or_create(
                email=r_data["email"],
                defaults={"full_name": r_data["full_name"]}
            )
            readers.append(reader)
        self.stdout.write(self.style.SUCCESS(f"✓ Додано {len(readers)} читачів"))

        # 5. Позики
        today = timezone.now().date()
        loans_plan = [
            # 3 активні позики
            {"book_isbn": "9780451524935", "reader_idx": 0, "due": today + datetime.timedelta(days=7), "ret": None},
            {"book_isbn": "9789660370011", "reader_idx": 1, "due": today + datetime.timedelta(days=14), "ret": None},
            {"book_isbn": "9780307743657", "reader_idx": 2, "due": today - datetime.timedelta(days=2), "ret": None}, # прострочена!
            # 2 повернуті позики
            {"book_isbn": "9789660370035", "reader_idx": 0, "due": today - datetime.timedelta(days=10), "ret": today - datetime.timedelta(days=3)},
            {"book_isbn": "9789660370066", "reader_idx": 1, "due": today - datetime.timedelta(days=5), "ret": today - datetime.timedelta(days=1)},
        ]
        created_loans_count = 0
        for l_data in loans_plan:
            book_obj = books.get(l_data["book_isbn"])
            reader_obj = readers[l_data["reader_idx"]]
            if book_obj and reader_obj:
                loan, created = Loan.objects.get_or_create(
                    book=book_obj,
                    reader=reader_obj,
                    due_date=l_data["due"],
                    defaults={"returned_at": l_data["ret"]}
                )
                if created:
                    created_loans_count += 1

        self.stdout.write(self.style.SUCCESS(f"✓ Підготовлено {len(loans_plan)} позик (з них одна прострочена для статистики)"))
        self.stdout.write(self.style.SUCCESS("База даних успішно наповнена тестовими даними!"))
