from django.shortcuts import render
from bs4 import BeautifulSoup


# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    search_string = request.POST.get('search')
    print(search_string)
    stuff_for_frontend = {
        'search': search_string,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)

