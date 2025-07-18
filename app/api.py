from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json

# API Đăng nhập: chỉ cho phép user có trong TaiKhoan đăng nhập
@api_view(['POST'])
def dangnhap_api(request):
    try:
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')
    except Exception:
        return Response({'success': False, 'message': 'Dữ liệu không hợp lệ!'}, status=400)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        # Kiểm tra user có trong TaiKhoan không
        from .models import TaiKhoan
        try:
            TaiKhoan.objects.get(user=user)
        except TaiKhoan.DoesNotExist:
            return Response({'success': False, 'message': 'Tài khoản không tồn tại trong hệ thống!'}, status=403)
        if not user.is_active:
            return Response({'success': False, 'message': 'Tài khoản đã bị khóa!'}, status=403)
        auth_login(request, user)
        return Response({'success': True})
    else:
        return Response({'success': False, 'message': 'Tên đăng nhập hoặc mật khẩu không đúng!'}, status=401)

from rest_framework.routers import DefaultRouter
from .views import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import TaiKhoan

# API lấy thông tin tài khoản hiện tại
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def thong_tin_tai_khoan(request):
    user = request.user
    try:
        tk = TaiKhoan.objects.get(user=user)
        data = {
            'ho_ten': tk.hovaten,
            'so_dien_thoai': tk.sodienthoai,
            'ten_tai_khoan': user.username,
            'email': user.email,
            'vai_tro': 'Quản trị viên' if tk.vaitro == 'admin' or user.is_staff else 'Nhân viên',
            'trang_thai': 'Hoạt động' if tk.trangthai == 'Active' and user.is_active else 'Bị khóa',
        }
    except TaiKhoan.DoesNotExist:
        data = {
            'ho_ten': user.get_full_name() or user.username,
            'so_dien_thoai': '',
            'ten_tai_khoan': user.username,
            'email': user.email,
            'vai_tro': 'Quản trị viên' if user.is_staff else 'Nhân viên',
            'trang_thai': 'Hoạt động' if user.is_active else 'Bị khóa',
        }
    return Response(data)

router = DefaultRouter()
router.register(r'loaisanh', LoaiSanhViewSet, basename='loaisanh')
router.register(r'sanh', SanhViewSet, basename='sanh')
router.register(r'taikhoan', TaiKhoanViewSet, basename='taikhoan')
router.register(r'dichvu', DichVuViewSet, basename='dichvu')
router.register(r'monan', MonAnViewSet, basename='monan')
router.register(r'quydinh', QuyDinhViewSet, basename='quydinh')
router.register(r'tieccuoi', TiecCuoiViewSet, basename='tieccuoi')
router.register(r'hoadon', HoaDonViewSet, basename='hoadon')
router.register(r'report', ReportViewSet, basename='report')

urlpatterns = router.urls