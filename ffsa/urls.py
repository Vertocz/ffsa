from django.urls import path, include
from django.contrib import auth, admin
from pole.views import *

urlpatterns = [
    path('', index, name="index"),
    path('admin/', admin.site.urls),
    path('membre/<int:id>', personne, name='personne'),
]
