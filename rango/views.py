from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    #return HttpResponse("Rango says hey there partner<br/><a href='/rango/about/'>About</a>")
    #the key boldmessage matches to {{boldmessage}} in the template
    context_dict = {"boldmessage":  "Crunchy, creamy, cookie, candy, cupcake!"}
    return render(request,'rango/index.html',context=context_dict)

def about(request):
    #return HttpResponse("Rango says here is the about page.<br/> <a href='/rango/'>Index</a>")
    return render(request,'rango/about.html')
