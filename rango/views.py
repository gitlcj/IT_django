from django.shortcuts import render, redirect
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.urls import reverse
from rango.forms import UserForm, UserProfileForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

def index(request):
    #test cookie
    #request.session.set_test_cookie()
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

    # Call the helper function before render function
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    # Obtain our Response object early so we can add cookie information.
    response = render(request,'rango/index.html',context=context_dict)

    # Call the helper function to handle the cookies
    #visitor_cookie_handler(request, response)

    # Return response back to the user, updating any cookies that need changed.
    return response

def about(request):
    # if request.session.test_cookie_worked():
    #     print("TEST COOKIE WORKED!")
    #     request.session.delete_test_cookie()

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


#Display an empty form for users to add categories;
#store the data submitted by the user into the corresponding model, and then render the Rango application home page;
#if there is an error, display the form again and display the error message together.
@login_required
def add_category(request):
    #create an instance
    form = CategoryForm
    if request.method =='POST':

        #data from backend is added to this form
        form = CategoryForm(request.POST)
        if form.is_valid():
            #save the new category to the database
            cat = form.save(commit=True)
            print(cat)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)

    return render(request,'rango/add_category.html',{'form':form})


@login_required
def add_page(request,category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None

        # You cannot add a page to a Category that does not exist... DM
    if category is None:
        return redirect(reverse('rango:index'))


    # create an instance
    form = PageForm

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)  # This could be better done; for the purposes of TwD, this is fine. DM.

    context_dict = {'form': form, 'category': category}
    #print(context_dict)
    return render(request, 'rango/add_page.html', context=context_dict)

#user register
def register(request):
    # A boolean value for telling the template whether the registration was successful.Set to False initially.
    # Code changes value to True when registration succeeds.
    registered = False


    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user =user_form.save()
            # Now we hash the password with the set_password method.
            #  Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # the UserProfile contains a foreign key reference to the standard Django User model –
            #  but the UserProfile does not provide this information!
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user =user

            # Update our variable to indicate that the template  registration was successful.
            registered = True

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

                # Now we save the UserProfile model instance.
                profile.save()



        else:
        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)

    else:
    # Not a HTTP POST, so we render our form using two ModelForm instances. # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,'rango/register.html',context={'user_form':user_form,'profile_form': profile_form,
                             'registered': registered})




def user_login(request):
# If the request is a HTTP POST, try to pull out the relevant information.
     if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the value does not exist,
        #  while request.POST['<variable>'] # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Use Django's machinery to attempt to see if the username/password combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
            # If the account is valid and active, we can log the user in.
            #  We'll send the user back to the homepage.
                login(request, user)
                #Reverse looks up the URL patterns in Rango’s urls.py module to find a URL called rango:index,
                # and substitutes in the corresponding pattern.
                return redirect(reverse('rango:index'))
            else:
            # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
     # The request is not a HTTP POST, so display the login form.
     # This scenario would most likely be a HTTP GET.
     else:
        # No context variables to pass to the template system, hence the # blank dictionary object...
        return render(request, 'rango/login.html')

# a decorator function @login_required provided by Django that checks if the user is authenticated.
#Python will execute the decorator before executing the code of your function/
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


# Use the login_required() decorator to ensure only those logged in can # access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('rango:index'))


#useing cookie
# Get the number of visits to the site
def visitor_cookie_handler1(request, response):
 # We use the COOKIES.get() function to obtain the visits cookie.
 # If the cookie exists, the value returned is casted to an integer.
 #If the cookie doesn't exist, then the default value of 1 is used.
 #if the cookie exists,returns the value. If it does not exist, we can provide a default value
 #Note that all cookie values are returned as strings
    visits = int(request.COOKIES.get('visits','1'))


    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                     '%Y-%m-%d %H:%M:%S')

 # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
 # Update the last visit cookie now that we have updated the count response.set_cookie('last_visit', str(datetime.now()))
    else:
     # set the last visit cookie
     #create a cookie with the set_cookie() method of the response object you create.
     #the name of the cookie you wish to create (as a string), and the value of the cookie.
     #Django will automatically cast the value to a string.
        response.set_cookie('last_visit', last_visit_cookie)
 # Update/set the visits cookie
    response.set_cookie('visits', visits)




# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
 # request.session.get(): it accesses the cookies on the server- side.
 # and store them by placing them in the dictionary request.session[].
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

#use session: store information to server
# Updated the function definition
def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                            'last_visit',
                                            str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
    # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
     # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits