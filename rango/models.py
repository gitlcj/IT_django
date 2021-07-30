from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    NAME_MAX_LENGTH = 128
    name = models.CharField(max_length=128,unique=True)
    views = models.IntegerField(default=0)
    likes =models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    #*args is tuple, **kwargs is dictionary
    #slugify: change blank space to -
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args,**kwargs)

    #modify categorys to Categories in admin interface
    class Meta:
        verbose_name_plural = 'Categories'


    def __str__(self):
        return self.name


class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url =models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    #The value of this attribute is conjoined with the project’s MEDIA_ROOT setting to provide a path with which uploaded profile images will be stored.
    #<workspace>/tango_with_django_project/media/profile_images/.
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username