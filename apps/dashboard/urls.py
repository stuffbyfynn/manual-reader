from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('users/', views.user_list, name='user_list'),
    path('users/approve/<int:user_id>/', views.approve_user, name='approve_user'),
    path('users/block/<int:user_id>/', views.block_user, name='block_user'),
    path('invitations/', views.invitation_list, name='invitation_list'),
    path('invitations/create/', views.create_invitation, name='create_invitation'),
]
