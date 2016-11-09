from django.db import models
from django.template.defaultfilters import slugify
# Create your models here.

class Bares(models.Model):
        name = models.CharField(max_length=128, unique=True)
        slug = models.SlugField()
        views = models.IntegerField(default=0)
        likes = models.IntegerField(default=0)
        def save(self, *args, **kwargs):
                # Uncomment if you don't want the slug to change every time the name changes
                #if self.id is None:
                        #self.slug = slugify(self.name)
                self.slug = slugify(self.name)
                if self.views<0:
                    self.views=0
                super(Bares, self).save(*args, **kwargs)

        def __unicode__(self):
                return self.name
class Tapas(models.Model):
    category = models.ForeignKey(Bares)
    title = models.CharField(max_length=128)
    url = models.URLField()
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.title
