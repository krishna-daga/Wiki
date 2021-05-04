from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.entrypage,name="title"),
    path("search",views.search,name="search"),
    path("create",views.create,name="newpage"),
    path("randompage",views.randompage,name="random"),
    path("<str:title>/edit",views.edit,name="edit"),
    path("wiki/<str:title>/save", views.save, name="save"),

]
