from django.urls import path
from .views import my_view, my_view_second

urlpatterns = [
    path('weather/', my_view),
    path('weather2/', my_view_second),
]

