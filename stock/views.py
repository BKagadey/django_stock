import requests
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StockForm
from .models import Stock
# Create your views here.


def home(request):
    token = 'pk_f7b16ba036ca413fa34f'

    if request.method == "POST":
        ticker = request.POST['ticker']
        url = f'https://cloud.iexapis.com/stable/stock/{ticker}/quote?token={token}'
        api_request = requests.get(url)
        
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        
        return render(request, 'home.html', {'api': api})

    else:
        return render(request, 'home.html', {'ticker': 'Enter a Ticker Symbol'})

    
def about(request):
    return render(request, 'about.html', {})

    
def add_stock(request):
    if request.method == "POST":
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ('Stock has been Added'))
            return redirect('add_stock')
    else:
        ticker = Stock.objects.all()
        token = 'pk_f7b16ba036ca413fa34fb7958a8a43c0'
        output = []
        for ticker_item in ticker:
            url = f'https://cloud.iexapis.com/stable/stock/{ticker_item}/quote?token={token}'
            api_request = requests.get(url)
            
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."

        return render(request, 'add-stock.html', {'ticker': ticker, 'output': output})

def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ('Stock deleted!'))
    return redirect('add_stock')

def delete_stock(request):
    
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker':ticker})
