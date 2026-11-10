from django.test import TestCase
from .structures import Stack, Queue, build_index, binary_search


class StackTestCase(TestCase):
    def test_stack_operations(self):
        stack = Stack()
        self.assertTrue(stack.is_empty())

        stack.push("Книга 1")
        stack.push("Книга 2")
        self.assertEqual(stack.size(), 2)
        self.assertEqual(stack.peek(), "Книга 2")

        # Перевірка LIFO: останній зайшов — перший вийшов
        self.assertEqual(stack.pop(), "Книга 2")
        self.assertEqual(stack.pop(), "Книга 1")
        self.assertTrue(stack.is_empty())

        # Перевірка помилки на порожньому стеку
        with self.assertRaises(IndexError):
            stack.pop()


class QueueTestCase(TestCase):
    def test_queue_operations(self):
        queue = Queue()
        self.assertTrue(queue.is_empty())

        queue.enqueue("Читач 1")
        queue.enqueue("Читач 2")
        self.assertEqual(queue.size(), 2)
        self.assertEqual(queue.peek(), "Читач 1")

        # Перевірка FIFO: перший зайшов — перший вийшов
        self.assertEqual(queue.dequeue(), "Читач 1")
        self.assertEqual(queue.dequeue(), "Читач 2")
        self.assertTrue(queue.is_empty())

        # Перевірка помилки на порожній черзі
        with self.assertRaises(IndexError):
            queue.dequeue()


class IndexTestCase(TestCase):
    def test_build_index(self):
        books = ["Кобзар", "Кайдашева сім'я", "1984", "Енеїда"]
        index = build_index(books)

        self.assertIn("К", index)
        self.assertEqual(len(index["К"]), 2)
        self.assertIn("Кобзар", index["К"])
        self.assertIn("Кайдашева сім'я", index["К"])
        self.assertIn("1", index)
        self.assertIn("Е", index)


class BinarySearchTestCase(TestCase):
    def test_binary_search(self):
        data = [10, 20, 30, 40, 50, 60, 70]

        # Пошук існуючих елементів
        self.assertEqual(binary_search(data, 10), 0)
        self.assertEqual(binary_search(data, 40), 3)
        self.assertEqual(binary_search(data, 70), 6)

        # Пошук неіснуючих елементів (має повернути -1)
        self.assertEqual(binary_search(data, 5), -1)
        self.assertEqual(binary_search(data, 99), -1)


from django.test import TestCase

# Create your tests here.
