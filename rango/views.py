from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from django.http import HttpResponse

def index(request):
    #return HttpResponse("Rango says hey there partner<br/><a href='/rango/about/'>About</a>")
    #the key boldmessage matches to {{boldmessage}} in the template
    #context_dict = {"boldmessage":  "Crunchy, creamy, cookie, candy, cupcake!"}

    # Query the database to obtain all currently stored classifications
    # Sort by likes in reverse order
    # Get the first 5 categories (if the number of categories is less than 5, get all)
    #  put the category list into the context_ Dict dictionary
    # Pass it to the template engine later
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    return render(request,'rango/index.html',context=context_dict)

def about(request):
    #return HttpResponse("Rango says here is the about page.<br/> <a href='/rango/'>Index</a>")
    return render(request,'rango/about.html')



def show_category(request, category_name_slug):
    #create a context dictionary which we can pass to the template rendering engine
    context_dict ={}
    try:
        # Can I find the corresponding category through the incoming category alias?
        # If not found, the. Get () method throws a doesnotexist exception
        # Therefore, the. Get () method returns a model instance or throws an exception
        category = Category.objects.get(slug=category_name_slug)
    # Retrieve all associated pages
    # Notice that filter () returns a list of web page objects or an empty list
        pages = Page.objects.filter(category=category)
    # add resulting list to the template context under name pages
        context_dict['pages'] =pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    #go render the response and return it to client
    return render(request,'rango/category.html', context=context_dict)
