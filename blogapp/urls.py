from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='index'),
    path('author/<name>', views.getauthor, name="author"),
    path('article/<int:id>', views.getsingle, name="single-post"),
    path('posts/<name>', views.getcategory, name="category"),
    path('post/new', views.create_post, name="create-post"),
    path('articles/all', views.get_all_blogs, name="all_blogs"),
    path('article/update/<int:pid>', views.update_post, name="update-post"),
    path('article/delete/<int:pid>', views.delete_post, name="delete-post"),
    path('profile/update/<name>', views.update_profile, name="update-profile"),

    # path('topics', views.getTopic, name="topics"),
    # path('topics/update/<int:pid>', views.update_topics, name="update-topics"),
    # path('topics/delete/<int:pid>', views.delete_topics, name="delete-topics"),
]
