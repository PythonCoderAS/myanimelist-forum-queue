from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('api/queue', views.api_queue_view, name='api_queue'),
]
