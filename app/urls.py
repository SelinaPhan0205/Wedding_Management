from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.trangchu, name='trangchu'),
    path('quanlytaikhoan/', views.quanlytaikhoan, name='quanlytaikhoan'),
    path('quanlysanh/', views.quanlysanh, name='quanlysanh'),
    path('quanlytieccuoi/', views.quanlytieccuoi, name='quanlytieccuoi'),
    path('quanlyhoadon/', views.quanlyhoadon, name='quanlyhoadon'),
    path('quanlythucdon/', views.quanlythucdon, name='quanlythucdon'),
    path('quanlydichvu/', views.quanlydichvu, name='quanlydichvu'),
    path('quanlyquydinh/', views.quanlyquydinh, name='quanlyquydinh'),
    path('xembaocao/', views.xembaocao, name='xembaocao'),
    path('api/', include('app.api')),
]