from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib import messages
from rest_framework.filters import SearchFilter
from django.core.paginator import Paginator
from .models import *
from .serializers import *
from django.contrib.auth.decorators import login_required

##### Code các yêu cầu #####

##### SẢNH #####
@login_required
def trangchu(request):
    return render(request, 'app/trangchu.html')
@login_required
def quanlytaikhoan(request):
    return render(request, 'app/quanlytaikhoan.html')
@login_required
def quanlysanh(request):
    return render(request, 'app/quanlysanh.html')
@login_required
def quanlytieccuoi(request):
    return render(request, 'app/quanlytieccuoi.html')
@login_required
def quanlyhoadon(request):
    return render(request, 'app/quanlyhoadon.html')
@login_required
def quanlythucdon(request):
    return render(request, 'app/quanlythucdon.html')
@login_required
def quanlydichvu(request):
    return render(request, 'app/quanlydichvu.html')
@login_required
def quanlyquydinh(request):
    return render(request, 'app/quanlyquydinh.html')
@login_required
def xembaocao(request):
    return render(request, 'app/xembaocao.html')


##### LOGIN #####
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            try:
                tai_khoan = TaiKhoan.objects.get(user=user)
                # Cả Admin và User đều redirect về trang chủ
                return redirect('trangchu')
            except TaiKhoan.DoesNotExist:
                messages.error(request, "Tài khoản không tồn tại trong hệ thống.")
                return redirect('login')
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
            return redirect('login')
    return render(request, 'app/login.html')

def custom_logout(request):
    logout(request)
    return redirect('login')

import unicodedata

def bo_dau(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

class LoaiSanhViewSet(viewsets.ModelViewSet):
    queryset = LoaiSanh.objects.all().order_by('gia_ban_toi_thieu')
    serializer_class = LoaiSanhSerializer

class SanhViewSet(viewsets.ModelViewSet):
    queryset = Sanh.objects.all().order_by('ten_sanh')
    serializer_class = SanhSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search_query = request.query_params.get('search', '').strip()
        
        # Lọc sảnh theo tên bắt đầu bằng search_query (không phân biệt hoa thường)
        if search_query:
            search_query_no_diacritics = bo_dau(search_query).lower().split()
            queryset = [
                s for s in queryset
                if all(
                    bo_dau(word).lower().startswith(q)
                    for word, q in zip(s.ten_sanh.split(), search_query_no_diacritics)
                )
            ]

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
    
class DichVuViewSet(viewsets.ModelViewSet):
    queryset = DichVu.objects.all().order_by('ten_dich_vu')
    serializer_class = DichVuSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search_query = request.query_params.get('search', '').strip().lower()

        if search_query:
            search_query_no_diacritics = bo_dau(search_query).lower()
            queryset = [
                dv for dv in queryset
                if bo_dau(dv.ten_dich_vu).lower().startswith(search_query_no_diacritics)
            ]

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
        search_query = request.query_params.get('search', '').strip().lower()
        queryset = self.get_queryset()

        if search_query:
            queryset = queryset.filter(ten_dich_vu__icontains=search_query)

        return Response({'total': queryset.count()})
    
class MonAnViewSet(viewsets.ModelViewSet):
    queryset = MonAn.objects.all().order_by('ten_mon_an')
    serializer_class = MonAnSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search_query = request.query_params.get('search', '').strip().lower()

        if search_query:
            search_query_no_diacritics = bo_dau(search_query).lower()
            # Lọc theo từng ký tự đầu, không dấu, không phân biệt hoa thường
            queryset = [
                m for m in queryset
                if bo_dau(m.ten_mon_an).lower().startswith(search_query_no_diacritics)
            ]

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
        search_query = request.query_params.get('search', '').strip().lower()
        queryset = self.get_queryset()
        if search_query:
            queryset = queryset.filter(ten_mon_an__icontains=search_query)
        return Response({'total': queryset.count()})