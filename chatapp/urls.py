from django.urls import path

from . import views

app_name='chatapp'

urlpatterns = [
    path('<str:room_name>/', views.room, name='room'),
    path('', views.room, name='room_bare'),
    path('users/listall/', views.list_user),
    path('create/new/', views.chat_create_view, name='chat_create'),
    # path('detail/<int:pk>', views.chat_detail_view, name='chat_detail'),
    # path('update/<int:pk>', views.chat_update_view, name='chat_update'),
    # path('delete/<int:pk>', views.chat_delete_view, name='chat_delete'),
]