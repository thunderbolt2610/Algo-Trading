from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
def index(request):

    return render(request, 'main/home.html')

def transactions(request):
    return render(request, 'main/transactions.html')