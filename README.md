# 📚 Міні-бібліотека (Django + PostgreSQL + Docker)

Тестове завдання на позицію **Trainee Backend Developer**.  
Повноцінний веб-сервіс для обліку книг, авторів, читачів та історії позик з кастомними алгоритмічними структурами даних та аналітичним дашбордом.

---

## 🛠 Технологічний стек
- **Мова:** Python 3.12 / 3.14
- **Фреймворк:** Django 6.1
- **База даних:** PostgreSQL 16 (контейнеризована)
- **Контейнеризація:** Docker & Docker Compose
- **Інтерфейс:** HTML5, Django Template Language (DTL), Bootstrap 5 (CDN)
- **Алгоритми:** Кастомні структури даних (без вбудованого `deque`/`queue`), бінарний пошук $O(\log N)$, Unit-тести

---

## 🚀 Швидкий запуск у Docker (для будь-якого комп'ютера)

Щоб запустити проєкт на будь-якій системі (macOS, Linux, Windows), потрібен лише встановлений **Docker Desktop**.

### 1. Клонувати репозиторій:
```bash
git clone https://github.com/ognovix-svg/mini-library.git
cd mini-library
```

### 2. Запустити контейнери (Django + PostgreSQL):
```bash
docker compose up -d --build
```
> Docker автоматично завантажить образ PostgreSQL 16, збере образ Django, налаштує внутрішню мережу та запустить сервіси.

### 3. Застосувати міграції:
```bash
docker compose exec web python manage.py migrate
```

### 4. Наповнити базу демонстраційними даними (Seed Data):
Ми створили спеціальну команду, яка автоматично створить суперкористувача, 5 авторів, 10 книг, 3 читачів та історію позик:
```bash
docker compose exec web python manage.py seed_data
```

---

## 🌐 Доступ до додатку в браузері

- 📖 **Каталог книг:** [http://localhost:8000/books/](http://localhost:8000/books/) (або [http://localhost:8000/](http://localhost:8000/))
- ➕ **Додати нову книгу:** [http://localhost:8000/books/new/](http://localhost:8000/books/new/)
- 📊 **Аналітика та статистика:** [http://localhost:8000/stats/](http://localhost:8000/stats/)
- 🔐 **Панель адміністратора:** [http://localhost:8000/admin/](http://localhost:8000/admin/)
  - **Логін:** `admin`
  - **Пароль:** `admin1234`

---

## 🧪 Запуск автоматичних Unit-тестів
Усі кастомні структури даних покрито модульними тестами:
```bash
docker compose exec web python manage.py test library
```

---

## 🧩 Реалізовані алгоритми та структури (`library/structures.py`)
1. **Стек (Stack):** реалізація принципу LIFO для історії переглядів сторінок.
2. **Черга (Queue) на зв'язному списку (`Node`):** принцип FIFO без використання `list.pop(0)` — операції додавання і вилучення виконуються за $O(1)$.
3. **Словниковий покажчик (`build_index`):** групування книг за першою літерою в хеш-таблицю $O(1)$.
4. **Бінарний пошук (`binary_search`):** пошук книги за ISBN за $O(\log N)$ + інтерактивний бенчмарк на 1 000 000 елементів (прискорення у ~3800 разів порівняно з лінійним пошуком).

---

## 🛑 Зупинка контейнерів
```bash
docker compose down
```
> Дані бази зберігаються у Docker Volume `postgres_data` і не зникають при перезапуску.
