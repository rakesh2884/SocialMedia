from social_platform import views
from django.urls import path
app_name = 'social_platform'

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('login/',views.LoginAPIView.as_view(),name="login"),
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),
    path('account/', views.AccountView.as_view(),name='account'),
    path('posts/', views.Posts.as_view(),name='posts'),
    path('like/', views.Likes.as_view(),name='like'),
    path('comment/', views.Comments.as_view(),name='comment'),
    path('viewLiked/', views.viewLikedPost.as_view(),name='liked'),
]