from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.UserListView.as_view()),
    path('create', views.CreateUser.as_view(), name='account-create')
]