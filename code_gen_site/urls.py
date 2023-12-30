from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('suggest/', views.suggest, name='suggest'),
  path('login/', views.login_user_fn, name='login'),
  path('logout/', views.logout_user_fn, name='logout'),
  path('register/', views.register_user_fn, name='register'),
  path('history/', views.history_user_fn, name='history'),
  path('delete_history/<History_id>', views.delete_history_fn, name='delete_history'),
]