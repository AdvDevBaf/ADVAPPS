from django.db import models
from datetime import datetime

# Create your models here.

STATUS_CHOISES = (
    ('d','Draft'),
    ('p','published'),
)

class Category(models.Model):
    name = models.CharField('Name',max_length=50)
    slug = models.SlugField('Slug')

    def __str__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class PostManager(models.Manager):
    def published(self):
        return self.filter(draft=False)
    def drafted(self):
        return self.filter(draft=True)

class BlogPost(models.Model):
    title = models.CharField('Title',max_length=50)
    slug = models.SlugField('Slug')
    tease = models.TextField('Tease(summary)', blank=True)
    body = models.TextField('Content')
    draft = models.BooleanField('Is draft',default=True)
    status = models.CharField(max_length=1,choices=STATUS_CHOISES,
                              default='d')
    created_date = models.DateTimeField('Date of creation',default=datetime.now)
    published_date = models.DateTimeField('Date of publication',default=datetime.now)
    category = models.ForeignKey(Category,related_name='entries', on_delete=models.DO_NOTHING)

    objects = PostManager()


    def __str__(self):
        return u'%s' % self.title

    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        ordering = ('-published_date',)


    #@models.permalink
    def get_absolute_url(self):
        return ('blog_details', ())


class Data(models.Model):
    pass