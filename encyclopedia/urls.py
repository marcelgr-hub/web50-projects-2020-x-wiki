from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:query>", views.display, name="result"),
    path("newpage", views.new, name="newpage"),
    path("wiki/<str:query>/edit", views.edit, name="edit"),
    path("random", views.random, name="random")

]
