from django.shortcuts import render
from .models import Apartment

def index(request):
    apartments = Apartment.objects.all()
    return render(request, "index.html", {'apartments': apartments})




