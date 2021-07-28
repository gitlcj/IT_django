from django import forms
from rango.models import Category,Page


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length= Category.NAME_MAX_LENGTH , help_text="Please enter the category name.")
    # widget=forms.HiddenInput():In order to hide widgets
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    #an inline class to provide addition information on the form
    class Meta:
        #provide an association between the modelForm and model
        model = Category
        #incule name field of Category class
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        # Which fields do you want to put in the form?
        # Sometimes not all fields are needed
        # Some fields accept null values, so they may not need to be displayed
        # Here we want to hide the foreign key field
        # For this, you can exclude the category field
        exclude = ('category',)

    # URL checking
    def clean(self):
        cleaned_data = self.cleaned_data
        # cleaned_data is a dictionary
        url = cleaned_data.get('url')

        # null or not start with http:?//
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url

        return cleaned_data