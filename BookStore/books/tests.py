from django.forms import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now, timedelta
from .models import Book, StockEvent
from django.contrib.auth.models import User
from .tasks import process_stock_event

# Create your tests here.
class BuyClientBookTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(title="Test Book", price=10.00, stock=5)
        self.url = reverse('buy_client_book', args=[self.book.id])

    def test_buy_book_success(self):
        response = self.client.post(self.url, {'quantity': 2})
        self.assertEqual(response.status_code, 200)
        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 3)  

    def test_buy_book_invalid_quantity(self):
        response = self.client.post(self.url, {'quantity': -1})
        self.assertEqual(response.status_code, 400)  
        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 5)

    def test_buy_book_not_enough_stock(self):
        response = self.client.post(self.url, {'quantity': 10})
        self.assertEqual(response.status_code, 400)
        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 5)
    

class AddStockTask(TestCase):
    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(title="Test Book", price=10.00, stock=5)
        self.event = StockEvent.objects.create(book=self.book, quantity=5, scheduled_for=now(), status='pending')

    def test_add_stock_task(self):
        
        process_stock_event(self.book.id, self.event.id, 5)
        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 10)
        self.event.refresh_from_db()
        self.assertEqual(self.event.status, 'processed')

class WorkAddStockTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')
        self.book = Book.objects.create(title="Test Book", price=10.00, stock=5)
        self.url = reverse('buy_book_stock', args=[self.book.id])
        
    def test_work_add_stock(self):
        response = self.client.post(self.url, {'quantity': 5})
        self.assertEqual(response.status_code, 302) # Redirect after successful purchase
        self.assertRedirects(response, reverse('book_list'))
        # We dont check the stock here because the task is async.
        

class BookModelTest(TestCase):
    
    def test_book_negative_stock(self):
        book = Book.objects.create(title="Test Book", price=10.00, stock=-1)
        with self.assertRaises(ValidationError):     
            book.full_clean()

    def test_book_price(self):
        book = Book.objects.create(title="Test Book", price=-10.00, stock=5)
        with self.assertRaises(ValidationError):     
            book.full_clean()


class StockEventModelTest(TestCase):

    def setUp(self):
        self.book = Book.objects.create(title="Test Book", price=10.00, stock=5)
        
    def test_create_valid_stock_event(self):
        event = StockEvent.objects.create(
            book=self.book,
            quantity=10,
            scheduled_for=now() + timedelta(days=1)
        )
        self.assertEqual(event.book, self.book)
        self.assertEqual(event.quantity, 10)
        self.assertEqual(event.status, 'pending')
    
    def test_stock_event_negative_quantity(self):
        event = StockEvent.objects.create(book=self.book, quantity=-1, scheduled_for=now(), status='pending')
        with self.assertRaises(ValidationError):     
            event.full_clean()
    
    

