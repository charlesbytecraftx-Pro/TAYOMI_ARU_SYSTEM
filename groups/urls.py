from django.urls import path
from . import views

urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('join/<int:group_id>/', views.join_group, name='join_group'),
    path('members/<int:group_id>/', views.group_members_view, name='group_members_view'),
]
