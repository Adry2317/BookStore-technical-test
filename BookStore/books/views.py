from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from .models import Book, StockEvent
from .forms import BookForm
from .tasks import process_stock_event


# Bookstore worker view
def home(request):
    return render(request, "home.html")


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    
    user = authenticate(
        request=request,
        username=request.POST['username'],
        password=request.POST['password']
    )

    if user is None:
        return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'Username or password is incorrect.'
        })

    login(request, user),
    return redirect('home')

@login_required
def sign_out(request):
    logout(request)
    return redirect('home')

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

@login_required
def book_delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    
@login_required
def book_edit(request, book_id):
    if request.method == 'GET':
        book = get_object_or_404(Book, pk=book_id)
        form = BookForm(instance=book)
        return render(request, 'book_edit.html',{
            'book': book,
            'form': form
        })
    else:
        try:
            book = get_object_or_404(Book, pk=book_id)
            form = BookForm(request.POST,instance=book)
            form.save()
            return redirect('book_list')
        except ValueError:
            return render(request, 'book_edit.html',{
                'book': book,
                'form': form,
                'error': 'Error updating book'
            })

@login_required
def buy_book_stock(request, book_id):
    if request.method == 'GET':
        book = get_object_or_404(Book, pk=book_id)
        return render(request, 'book_stock.html', {
            'book': book,
        })
    
    else:
        try:
            book = get_object_or_404(Book, pk=book_id)
            quantity = int(request.POST['quantity'])
            
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
        
            

            return redirect('book_list')
        except Exception:
            return render(request, 'book_stock.html', {
                'book': book,
                'error': 'Error buying book stock'
            })
@login_required
def buy_new_book(request):
    if request.method == 'GET':
        return render(request, 'book_new.html', {
            'form': BookForm()
        })
    else:
        try:
            form = BookForm(request.POST)
            form.save()
            return redirect('book_list')
        except ValueError:
            return render(request, 'book_new.html', {
                'form': BookForm(),
                'error': 'Error creating book'
            })

@login_required
def event_list(request):
    events_pending = StockEvent.objects.filter(status='pending')
    events_completed = StockEvent.objects.filter(status='processed')
    return render(request, 'event_panel.html', {
        'events_pending': events_pending,
        'events_completed': events_completed
        })