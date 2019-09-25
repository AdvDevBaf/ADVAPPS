from django.contrib import admin
from .models import BlogPost,Category
from datetime import datetime
# Register your models here.





class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',),
    }

    list_display = ('name', 'slug')


def make_published(modeladmin,request,queryset):
    queryset.update(status='p', draft=False)
    queryset.update(published_date=datetime.now())


make_published.short_description='Make selected posts as published'


def make_draft(modeladmin,request,queryset):
    queryset.update(status='d', draft=True)
    queryset.update(published_date=datetime.now())


make_draft.short_description='Make selected posts as draft'



class BlogEntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',),
    }

    list_display = ['title', 'draft','status','created_date', 'published_date',]
    list_display_links = ('title',)
    list_filter = ('created_date', 'published_date', 'draft')
    date_hierarchy = 'created_date'
    search_fields = ('title', 'tease', 'body')
    actions=[make_published, make_draft]

    exclude = ('created_date',)
    fieldsets = (
        (None, {'fields': ('slug', 'title', 'tease', 'body')}),
        ('Properties', {'fields': ('draft', 'published_date', 'category')}),
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(BlogPost, BlogEntryAdmin)