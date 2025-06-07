from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import (
    SanhCuoiViewSet, TaiKhoanViewSet, LoaiSanhViewSet, MonAnViewSet, DichVuViewSet,
    QuyDinhViewSet, TiecCuoiViewSet, HoaDonViewSet,
    ChiTietThucDonViewSet, ChiTietDichVuViewSet
)

router = DefaultRouter()
router.register(r'sanh', SanhCuoiViewSet)
router.register(r'taikhoan', TaiKhoanViewSet)
router.register(r'loaisanh', LoaiSanhViewSet)
router.register(r'monan', MonAnViewSet)
router.register(r'dichvu', DichVuViewSet)
router.register(r'quydinh', QuyDinhViewSet)
router.register(r'tieccuoi', TiecCuoiViewSet)
router.register(r'hoadon', HoaDonViewSet)
router.register(r'chitietthucdon', ChiTietThucDonViewSet)
router.register(r'chitietdichvu', ChiTietDichVuViewSet)

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
    path('api/', include(router.urls)),
]