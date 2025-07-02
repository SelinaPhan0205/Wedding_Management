# Đăng nhập view
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
from django.db.models import Sum, F
import datetime


##### Code các yêu cầu #####

def dangnhap(request):
    return render(request, 'app/dangnhap.html')
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
def baocaodoanhthu(request):
    return render(request, 'app/baocaodoanhthu.html')
def baocaocongno(request):
    return render(request, 'app/baocaocongno.html')
def baocaothucthu(request):
    return render(request, 'app/baocaothucthu.html')

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
    
    @action(detail=False, methods=['get'], url_path='tracuu')
    def tra_cuu_sanh_trong(self, request):
        """
        API tra cứu sảnh trống theo ngày và ca.
        GET /api/sanh/tracuu/?ngay=yyyy-mm-dd&ca=Trưa|Tối
        """
        ngay = request.query_params.get('ngay')
        ca = request.query_params.get('ca')
        if not ngay or not ca:
            return Response({'error': 'Thiếu tham số ngày hoặc ca.'}, status=400)

        tat_ca_sanh = Sanh.objects.filter(trang_thai='Active')
        sanh_ban_ids = TiecCuoi.objects.filter(ngay_dai_tiec=ngay, ca=ca).values_list('sanh_id', flat=True)
        sanh_trong = tat_ca_sanh.exclude(id__in=sanh_ban_ids)
        serializer = SanhSerializer(sanh_trong, many=True)
        return Response({'data': serializer.data})

