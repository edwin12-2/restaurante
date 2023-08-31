from django.urls import path
from django.contrib.auth import views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.handleIngresar, name='handleIngresar'),
    path('signup/', views.handleRegistro, name='handleRegistro'),
    path('logout/', views.handleSalir, name='handleSalir'),
    path('buscar/', views.buscar, name='buscar'),
    path('verificar/', views.verificar, name='verificar'),
    path('rastreo/', views.rastreo, name='rastreo'),
    path('verProducto/<int:myid>', views.verProducto, name='verProducto'),
    path('verPedido/', views.verPedido, name='verPedido'),

]