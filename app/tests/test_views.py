from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from datetime import date, timedelta
from app.models import *

class DangNhapViewTest(TestCase):
    """Test cases cho view đăng nhập"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho view đăng nhập"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User',
            vaitro='admin',
            trangthai='Active'
        )

    def test_dangnhap_get(self):
        """Test GET request đến trang đăng nhập"""
        response = self.client.get(reverse('dangnhap'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/dangnhap.html')

    def test_dangnhap_post_success(self):
        """Test POST request đăng nhập thành công"""
        response = self.client.post(reverse('dangnhap'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('trangchu'))

    def test_dangnhap_post_fail_wrong_credentials(self):
        """Test POST request đăng nhập thất bại do sai thông tin"""
        response = self.client.post(reverse('dangnhap'), {
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/dangnhap.html')
        self.assertIn('error_message', response.context)
        self.assertIn('Tên đăng nhập hoặc mật khẩu không đúng', response.context['error_message'])

    def test_dangnhap_post_fail_user_not_in_taikhoan(self):
        """Test POST request đăng nhập thất bại do user không có trong TaiKhoan"""
        # Tạo user mới không có trong TaiKhoan
        user2 = User.objects.create_user(
            username='user2',
            password='pass123',
            email='user2@example.com'
        )
        
        response = self.client.post(reverse('dangnhap'), {
            'username': 'user2',
            'password': 'pass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/dangnhap.html')
        self.assertIn('error_message', response.context)
        self.assertIn('Tài khoản không tồn tại trong hệ thống', response.context['error_message'])

    def test_dangnhap_post_fail_blocked_user(self):
        """Test POST request đăng nhập thất bại do user bị khóa"""
        # Khóa user
        self.user.is_active = False
        self.user.save()
        
        response = self.client.post(reverse('dangnhap'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/dangnhap.html')
        self.assertIn('error_message', response.context)
        self.assertIn('Tài khoản đã bị khóa', response.context['error_message'])


class DangXuatViewTest(TestCase):
    """Test cases cho view đăng xuất"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho view đăng xuất"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User'
        )

    def test_dangxuat(self):
        """Test đăng xuất"""
        # Đăng nhập trước
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('dangxuat'))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('dangnhap'))
        
        # Kiểm tra cache control headers
        self.assertIn('Cache-Control', response)
        self.assertIn('no-cache, no-store, must-revalidate', response['Cache-Control'])
        self.assertIn('Pragma', response)
        self.assertIn('no-cache', response['Pragma'])
        self.assertIn('Expires', response)
        self.assertIn('0', response['Expires'])


