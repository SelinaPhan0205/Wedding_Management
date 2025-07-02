from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F
from .models import HoaDon, TiecCuoi
import datetime

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
