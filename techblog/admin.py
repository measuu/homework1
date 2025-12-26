from django.contrib import admin
from django.contrib import admin
from .models import Article, Tag
from django.http import HttpResponse
import csv


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'views', 'likes', 'is_featured', 'published_at']
    list_filter = ['is_featured', 'published_at', 'author', 'tags']
    search_fields = ['title', 'content']
    list_editable = ['is_featured']
    filter_horizontal = ['tags']
    readonly_fields = ['views', 'likes']


@admin.action(description="Позначити як Featured")
def make_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)


@admin.action(description="Скинути перегляди (views)")
def reset_views(modeladmin, request, queryset):
    queryset.update(views=0)


@admin.action(description="Експорт обраних статей (CSV)")
def export_articles_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="articles.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Title', 'Author', 'Views', 'Likes',
        'Featured', 'Published At'
    ])

    for article in queryset:
        writer.writerow([
            article.title,
            article.author.username,
            article.views,
            article.likes,
            article.is_featured,
            article.published_at
        ])

    return response