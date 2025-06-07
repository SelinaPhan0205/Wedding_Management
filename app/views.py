from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django.core.paginator import Paginator
from .models import *
from .serializers import *
from unidecode import unidecode

##### SẢNH #####
def trangchu(request):
    return render(request, 'app/trangchu.html')
def quanlytaikhoan(request):
    return render(request, 'app/quanlytaikhoan.html')
def quanlysanh(request):
    return render(request, 'app/quanlysanh.html')
def quanlytieccuoi(request):
    return render(request, 'app/quanlytieccuoi.html')
def quanlyhoadon(request):
    return render(request, 'app/quanlyhoadon.html')
def quanlythucdon(request):
    return render(request, 'app/quanlythucdon.html')
def quanlydichvu(request):
    return render(request, 'app/quanlydichvu.html')
def quanlyquydinh(request):
    return render(request, 'app/quanlyquydinh.html')
def xembaocao(request):
    return render(request, 'app/xembaocao.html')

class LoaiSanhViewSet(viewsets.ModelViewSet):
    queryset = LoaiSanh.objects.all()
    serializer_class = LoaiSanhSerializer

class SanhViewSet(viewsets.ModelViewSet):
    queryset = Sanh.objects.all()
    serializer_class = SanhSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search_query = request.query_params.get('search', '').strip()
        
        for sanh in queryset:
            ten_sanh = sanh.ten_sanh.strip().lower()

        if search_query:
            filtered = []
            for sanh in queryset:
                ten_sanh = sanh.ten_sanh.strip().lower()
                if ten_sanh.startswith(search_query):
                    filtered.append(sanh)
            queryset = filtered

        # Sắp xếp theo thứ tự chữ cái tên sảnh (không phân biệt hoa thường)
        queryset = sorted(queryset, key=lambda s: s.ten_sanh.lower())

        # Phân trang
        page = request.query_params.get('page', 1)
        limit = int(request.query_params.get('limit', 8))
        paginator = Paginator(queryset, limit)
        page_obj = paginator.page(page)

        serializer = self.get_serializer(page_obj, many=True)
        return Response({
            'data': serializer.data,
            'total': paginator.count
        })

    @action(detail=False, methods=['get'], url_path='count')
    def count(self, request):
        search_query = request.query_params.get('search', '').strip()
        queryset = self.get_queryset()

        # Lọc sảnh theo tên bắt đầu bằng search_query
        if search_query:
            queryset = queryset.filter(ten_sanh__istartswith=search_query)

        return Response({'total': queryset.count()})

# Thêm viewset cho Tài Khoản (nếu cần cho quản lý tài khoản)
class TaiKhoanViewSet(viewsets.ModelViewSet):
    queryset = TaiKhoan.objects.all().select_related('user')
    serializer_class = TaiKhoanSerializer
    filter_backends = [SearchFilter]
    search_fields = ['hovaten', 'sodienthoai', 'user__email', 'user__username']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = request.query_params.get('page', 1)
        limit = int(request.query_params.get('limit', 8))
        
        paginator = Paginator(queryset, limit)
        page_obj = paginator.page(page)
        
        serializer = self.get_serializer(page_obj, many=True)
        return Response({
            'data': serializer.data,
            'total': paginator.count
        })

    @action(detail=False, methods=['get'], url_path='count')
    def count(self, request):
        search_query = request.query_params.get('search', '')
        queryset = self.filter_queryset(self.get_queryset())
        return Response({'total': queryset.count()})