from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponse
from .models import Sanh, TaiKhoan, LoaiSanh, MonAn, DichVu, QuyDinh, TiecCuoi, HoaDon, ChiTietThucDon, ChiTietDichVu
from .serializers import (
    SanhCuoiSerializer, TaiKhoanSerializer, LoaiSanhSerializer, MonAnSerializer, DichVuSerializer,
    QuyDinhSerializer, TiecCuoiSerializer, HoaDonSerializer,
    ChiTietThucDonSerializer, ChiTietDichVuSerializer
)

# Create your views here.
def trangchu(request):
    return render(request,'app/trangchu.html')
def quanlytaikhoan(request):
    return render(request,'app/quanlytaikhoan.html')
def quanlysanh(request):
    return render(request,'app/quanlysanh.html')
def quanlytieccuoi(request):
    return render(request,'app/quanlytieccuoi.html')
def quanlyhoadon(request):
    return render(request,'app/quanlyhoadon.html')
def quanlythucdon(request):
    return render(request,'app/quanlythucdon.html')
def quanlydichvu(request):
    return render(request,'app/quanlydichvu.html')
def quanlyquydinh(request):
    return render(request,'app/quanlyquydinh.html')
def xembaocao(request):
    return render(request,'app/xembaocao.html')

class SanhCuoiViewSet(viewsets.ModelViewSet):
    queryset = Sanh.objects.all()
    serializer_class = SanhCuoiSerializer

class TaiKhoanViewSet(viewsets.ModelViewSet):
    queryset = TaiKhoan.objects.all()
    serializer_class = TaiKhoanSerializer

class LoaiSanhViewSet(viewsets.ModelViewSet):
    queryset = LoaiSanh.objects.all()
    serializer_class = LoaiSanhSerializer

class MonAnViewSet(viewsets.ModelViewSet):
    queryset = MonAn.objects.all()
    serializer_class = MonAnSerializer

class DichVuViewSet(viewsets.ModelViewSet):
    queryset = DichVu.objects.all()
    serializer_class = DichVuSerializer

class QuyDinhViewSet(viewsets.ModelViewSet):
    queryset = QuyDinh.objects.all()
    serializer_class = QuyDinhSerializer

class TiecCuoiViewSet(viewsets.ModelViewSet):
    queryset = TiecCuoi.objects.all()
    serializer_class = TiecCuoiSerializer

class HoaDonViewSet(viewsets.ModelViewSet):
    queryset = HoaDon.objects.all()
    serializer_class = HoaDonSerializer

class ChiTietThucDonViewSet(viewsets.ModelViewSet):
    queryset = ChiTietThucDon.objects.all()
    serializer_class = ChiTietThucDonSerializer

class ChiTietDichVuViewSet(viewsets.ModelViewSet):
    queryset = ChiTietDichVu.objects.all()
    serializer_class = ChiTietDichVuSerializer