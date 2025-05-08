from celery import shared_task
from .models import StockEvent, Book

@shared_task
def process_stock_event(book_id, event_id, quantity):
    try:
        #update book stock
        book = Book.objects.get(id=book_id)
        book.stock += int(quantity)
        book.save()
        
        # #update event status
        event = StockEvent.objects.get(id=event_id)
        event.status = 'processed'
        event.save()
    except Exception as e:
        print(f"Error processing stock event: {e}")
        