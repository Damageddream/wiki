from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_name>", views.entry, name="entry"),
    path("/", views.query, name="query"),
    path("new_page", views.new_page, name="new_page"),
    path("wiki/<str:entry_name>/edit", views.edit, name="edit"),
    path("random_page", views.random_page, name="random_page"),
    
]
