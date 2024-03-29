from django.urls import path
from social_platform import views

app_name = 'users'

urlpatterns = [
    path("register",views.RegisterView.as_view(),name="api"),
    path("Login",views.LoginView.as_view(),name="api"),
    path("account",views.AccountView.as_view()),
    path("post",views.Posts.as_view())
]
