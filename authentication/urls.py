from django.urls import path

from authentication import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='api-login'),
    path('register/', views.Register.as_view(), name='api-register'),
    path('logout/', views.Logout.as_view(), name='api-logout'),
]
