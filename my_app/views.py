from django.shortcuts import render
from bs4 import BeautifulSoup

from . import models
from .models import Search
from requests.compat import quote_plus
import requests


BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    search_string = request.POST.get('search')
    if search_string is None:
        search_string = ''
    print(quote_plus(search_string))
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search_string))
    print(final_url)
    temp_search = models.Search.objects.create(search=search_string)
    temp_search.save()
    # url = "https://losangeles.craigslist.org/search/sss?query=beauty&sort=rel"
    response = requests.get(final_url)

    data = response.text

    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})
    post_title = post_listings[0].find(class_='result-title').text
    post_url = post_listings[0].find('a').get('href')
    post_price = post_listings[0].find(class_='result-price')
    final_postings = []
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search_string,
        'final_postings': final_postings
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)

