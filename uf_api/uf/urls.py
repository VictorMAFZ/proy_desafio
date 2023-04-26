from django.urls import path
from . import views

urlpatterns = [
    path('uf/', views.uf_view, name='uf_view'),
]