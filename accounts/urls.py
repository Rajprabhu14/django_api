from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('', views.UserListView.as_view()),
    path('create', views.CreateUser.as_view(), name='account-create'),
    re_path(r'activate/(?P<uidb64>)/(?P<token>)/$', views.activate_account,
            name='activate'),
]