class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)


    def pop(self):
        if self.is_empty():
            raise IndexError('Стек порожній: неможливо виконати pop')
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Стек порожній: неможливо виконати peek")
        return self.items[-1]


    def is_empty(self):
        return len(self.items) == 0


    def size(self):
        return len(self.items)



class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def enqueue(self, item):
        new_node = Node(item)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1


    def dequeue(self):
        if self.is_empty():
            raise IndexError("Черга порожня: неможливо виконати dequeue")
        value = self.head.value
        self.head = self.head.next
        self._size -= 1
        if self.is_empty():
            self.tail = None
        return value


    def peek(self):
        if self.is_empty():
            raise IndexError("Черга порожня: неможливо виконати peek")
        return self.head.value


    def is_empty(self):
        return self._size == 0


    def size(self):
        return self._size


def build_index(books):
    index = {}
    for book in books:
        if isinstance(book, str):
            title = book
        elif hasattr(book, 'title'):
            title = book.title
        else:
            title = str(book)

        title = title.strip()
        if not title:
            continue

        first_letter = title[0].upper()
        if first_letter not in index:
            index[first_letter] = []
        index[first_letter].append(book)

    return index

import time


def binary_search(sorted_list, target):
    """
    Бінарний пошук у відсортованому списку.
    Повертає індекс знайденого елемента або -1, якщо елемент відсутній.
    Складність: O(log N).
    """
    left = 0
    right = len(sorted_list) - 1

    while left <= right:
        mid = (left + right) // 2
        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def benchmark_search():
    size = 1_000_000
    data = list(range(size))
    target = 999_999  # Шукаємо останній елемент (найгірший випадок для лінійного)

    # 1. Замір лінійного пошуку (O(N))
    start_time = time.perf_counter()
    linear_result = -1
    for i in range(len(data)):
        if data[i] == target:
            linear_result = i
            break
    linear_time = time.perf_counter() - start_time

    # 2. Замір бінарного пошуку (O(log N))
    start_time = time.perf_counter()
    binary_result = binary_search(data, target)
    binary_time = time.perf_counter() - start_time

    return {
        'size': size,
        'linear_time_sec': f"{linear_time:.6f}",
        'binary_time_sec': f"{binary_time:.8f}",
        'speedup': f"{linear_time / binary_time:.1f}x faster" if binary_time > 0 else "Instant",
    }