class TrangChuViewTest(TestCase):
    """Test cases cho view trang chủ"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho view trang chủ"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User'
        )

    def test_trangchu_authenticated(self):
        """Test truy cập trang chủ khi đã đăng nhập"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('trangchu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/trangchu.html')

    def test_trangchu_unauthenticated(self):
        """Test truy cập trang chủ khi chưa đăng nhập"""
        response = self.client.get(reverse('trangchu'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, f"{reverse('dangnhap')}?next={reverse('trangchu')}")


class QuanLyTaiKhoanViewTest(TestCase):
    """Test cases cho view quản lý tài khoản"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho view quản lý tài khoản"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User'
        )

    def test_quanlytaikhoan_authenticated(self):
        """Test truy cập trang quản lý tài khoản khi đã đăng nhập"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('quanlytaikhoan'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/quanlytaikhoan.html')

    def test_quanlytaikhoan_unauthenticated(self):
        """Test truy cập trang quản lý tài khoản khi chưa đăng nhập"""
        response = self.client.get(reverse('quanlytaikhoan'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class QuanLySanhViewTest(TestCase):
    """Test cases cho view quản lý sảnh"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho view quản lý sảnh"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User'
        )

    def test_quanlysanh_authenticated(self):
        """Test truy cập trang quản lý sảnh khi đã đăng nhập"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('quanlysanh'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/quanlysanh.html')

    def test_quanlysanh_unauthenticated(self):
        """Test truy cập trang quản lý sảnh khi chưa đăng nhập"""
        response = self.client.get(reverse('quanlysanh'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class QuanLyTiecCuoiViewTest(TestCase):
    """Test cases cho view quản lý tiệc cưới"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho view quản lý tiệc cưới"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User'
        )

    def test_quanlytieccuoi_authenticated(self):
        """Test truy cập trang quản lý tiệc cưới khi đã đăng nhập"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('quanlytieccuoi'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/quanlytieccuoi.html')

    def test_quanlytieccuoi_unauthenticated(self):
        """Test truy cập trang quản lý tiệc cưới khi chưa đăng nhập"""
        response = self.client.get(reverse('quanlytieccuoi'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class QuanLyHoaDonViewTest(TestCase):
    """Test cases cho view quản lý hóa đơn"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho view quản lý hóa đơn"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User'
        )

    def test_quanlyhoadon_authenticated(self):
        """Test truy cập trang quản lý hóa đơn khi đã đăng nhập"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('quanlyhoadon'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/quanlyhoadon.html')

    def test_quanlyhoadon_unauthenticated(self):
        """Test truy cập trang quản lý hóa đơn khi chưa đăng nhập"""
        response = self.client.get(reverse('quanlyhoadon'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class QuanLyThucDonViewTest(TestCase):
    """Test cases cho view quản lý thực đơn"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho view quản lý thực đơn"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User'
        )

    def test_quanlythucdon_authenticated(self):
        """Test truy cập trang quản lý thực đơn khi đã đăng nhập"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('quanlythucdon'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/quanlythucdon.html')

    def test_quanlythucdon_unauthenticated(self):
        """Test truy cập trang quản lý thực đơn khi chưa đăng nhập"""
        response = self.client.get(reverse('quanlythucdon'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class QuanLyDichVuViewTest(TestCase):
    """Test cases cho view quản lý dịch vụ"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho view quản lý dịch vụ"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User'
        )

    def test_quanlydichvu_authenticated(self):
        """Test truy cập trang quản lý dịch vụ khi đã đăng nhập"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('quanlydichvu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/quanlydichvu.html')

    def test_quanlydichvu_unauthenticated(self):
        """Test truy cập trang quản lý dịch vụ khi chưa đăng nhập"""
        response = self.client.get(reverse('quanlydichvu'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class QuanLyQuyDinhViewTest(TestCase):
    """Test cases cho view quản lý quy định"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho view quản lý quy định"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User'
        )

    def test_quanlyquydinh_authenticated(self):
        """Test truy cập trang quản lý quy định khi đã đăng nhập"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('quanlyquydinh'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/quanlyquydinh.html')

    def test_quanlyquydinh_unauthenticated(self):
        """Test truy cập trang quản lý quy định khi chưa đăng nhập"""
        response = self.client.get(reverse('quanlyquydinh'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class XemBaoCaoViewTest(TestCase):
    """Test cases cho view xem báo cáo"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho view xem báo cáo"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User'
        )

    def test_xembaocao_authenticated(self):
        """Test truy cập trang xem báo cáo khi đã đăng nhập"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('xembaocao'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/xembaocao.html')

    def test_xembaocao_unauthenticated(self):
        """Test truy cập trang xem báo cáo khi chưa đăng nhập"""
        response = self.client.get(reverse('xembaocao'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class BaoCaoDoanhThuViewTest(TestCase):
    """Test cases cho view báo cáo doanh thu"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho view báo cáo doanh thu"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User'
        )

    def test_baocaodoanhthu_authenticated(self):
        """Test truy cập trang báo cáo doanh thu khi đã đăng nhập"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('baocaodoanhthu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/baocaodoanhthu.html')

    def test_baocaodoanhthu_unauthenticated(self):
        """Test truy cập trang báo cáo doanh thu khi chưa đăng nhập"""
        response = self.client.get(reverse('baocaodoanhthu'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class BaoCaoCongNoViewTest(TestCase):
    """Test cases cho view báo cáo công nợ"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho view báo cáo công nợ"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User'
        )

    def test_baocaocongno_authenticated(self):
        """Test truy cập trang báo cáo công nợ khi đã đăng nhập"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('baocaocongno'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/baocaocongno.html')

    def test_baocaocongno_unauthenticated(self):
        """Test truy cập trang báo cáo công nợ khi chưa đăng nhập"""
        response = self.client.get(reverse('baocaocongno'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class BaoCaoThucThuViewTest(TestCase):
    """Test cases cho view báo cáo thực thu"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho view báo cáo thực thu"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User'
        )

    def test_baocaothucthu_authenticated(self):
        """Test truy cập trang báo cáo thực thu khi đã đăng nhập"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('baocaothucthu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/baocaothucthu.html')

    def test_baocaothucthu_unauthenticated(self):
        """Test truy cập trang báo cáo thực thu khi chưa đăng nhập"""
        response = self.client.get(reverse('baocaothucthu'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class ViewSetTest(TestCase):
    """Test cases cho các ViewSet"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho ViewSet"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User'
        )
        
        # Tạo dữ liệu test
        self.loai_sanh = LoaiSanh.objects.create(
            ten_loai_sanh='Sảnh VIP',
            gia_ban_toi_thieu=5000000.0
        )
        self.sanh = Sanh.objects.create(
            loai_sanh=self.loai_sanh,
            ten_sanh='Sảnh Hoa Hồng',
            so_luong_ban_toi_da=50,
            trang_thai='Active'
        )
        
        self.tiec_cuoi = TiecCuoi.objects.create(
            tai_khoan=self.tai_khoan,
            sanh=self.sanh,
            ten_chu_re='Nguyễn Văn A',
            ten_co_dau='Trần Thị B',
            ngay_dai_tiec=date.today() + timedelta(days=30),
            so_luong_ban=20,
            so_luong_ban_du_tru=5,
            ca='Trưa',
            tong_tien_tiec_cuoi=10000000.0,
            tien_dat_coc=3000000.0,
            so_dien_thoai='0987654321'
        )

    def test_sanh_viewset_count(self):
        """Test ViewSet Sanh action count"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/sanh/count/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total'], 1)

    def test_sanh_viewset_tracuu(self):
        """Test ViewSet Sanh action tra cứu sảnh trống"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(f'/api/sanh/tracuu/?ngay={(date.today() + timedelta(days=30)).isoformat()}&ca=Trưa')
        self.assertEqual(response.status_code, 200)
        # Sảnh đã bị chiếm bởi tiệc cưới
        self.assertEqual(len(response.data['data']), 0)

    def test_tai_khoan_viewset_count(self):
        """Test ViewSet TaiKhoan action count"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/taikhoan/count/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total'], 1)

    def test_dich_vu_viewset_count(self):
        """Test ViewSet DichVu action count"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/dichvu/count/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total'], 0)  # Chưa có dịch vụ nào

    def test_mon_an_viewset_count(self):
        """Test ViewSet MonAn action count"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/monan/count/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total'], 0)  # Chưa có món ăn nào

    def test_quy_dinh_viewset_count(self):
        """Test ViewSet QuyDinh action count"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/quydinh/count/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total'], 0)  # Chưa có quy định nào

    def test_tiec_cuoi_viewset_count(self):
        """Test ViewSet TiecCuoi action count"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/tieccuoi/count/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total'], 1)

    def test_hoa_don_viewset_count(self):
        """Test ViewSet HoaDon action count"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/hoadon/count/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total'], 0)  # Chưa có hóa đơn nào


class ReportViewSetTest(TestCase):
    """Test cases cho ReportViewSet"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho ReportViewSet"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User'
        )
        
        # Tạo dữ liệu test cho báo cáo
        self.loai_sanh = LoaiSanh.objects.create(
            ten_loai_sanh='Sảnh VIP',
            gia_ban_toi_thieu=5000000.0
        )
        self.sanh = Sanh.objects.create(
            loai_sanh=self.loai_sanh,
            ten_sanh='Sảnh Hoa Hồng',
            so_luong_ban_toi_da=50,
            trang_thai='Active'
        )
        
        self.tiec_cuoi = TiecCuoi.objects.create(
            tai_khoan=self.tai_khoan,
            sanh=self.sanh,
            ten_chu_re='Nguyễn Văn A',
            ten_co_dau='Trần Thị B',
            ngay_dai_tiec=date.today() + timedelta(days=30),
            so_luong_ban=20,
            so_luong_ban_du_tru=5,
            ca='Trưa',
            tong_tien_tiec_cuoi=10000000.0,
            tien_dat_coc=3000000.0,
            so_dien_thoai='0987654321'
        )

    def test_report_total_tiec_cuoi(self):
        """Test ReportViewSet action total_tiec_cuoi"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/report/total-tiec-cuoi/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total'], 1)

    def test_report_overview(self):
        """Test ReportViewSet action overview"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/report/overview/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_tiec_cuoi', response.data)
        self.assertIn('total_doanh_thu', response.data)
        self.assertIn('total_cong_no', response.data)

    def test_report_top_mon_an(self):
        """Test ReportViewSet action top_mon_an"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/report/top-mon-an/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_report_top_dich_vu(self):
        """Test ReportViewSet action top_dich_vu"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/report/top-dich-vu/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_report_sanh_usage(self):
        """Test ReportViewSet action sanh_usage"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/report/sanh-usage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_report_revenue(self):
        """Test ReportViewSet action revenue_report"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/report/revenue/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_report_debt(self):
        """Test ReportViewSet action debt_report"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/report/debt/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_report_actual_receipt(self):
        """Test ReportViewSet action actual_receipt_report"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/report/actual-receipt/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)


class CapNhatTaiKhoanViewTest(TestCase):
    """Test cases cho view cập nhật tài khoản"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho view cập nhật tài khoản"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User',
            vaitro='admin',
            trangthai='Active'
        )

    def test_cap_nhat_tai_khoan_success(self):
        """Test cập nhật tài khoản thành công"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'hovaten': 'Updated User',
            'sodienthoai': '0987654321',
            'email': 'updated@example.com'
        }
        response = self.client.patch('/api/cap-nhat-tai-khoan/', data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['hovaten'], 'Updated User')
        self.assertEqual(response.data['sodienthoai'], '0987654321')
        self.assertEqual(response.data['email'], 'updated@example.com')

    def test_cap_nhat_tai_khoan_unauthenticated(self):
        """Test cập nhật tài khoản khi chưa đăng nhập"""
        data = {
            'hovaten': 'Updated User',
            'sodienthoai': '0987654321'
        }
        response = self.client.patch('/api/cap-nhat-tai-khoan/', data, content_type='application/json')
        self.assertEqual(response.status_code, 401)  # Unauthorized

    def test_cap_nhat_tai_khoan_invalid_data(self):
        """Test cập nhật tài khoản với dữ liệu không hợp lệ"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'sodienthoai': 'invalid_phone'  # Số điện thoại không hợp lệ
        }
        response = self.client.patch('/api/cap-nhat-tai-khoan/', data, content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Bad Request 