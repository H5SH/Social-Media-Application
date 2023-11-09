
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allpost", views.allpost, name='allpost'),
    path("likes/<int:post_id>/<str:username>", views.likes, name="likes"),
    path("following/<str:username>", views.following, name='following'),
    path("user/<str:username>/<str:current_user>", views.user, name="user")
]
