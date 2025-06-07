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
        
        # Lọc sảnh theo tên bắt đầu bằng search_query (không phân biệt hoa thường và dấu)
        if search_query:
            if search_query != unidecode(search_query):
                # Người dùng nhập có dấu: chỉ so với tên sảnh gốc (có dấu)
                queryset = [sanh for sanh in queryset if search_query.lower() in sanh.ten_sanh.lower()]
            else:
                # Người dùng nhập không dấu: chỉ so với tên sảnh đã bỏ dấu
                search_query_unaccent = search_query.lower()
                queryset = [sanh for sanh in queryset if search_query_unaccent in unidecode(sanh.ten_sanh).lower()]

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