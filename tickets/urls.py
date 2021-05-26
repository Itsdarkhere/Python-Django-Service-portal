from django.urls import path
from . import views


urlpatterns = [
    path('welcome/', views.WelcomeView.as_view()),
    path('menu/', views.MenuView.as_view()),
    path('next', views.Next.as_view()),
    path('get_ticket/<str:link>/', views.Service.as_view()),
    path('processing', views.Processing.as_view())
]