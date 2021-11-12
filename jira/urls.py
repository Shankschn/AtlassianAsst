from django.urls import path
from . import views

urlpatterns = [
    path('group_users_op/', views.group_users_op),
]