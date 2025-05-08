from django.utils.timezone import now, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book, StockEvent
from .serializers import BookSerializer
from .tasks import process_stock_event


class buyClientBookView(APIView):
    
    def post(self, request, book_id):
        
        book = get_object_or_404(Book, pk=book_id)
        
        # Validate the request data
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data['quantity']

        # check if the book is in stock
        if book.stock < quantity:
            return Response({"error": "Not enough stock available."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the book stock
        book.stock -= quantity
        book.save()

        #create event
        event = StockEvent(
            book=book,
            quantity=quantity,
            scheduled_for= now() + timedelta(minutes=1),
            status='pending'
        )
        event.save()

        #create celery task
        process_stock_event.apply_async(
            (book.id, event.id, quantity),
            eta=event.scheduled_for
        )

        return Response({"message": "Book purchased successfully!"}, status=status.HTTP_200_OK)