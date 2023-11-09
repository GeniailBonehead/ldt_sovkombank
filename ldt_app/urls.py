from django.urls import path
from ldt_app.views import *


urlpatterns = [
    path('', index),
    path('auth/<str:action>', auth),
    path('register', register),
    path('task', tasks),
    path('task/<int:pk>', task_data),
    path('profile/<int:pk>', profile_data),
    path('gis/<int:pk>', gis),
    path('task_history/<int:pk>', task_history),
    path('count', count),
]
