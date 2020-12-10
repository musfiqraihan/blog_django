from django.contrib import admin
from .models import Author, Category, Article, Comment

admin.site.site_header = 'BLOG ADMIN PANEL'


class AuthorModel(admin.ModelAdmin):
    # search_fields = ["__str__", "name"]
    list_display = ["__str__", "email"]

    class Meta:
        model = Author


admin.site.register(Author, AuthorModel)


class CategoryModel(admin.ModelAdmin):
    # search_fields = ["__str__"]
    list_display = ["__str__"]
    list_per_page = 10

    class Meta:
        model = Category


admin.site.register(Category, CategoryModel)


class ArticleModel(admin.ModelAdmin):
    # search_fields = ["__str__", "details"]
    list_display = ["__str__", "category", "posted_on"]
    list_per_page = 10
    list_filter = ["posted_on", "category"]

    class Meta:
        model = Article


admin.site.register(Article, ArticleModel)


class CommentModel(admin.ModelAdmin):
    # search_fields = ["__str__", ]
    list_display = ["__str__", "name", "post_comment"]
    list_per_page = 10

    class Meta:
        model = Comment


admin.site.register(Comment, CommentModel)
