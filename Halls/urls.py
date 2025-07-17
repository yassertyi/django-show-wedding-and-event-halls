from django.urls import path
from . import views

app_name = 'halls'

urlpatterns = [
    path('', views.HallsListView.as_view(), name='halls_list'),
    path('client/', views.ClientHallsListView.as_view(), name='client_list'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.halls_add, name='halls_add'),
    path('edit_client/', views.edit_client, name='edit_client'),
    path('<slug:slug>/', views.halls_detail, name='halls_detail'),
    path('<int:halls_id>/shar/', views.halls_shar, name='halls_shar'),
    path('edit/<int:pk>/', views.halls_edit, name='halls_edit'),
    path('delete/<int:id>/', views.halls_delete, name='halls_delete'),
    
]