class TaiKhoanViewSet(viewsets.ModelViewSet):
    queryset = TaiKhoan.objects.all().select_related('user')
    serializer_class = TaiKhoanSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search_query = request.query_params.get('search', '').strip().lower()

        if search_query:
            search_query_no_diacritics = bo_dau(search_query).lower()
            queryset = [
                tk for tk in queryset
                if search_query_no_diacritics in bo_dau(tk.hovaten or '').lower()
                or search_query_no_diacritics in bo_dau(tk.sodienthoai or '').lower()
                or search_query_no_diacritics in bo_dau(tk.user.username or '').lower()
                or search_query_no_diacritics in bo_dau(tk.user.email or '').lower()
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
    
class QuyDinhViewSet(viewsets.ModelViewSet):
    queryset = QuyDinh.objects.all().order_by('id')
    serializer_class = QuyDinhSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('ma_quy_dinh')
        search_query = request.query_params.get('search', '').strip().lower()

        if search_query:
            search_query_no_diacritics = bo_dau(search_query).lower()
            queryset = [
                qd for qd in queryset
                if bo_dau(qd.ma_quy_dinh).lower().startswith(search_query_no_diacritics)
                or bo_dau(qd.mo_ta or '').lower().startswith(search_query_no_diacritics)
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
            search_query_no_diacritics = bo_dau(search_query).lower()
            queryset = [
                qd for qd in queryset
                if bo_dau(qd.ma_quy_dinh).lower().startswith(search_query_no_diacritics)
                or bo_dau(qd.mo_ta or '').lower().startswith(search_query_no_diacritics)
            ]
        return Response({'total': queryset.count()})
    
class TiecCuoiViewSet(viewsets.ModelViewSet):
    queryset = TiecCuoi.objects.all().select_related('sanh', 'tai_khoan')
    serializer_class = TiecCuoiSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('-ngay_dai_tiec')
        search_query = request.query_params.get('search', '').strip().lower()
        if search_query:
            search_query_no_diacritics = bo_dau(search_query).lower()
            queryset = [
                t for t in queryset
                if search_query_no_diacritics in bo_dau(t.ten_chu_re or '').lower()
                or search_query_no_diacritics in bo_dau(t.ten_co_dau or '').lower()
                or search_query_no_diacritics in bo_dau(t.so_dien_thoai or '').lower()
                or search_query_no_diacritics in bo_dau(t.sanh.ten_sanh if t.sanh else '').lower()
            ]
        # Phân trang
        page = int(request.query_params.get('page', 1))
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
        queryset = self.get_queryset()
        return Response({'total': queryset.count()})
    
class HoaDonViewSet(viewsets.ModelViewSet):
    queryset = HoaDon.objects.all().select_related('tiec_cuoi')
    serializer_class = HoaDonSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('-ngay_thanh_toan')
        search_query = request.query_params.get('search', '').strip().lower()
        if search_query:
            queryset = queryset.filter(
                tiec_cuoi__ten_chu_re__icontains=search_query
            ) | queryset.filter(
                tiec_cuoi__ten_co_dau__icontains=search_query
            ) | queryset.filter(
                tiec_cuoi__id__icontains=search_query
            ) | queryset.filter(
                id__icontains=search_query
            )
        # Phân trang
        page = int(request.query_params.get('page', 1))
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
        queryset = self.get_queryset()
        return Response({'total': queryset.count()})
class ReportViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'], url_path='total-tiec-cuoi')
    def total_tiec_cuoi(self, request):
        """API trả về tổng số tiệc cưới theo tháng/năm (?month=7&year=2025)"""
        month = int(request.query_params.get('month', datetime.date.today().month))
        year = int(request.query_params.get('year', datetime.date.today().year))
        total = TiecCuoi.objects.filter(ngay_dai_tiec__month=month, ngay_dai_tiec__year=year).count()
        return Response({
            'month': month,
            'year': year,
            'total_tiec_cuoi': total
        })

    @action(detail=False, methods=['get'], url_path='overview')
    def overview(self, request):
        """API tổng quan: tổng số tiệc cưới, doanh thu dự kiến, công nợ, thực thu theo tháng/năm"""
        month = int(request.query_params.get('month', datetime.date.today().month))
        year = int(request.query_params.get('year', datetime.date.today().year))
        # Tổng số tiệc cưới trong tháng/năm
        total_tiec = TiecCuoi.objects.filter(ngay_dai_tiec__month=month, ngay_dai_tiec__year=year).count()
        # Doanh thu dự kiến: tổng tong_tien_tiec_cuoi của các tiệc cưới trong tháng/năm
        doanh_thu_du_kien = TiecCuoi.objects.filter(ngay_dai_tiec__month=month, ngay_dai_tiec__year=year).aggregate(total=Sum('tong_tien_tiec_cuoi'))['total'] or 0
        # Công nợ: tổng các hóa đơn chưa thanh toán trong tháng/năm
        cong_no = HoaDon.objects.filter(trang_thai='Chưa Thanh Toán', tiec_cuoi__ngay_dai_tiec__month=month, tiec_cuoi__ngay_dai_tiec__year=year)
        tong_cong_no = cong_no.aggregate(total=Sum(F('tiec_cuoi__tong_tien_tiec_cuoi')-F('tiec_cuoi__tien_dat_coc')))['total'] or 0
        # Thực thu: tổng các hóa đơn đã thanh toán trong tháng/năm
        thuc_thu = HoaDon.objects.filter(trang_thai='Đã thanh toán', tiec_cuoi__ngay_dai_tiec__month=month, tiec_cuoi__ngay_dai_tiec__year=year).aggregate(total=Sum('tiec_cuoi__tong_tien_tiec_cuoi'))['total'] or 0
        return Response({
            'month': month,
            'year': year,
            'total_tiec': total_tiec,
            'doanh_thu_du_kien': doanh_thu_du_kien,
            'cong_no': tong_cong_no,
            'thuc_thu': thuc_thu,
        })

    @action(detail=False, methods=['get'], url_path='top-mon-an')
    def top_mon_an(self, request):
        """Top món ăn được đặt nhiều nhất theo tháng/năm"""
        month = int(request.query_params.get('month', datetime.date.today().month))
        year = int(request.query_params.get('year', datetime.date.today().year))
        from .models import ChiTietThucDon, MonAn, TiecCuoi
        # Lấy các tiệc cưới trong tháng/năm
        tiec_ids = TiecCuoi.objects.filter(ngay_dai_tiec__month=month, ngay_dai_tiec__year=year).values_list('id', flat=True)
        # Thống kê số lượng từng món ăn
        qs = ChiTietThucDon.objects.filter(tiec_cuoi_id__in=tiec_ids)
        result = (
            qs.values('mon_an__ten_mon_an')
            .annotate(total=Sum('so_luong'))
            .order_by('-total')[:10]
        )
        return Response({'month': month, 'year': year, 'top_mon_an': list(result)})

    @action(detail=False, methods=['get'], url_path='top-dich-vu')
    def top_dich_vu(self, request):
        """Top dịch vụ được đặt nhiều nhất theo tháng/năm"""
        month = int(request.query_params.get('month', datetime.date.today().month))
        year = int(request.query_params.get('year', datetime.date.today().year))
        from .models import ChiTietDichVu, DichVu, TiecCuoi
        tiec_ids = TiecCuoi.objects.filter(ngay_dai_tiec__month=month, ngay_dai_tiec__year=year).values_list('id', flat=True)
        qs = ChiTietDichVu.objects.filter(tiec_cuoi_id__in=tiec_ids)
        result = (
            qs.values('dich_vu__ten_dich_vu')
            .annotate(total=Sum('so_luong'))
            .order_by('-total')[:10]
        )
        return Response({'month': month, 'year': year, 'top_dich_vu': list(result)})

    @action(detail=False, methods=['get'], url_path='sanh-usage')
    def sanh_usage(self, request):
        """Thống kê số lần sử dụng từng sảnh theo tháng/năm"""
        month = int(request.query_params.get('month', datetime.date.today().month))
        year = int(request.query_params.get('year', datetime.date.today().year))
        from .models import Sanh, TiecCuoi
        qs = TiecCuoi.objects.filter(ngay_dai_tiec__month=month, ngay_dai_tiec__year=year)
        # annotate count for each hall
        from django.db.models import Count
        result = (
            qs.values('sanh__ten_sanh')
            .annotate(total=Count('id'))
            .order_by('-total')
        )
        return Response({'month': month, 'year': year, 'sanh_usage': list(result)})
    """
    API cho các loại báo cáo: doanh thu, công nợ, thực thu
    """
    @action(detail=False, methods=['get'], url_path='revenue')
    def revenue_report(self, request):
        """Báo cáo doanh thu theo tháng/năm (truyền ?month=7&year=2025)"""
        month = int(request.query_params.get('month', datetime.date.today().month))
        year = int(request.query_params.get('year', datetime.date.today().year))
        hoadons = HoaDon.objects.filter(ngay_thanh_toan__month=month, ngay_thanh_toan__year=year)
        total = hoadons.aggregate(total=Sum('tiec_cuoi__tong_tien_tiec_cuoi'))['total'] or 0
        return Response({
            'month': month,
            'year': year,
            'total_revenue': total,
            'count': hoadons.count(),
        })

    @action(detail=False, methods=['get'], url_path='debt')
    def debt_report(self, request):
        """Báo cáo công nợ: tổng các hóa đơn chưa thanh toán"""
        hoadons = HoaDon.objects.filter(trang_thai='Chưa Thanh Toán')
        total_debt = hoadons.aggregate(total=Sum(F('tiec_cuoi__tong_tien_tiec_cuoi')-F('tiec_cuoi__tien_dat_coc')))['total'] or 0
        return Response({
            'total_debt': total_debt,
            'count': hoadons.count(),
        })

    @action(detail=False, methods=['get'], url_path='actual-receipt')
    def actual_receipt_report(self, request):
        """Báo cáo thực thu: tổng tiền đã thu (đã thanh toán) theo tháng/năm"""
        month = int(request.query_params.get('month', datetime.date.today().month))
        year = int(request.query_params.get('year', datetime.date.today().year))
        hoadons = HoaDon.objects.filter(trang_thai='Đã thanh toán', ngay_thanh_toan__month=month, ngay_thanh_toan__year=year)
        total = hoadons.aggregate(total=Sum('tiec_cuoi__tong_tien_tiec_cuoi'))['total'] or 0
        return Response({
            'month': month,
            'year': year,
            'total_actual_receipt': total,
            'count': hoadons.count(),
        })
