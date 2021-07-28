from django.urls import path
from rango import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/',views.about,name ='about'),
    #parameterised URL Mapping
    #pass the value of category_name_slug parameter to show_category function
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
]