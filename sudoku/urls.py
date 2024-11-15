from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload_sudoku, name='upload_sudoku'),
    path("login", views.login_page, name='login_page'),
    path("logout", views.logout_page, name='logout_page'),
    path("register", views.register, name='register'),
    path("", views.index, name='home'),
]
