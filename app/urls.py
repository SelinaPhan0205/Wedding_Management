
from django.contrib import admin
from django.urls import path, include
from . import views, api


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
    path('baocaodoanhthu/', views.baocaodoanhthu, name='baocaodoanhthu'),
    path('baocaocongno/', views.baocaocongno, name='baocaocongno'),
    path('baocaothucthu/', views.baocaothucthu, name='baocaothucthu'),
    path('api/dangnhap/', api.dangnhap_api, name='api_dangnhap'),
    path('api/thong-tin-tai-khoan/', api.thong_tin_tai_khoan, name='api_thong_tin_tai_khoan'),
    path('api/', include('app.api')),
    path('dangnhap/', views.dangnhap, name='dangnhap'),
]