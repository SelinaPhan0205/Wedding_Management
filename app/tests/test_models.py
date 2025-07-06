from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date, timedelta
from app.models import *


class TaiKhoanModelTest(TestCase):
    """Test cases cho model TaiKhoan"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho TaiKhoan"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User',
            vaitro='admin',
            trangthai='Active'
        )

    def test_tai_khoan_creation(self):
        """Test tạo mới TaiKhoan"""
        self.assertEqual(self.tai_khoan.user.username, 'testuser')
        self.assertEqual(self.tai_khoan.sodienthoai, '0123456789')
        self.assertEqual(self.tai_khoan.hovaten, 'Test User')
        self.assertEqual(self.tai_khoan.vaitro, 'admin')
        self.assertEqual(self.tai_khoan.trangthai, 'Active')

    def test_tai_khoan_str_method(self):
        """Test phương thức __str__ của TaiKhoan"""
        self.assertEqual(str(self.tai_khoan), 'testuser')

    def test_tai_khoan_delete_cascade_user(self):
        """Test xóa TaiKhoan sẽ xóa luôn User liên kết"""
        user_id = self.user.id
        self.tai_khoan.delete()
        # Kiểm tra User đã bị xóa
        self.assertFalse(User.objects.filter(id=user_id).exists())

    def test_tai_khoan_choices(self):
        """Test các choices của TaiKhoan"""
        # Test vai trò
        self.assertIn(('admin', 'Admin'), TaiKhoan._meta.get_field('vaitro').choices)
        self.assertIn(('user', 'User'), TaiKhoan._meta.get_field('vaitro').choices)
        
        # Test trạng thái
        self.assertIn(('Active', 'Hoạt động'), TaiKhoan._meta.get_field('trangthai').choices)
        self.assertIn(('Block', 'Bị khoá'), TaiKhoan._meta.get_field('trangthai').choices)


class LoaiSanhModelTest(TestCase):
    """Test cases cho model LoaiSanh"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho LoaiSanh"""
        self.loai_sanh = LoaiSanh.objects.create(
            ten_loai_sanh='Sảnh VIP',
            gia_ban_toi_thieu=5000000.0
        )

    def test_loai_sanh_creation(self):
        """Test tạo mới LoaiSanh"""
        self.assertEqual(self.loai_sanh.ten_loai_sanh, 'Sảnh VIP')
        self.assertEqual(self.loai_sanh.gia_ban_toi_thieu, 5000000.0)

    def test_loai_sanh_str_method(self):
        """Test phương thức __str__ của LoaiSanh"""
        self.assertEqual(str(self.loai_sanh), 'Sảnh VIP')


class SanhModelTest(TestCase):
    """Test cases cho model Sanh"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho Sanh"""
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

    def test_sanh_creation(self):
        """Test tạo mới Sanh"""
        self.assertEqual(self.sanh.ten_sanh, 'Sảnh Hoa Hồng')
        self.assertEqual(self.sanh.so_luong_ban_toi_da, 50)
        self.assertEqual(self.sanh.trang_thai, 'Active')
        self.assertEqual(self.sanh.loai_sanh, self.loai_sanh)

    def test_sanh_str_method(self):
        """Test phương thức __str__ của Sanh"""
        self.assertEqual(str(self.sanh), 'Sảnh Hoa Hồng')

    def test_sanh_choices(self):
        """Test các choices của Sanh"""
        self.assertIn(('Active', 'Đang hoạt động'), Sanh._meta.get_field('trang_thai').choices)
        self.assertIn(('Maintaining', 'Đang bảo trì'), Sanh._meta.get_field('trang_thai').choices)


class MonAnModelTest(TestCase):
    """Test cases cho model MonAn"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho MonAn"""
        self.mon_an = MonAn.objects.create(
            ten_mon_an='Gà nướng',
            don_gia=150000.0,
            ghi_chu='Gà ta nướng lá chanh'
        )

    def test_mon_an_creation(self):
        """Test tạo mới MonAn"""
        self.assertEqual(self.mon_an.ten_mon_an, 'Gà nướng')
        self.assertEqual(self.mon_an.don_gia, 150000.0)
        self.assertEqual(self.mon_an.ghi_chu, 'Gà ta nướng lá chanh')

    def test_mon_an_str_method(self):
        """Test phương thức __str__ của MonAn"""
        self.assertEqual(str(self.mon_an), 'Gà nướng')

    def test_mon_an_blank_ghi_chu(self):
        """Test MonAn với ghi_chu để trống"""
        mon_an_2 = MonAn.objects.create(
            ten_mon_an='Cơm trắng',
            don_gia=20000.0
        )
        self.assertEqual(mon_an_2.ghi_chu, '')


