#import django model
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page
# create some dictionaries and list the pages you want to add to each category
# Then create a nested dictionary and set each category
# it is easy to iterate and add data to the model
def populate():
    python_pages = [
        {"title": "Official Python Tutorial",
         "url": "http://docs.python.org/2/tutorial/"},
        {"title": "How to Think like a Computer Scientist",
         "url": "http://www.greenteapress.com/thinkpython/"},
        {"title": "Learn Python in 10 Minutes",
         "url": "http://www.korokithakis.net/tutorials/python/"}]
    django_pages = [
        {"title": "Official Django Tutorial",
         "url": "https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
        {"title": "Django Rocks",
         "url": "http://www.djangorocks.com/"},
        {"title": "How to Tango with Django",
         "url": "http://www.tangowithdjango.com/"}]
    other_pages = [
        {"title": "Bottle",
         "url": "http://bottlepy.org/docs/dev/"},
        {"title": "Flask",
         "url": "http://flask.pocoo.org"}]
    cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
            'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
            'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16}}

    #If you want to add more categories or web pages, just add them to the previous dictionary
    # The following code iterates the cats dictionary, adds each category, and adds relevant web pages to the category
    # If you are using Python 2. X, iterate using cats. Iteritems()

    for cat, cat_data in cats.items():
        c= add_cat(cat,views=cat_data['views'],likes=cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'])

    #terminal print
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views=0):
    #get_or_create: create  model instance return a tuple (object, created),[0] means object instance
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name,views=0, likes =0):
    #create cat instance and save
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes =likes
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()


