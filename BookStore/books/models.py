from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2,validators=[MinValueValidator(0.01)])
    stock = models.IntegerField(default=0, 
                                validators=[MinValueValidator(0)])

    def __str__(self):
        return self.title


class StockEvent(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    date_added = models.DateTimeField(auto_now_add=True)
    scheduled_for = models.DateTimeField(null=False)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"{self.book.title} - {self.status}"