class DichVuModelTest(TestCase):
    """Test cases cho model DichVu"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho DichVu"""
        self.dich_vu = DichVu.objects.create(
            ten_dich_vu='Trang trí sảnh',
            mo_ta='Trang trí hoa và bóng bay',
            don_gia=2000000.0
        )

    def test_dich_vu_creation(self):
        """Test tạo mới DichVu"""
        self.assertEqual(self.dich_vu.ten_dich_vu, 'Trang trí sảnh')
        self.assertEqual(self.dich_vu.mo_ta, 'Trang trí hoa và bóng bay')
        self.assertEqual(self.dich_vu.don_gia, 2000000.0)

    def test_dich_vu_str_method(self):
        """Test phương thức __str__ của DichVu"""
        self.assertEqual(str(self.dich_vu), 'Trang trí sảnh')

    def test_dich_vu_blank_mo_ta(self):
        """Test DichVu với mo_ta để trống"""
        dich_vu_2 = DichVu.objects.create(
            ten_dich_vu='Âm thanh',
            don_gia=500000.0
        )
        self.assertEqual(dich_vu_2.mo_ta, '')


class QuyDinhModelTest(TestCase):
    """Test cases cho model QuyDinh"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho QuyDinh"""
        self.quy_dinh = QuyDinh.objects.create(
            ma_quy_dinh='QD001',
            mo_ta='Quy định về tiền cọc',
            gia_tri='30%',
            dang_ap_dung=True
        )

    def test_quy_dinh_creation(self):
        """Test tạo mới QuyDinh"""
        self.assertEqual(self.quy_dinh.ma_quy_dinh, 'QD001')
        self.assertEqual(self.quy_dinh.mo_ta, 'Quy định về tiền cọc')
        self.assertEqual(self.quy_dinh.gia_tri, '30%')
        self.assertTrue(self.quy_dinh.dang_ap_dung)

    def test_quy_dinh_str_method(self):
        """Test phương thức __str__ của QuyDinh"""
        self.assertEqual(str(self.quy_dinh), 'QD001')

    def test_quy_dinh_default_dang_ap_dung(self):
        """Test QuyDinh với dang_ap_dung mặc định"""
        quy_dinh_2 = QuyDinh.objects.create(
            ma_quy_dinh='QD002',
            mo_ta='Quy định khác',
            gia_tri='50%'
        )
        self.assertTrue(quy_dinh_2.dang_ap_dung)


