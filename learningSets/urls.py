from django.urls import path
from . import views

urlpatterns = [
    # path('create-set/', views.create_set, name='create_set'),
    path('create-set/', views.create_set_new, name='create_set'),
    # path('edit-set/<int:pk>/', views.edit_set, name='edit_set'),
    path('edit-set/<int:pk>/', views.edit_set_new, name='edit_set'),
    path('view-set/<int:pk>/', views.view_set, name='view_set'),
    path('delete-set/<int:pk>/', views.delete_set, name='delete_set'),
    path('delete-term/<int:pk>/', views.delete_term, name='delete_term'),
]