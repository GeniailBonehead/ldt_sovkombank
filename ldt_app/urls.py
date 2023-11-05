from django.urls import path
from ldt_app.views import *


urlpatterns = [
    path('', index),
    path('tasks', tasks),
    path('task_data/<int:pk>', task_data),
]