class TiecCuoiModelTest(TestCase):
    """Test cases cho model TiecCuoi"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho TiecCuoi"""
        # Tạo User và TaiKhoan
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User'
        )
        
        # Tạo LoaiSanh và Sanh
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
        
        # Tạo TiecCuoi
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

    def test_tiec_cuoi_creation(self):
        """Test tạo mới TiecCuoi"""
        self.assertEqual(self.tiec_cuoi.ten_chu_re, 'Nguyễn Văn A')
        self.assertEqual(self.tiec_cuoi.ten_co_dau, 'Trần Thị B')
        self.assertEqual(self.tiec_cuoi.so_luong_ban, 20)
        self.assertEqual(self.tiec_cuoi.so_luong_ban_du_tru, 5)
        self.assertEqual(self.tiec_cuoi.ca, 'Trưa')
        self.assertEqual(self.tiec_cuoi.tong_tien_tiec_cuoi, 10000000.0)
        self.assertEqual(self.tiec_cuoi.tien_dat_coc, 3000000.0)
        self.assertEqual(self.tiec_cuoi.so_dien_thoai, '0987654321')

    def test_tiec_cuoi_str_method(self):
        """Test phương thức __str__ của TiecCuoi"""
        expected_str = f"Nguyễn Văn A & Trần Thị B ({self.tiec_cuoi.ngay_dai_tiec})"
        self.assertEqual(str(self.tiec_cuoi), expected_str)

    def test_tiec_cuoi_choices(self):
        """Test các choices của TiecCuoi"""
        self.assertIn(('Trưa', 'Trưa'), TiecCuoi._meta.get_field('ca').choices)
        self.assertIn(('Tối', 'Tối'), TiecCuoi._meta.get_field('ca').choices)

    def test_tiec_cuoi_tinh_tong_tien_method(self):
        """Test phương thức tinh_tong_tien của TiecCuoi"""
        # Tạo MonAn và ChiTietThucDon
        mon_an = MonAn.objects.create(
            ten_mon_an='Gà nướng',
            don_gia=150000.0
        )
        ChiTietThucDon.objects.create(
            mon_an=mon_an,
            tiec_cuoi=self.tiec_cuoi,
            so_luong=1,
            thanh_tien=150000.0
        )
        
        # Tạo DichVu và ChiTietDichVu
        dich_vu = DichVu.objects.create(
            ten_dich_vu='Trang trí',
            don_gia=2000000.0
        )
        ChiTietDichVu.objects.create(
            dich_vu=dich_vu,
            tiec_cuoi=self.tiec_cuoi,
            so_luong=1,
            thanh_tien=2000000.0
        )
        
        # Test tính tổng tiền
        tong_tien = self.tiec_cuoi.tinh_tong_tien()
        expected_tong = (150000.0 * 20) + 2000000.0  # (tiền món ăn * số bàn) + tiền dịch vụ
        self.assertEqual(tong_tien, expected_tong)

    def test_tiec_cuoi_tinh_tong_tien_with_custom_ban(self):
        """Test tính tổng tiền với số bàn tùy chỉnh"""
        # Tạo MonAn và ChiTietThucDon
        mon_an = MonAn.objects.create(
            ten_mon_an='Gà nướng',
            don_gia=150000.0
        )
        ChiTietThucDon.objects.create(
            mon_an=mon_an,
            tiec_cuoi=self.tiec_cuoi,
            so_luong=1,
            thanh_tien=150000.0
        )
        
        # Test với số bàn tùy chỉnh
        tong_tien = self.tiec_cuoi.tinh_tong_tien(so_luong_ban=25)
        expected_tong = 150000.0 * 25  # tiền món ăn * số bàn tùy chỉnh
        self.assertEqual(tong_tien, expected_tong)


class HoaDonModelTest(TestCase):
    """Test cases cho model HoaDon"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho HoaDon"""
        # Tạo User và TaiKhoan
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User'
        )
        
        # Tạo LoaiSanh và Sanh
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
        
        # Tạo TiecCuoi
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
        
        # Tạo HoaDon
        self.hoa_don = HoaDon.objects.create(
            tiec_cuoi=self.tiec_cuoi,
            ngay_thanh_toan=date.today(),
            so_ngay_tre=0,
            trang_thai='Đã thanh toán',
            tien_phat=Decimal('0.00'),
            so_luong_ban=20
        )

    def test_hoa_don_creation(self):
        """Test tạo mới HoaDon"""
        self.assertEqual(self.hoa_don.tiec_cuoi, self.tiec_cuoi)
        self.assertEqual(self.hoa_don.ngay_thanh_toan, date.today())
        self.assertEqual(self.hoa_don.so_ngay_tre, 0)
        self.assertEqual(self.hoa_don.trang_thai, 'Đã thanh toán')
        self.assertEqual(self.hoa_don.tien_phat, Decimal('0.00'))
        self.assertEqual(self.hoa_don.so_luong_ban, 20)

    def test_hoa_don_str_method(self):
        """Test phương thức __str__ của HoaDon"""
        expected_str = f"HĐ - {self.tiec_cuoi}"
        self.assertEqual(str(self.hoa_don), expected_str)

    def test_hoa_don_choices(self):
        """Test các choices của HoaDon"""
        self.assertIn(('Chưa thanh toán', 'Chưa thanh toán'), 
                     HoaDon._meta.get_field('trang_thai').choices)
        self.assertIn(('Đã thanh toán', 'Đã thanh toán'), 
                     HoaDon._meta.get_field('trang_thai').choices)

    def test_hoa_don_tinh_tong_tien_method(self):
        """Test phương thức tinh_tong_tien của HoaDon"""
        # Tạo MonAn và ChiTietThucDon
        mon_an = MonAn.objects.create(
            ten_mon_an='Gà nướng',
            don_gia=150000.0
        )
        ChiTietThucDon.objects.create(
            mon_an=mon_an,
            tiec_cuoi=self.tiec_cuoi,
            so_luong=1,
            thanh_tien=150000.0
        )
        
        # Test tính tổng tiền
        tong_tien = self.hoa_don.tinh_tong_tien()
        expected_tong = 150000.0 * 20  # tiền món ăn * số bàn trong hóa đơn
        self.assertEqual(tong_tien, expected_tong)


