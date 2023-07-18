from django.urls import path
from . import views
app_name = 'MChat'
urlpatterns = [
    path('chat/', views.messages_page, name='chat-view'),
]
