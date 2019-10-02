from django.db import models
from datetime import datetime
from dbmail import send_db_mail
from dbmail.models import MailTemplate
from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history.models import HistoricalRecords
from wiki.models import Article, ArticleRevision
from simple_history import register
from django.db.models import signals
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.


STATUS_CHOISES = (
    ('d', 'Draft'),
    ('p', 'published'),
)


class Category(models.Model):
    name = models.CharField('Name', max_length=50)
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
    title = models.CharField('Title', max_length=50)
    slug = models.SlugField('Slug')
    tease = models.TextField('Tease(summary)', blank=True)
    body = models.TextField('Content')
    draft = models.BooleanField('Is draft', default=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOISES,
                              default='d')
    created_date = models.DateTimeField('Date of creation', default=datetime.now)
    published_date = models.DateTimeField('Date of publication', default=datetime.now)
    category = models.ForeignKey(Category, related_name='entries', on_delete=models.DO_NOTHING)

    objects = PostManager()

    def __str__(self):
        return u'%s' % self.title

    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        ordering = ('-published_date',)

    # @models.permalink
    def get_absolute_url(self):
        return ('blog_details', ())


OPTION_CHOISE = (
    ('n', 'No'),
    ('s', 'sended'),
)


class MTemplate(models.Model):
    name = models.CharField('Name', max_length=50, default='default_template')
    draft = models.BooleanField('Is send', default=True)
    status = models.CharField(max_length=1, choices=OPTION_CHOISE,
                              default='n')


class Polls(models.Model):
    name = models.CharField('Name', max_length=50, default='default_poll')
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    history = HistoricalRecords()


def check_model(sender, instance, created, **kwargs):
    user = User.objects.get(pk=1)
    field_value_time = ArticleRevision.history.all()[0]
    obj = ArticleRevision.objects.all()[0]
    field_name = 'title'
    field_value_name = getattr(obj, field_name)
    field_name = 'content'
    field_value_content = getattr(obj, field_name)
    field_name = 'user'
    field_value_user = getattr(obj, field_name)
    MailTemplate.objects.create(
        name="Article was changed",
        subject="Article changed",
        message="Article '" + str(field_value_name) + "' was changed by" + str(field_value_user) + " in " +
                str(field_value_time) + ". Now content of the '" + str(field_value_name) + "' is " + str(field_value_content),
        slug="Article was changed in " + str(datetime.now().date().strftime("%d/%m/%y")) + " " + str(datetime.now().time().strftime("%H:%M")),
        is_html=False,
    )

    usermails =  User.objects.all()
    for users in usermails:
        send_db_mail("Articlewaschangedin" + str(datetime.now().date().strftime("%d%m%y")) + "" +
                     str(datetime.now().time().strftime("%H%M")), users.email, use_celery=False)
    send_db_mail("Articlewaschangedin" + str(datetime.now().date().strftime("%d%m%y")) + "" +
                 str(datetime.now().time().strftime("%H%M")), user.email, use_celery=False)


signals.post_save.connect(check_model, sender=ArticleRevision)

register(ArticleRevision)