class ChiTietThucDonModelTest(TestCase):
    """Test cases cho model ChiTietThucDon"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho ChiTietThucDon"""
        # Tạo User và TaiKhoan
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User'
        )
        
        # Tạo LoaiSanh và Sanh
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
        
        # Tạo TiecCuoi
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
        
        # Tạo MonAn
        self.mon_an = MonAn.objects.create(
            ten_mon_an='Gà nướng',
            don_gia=150000.0,
            ghi_chu='Gà ta nướng lá chanh'
        )
        
        # Tạo ChiTietThucDon
        self.chi_tiet_thuc_don = ChiTietThucDon.objects.create(
            mon_an=self.mon_an,
            tiec_cuoi=self.tiec_cuoi,
            so_luong=1,
            thanh_tien=150000.0,
            ghi_chu='Ghi chú test'
        )

    def test_chi_tiet_thuc_don_creation(self):
        """Test tạo mới ChiTietThucDon"""
        self.assertEqual(self.chi_tiet_thuc_don.mon_an, self.mon_an)
        self.assertEqual(self.chi_tiet_thuc_don.tiec_cuoi, self.tiec_cuoi)
        self.assertEqual(self.chi_tiet_thuc_don.so_luong, 1)
        self.assertEqual(self.chi_tiet_thuc_don.thanh_tien, 150000.0)
        self.assertEqual(self.chi_tiet_thuc_don.ghi_chu, 'Ghi chú test')

    def test_chi_tiet_thuc_don_str_method(self):
        """Test phương thức __str__ của ChiTietThucDon"""
        expected_str = f"Gà nướng - {self.tiec_cuoi}"
        self.assertEqual(str(self.chi_tiet_thuc_don), expected_str)

    def test_chi_tiet_thuc_don_blank_ghi_chu(self):
        """Test ChiTietThucDon với ghi_chu để trống"""
        chi_tiet_2 = ChiTietThucDon.objects.create(
            mon_an=self.mon_an,
            tiec_cuoi=self.tiec_cuoi,
            so_luong=2,
            thanh_tien=300000.0
        )
        self.assertEqual(chi_tiet_2.ghi_chu, '')


class ChiTietDichVuModelTest(TestCase):
    """Test cases cho model ChiTietDichVu"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho ChiTietDichVu"""
        # Tạo User và TaiKhoan
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Test User'
        )
        
        # Tạo LoaiSanh và Sanh
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
        
        # Tạo TiecCuoi
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
        
        # Tạo DichVu
        self.dich_vu = DichVu.objects.create(
            ten_dich_vu='Trang trí sảnh',
            mo_ta='Trang trí hoa và bóng bay',
            don_gia=2000000.0
        )
        
        # Tạo ChiTietDichVu
        self.chi_tiet_dich_vu = ChiTietDichVu.objects.create(
            dich_vu=self.dich_vu,
            tiec_cuoi=self.tiec_cuoi,
            so_luong=1,
            thanh_tien=2000000.0
        )

    def test_chi_tiet_dich_vu_creation(self):
        """Test tạo mới ChiTietDichVu"""
        self.assertEqual(self.chi_tiet_dich_vu.dich_vu, self.dich_vu)
        self.assertEqual(self.chi_tiet_dich_vu.tiec_cuoi, self.tiec_cuoi)
        self.assertEqual(self.chi_tiet_dich_vu.so_luong, 1)
        self.assertEqual(self.chi_tiet_dich_vu.thanh_tien, 2000000.0)

    def test_chi_tiet_dich_vu_str_method(self):
        """Test phương thức __str__ của ChiTietDichVu"""
        expected_str = f"Trang trí sảnh - {self.tiec_cuoi}"
        self.assertEqual(str(self.chi_tiet_dich_vu), expected_str) 