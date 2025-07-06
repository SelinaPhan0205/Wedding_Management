from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date, timedelta
from app.models import *
from app.serializers import *

class UserSerializerTest(TestCase):
    """Test cases cho UserSerializer"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho UserSerializer"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        self.serializer = UserSerializer(instance=self.user)

    def test_user_serializer_fields(self):
        """Test các trường của UserSerializer"""
        data = self.serializer.data
        self.assertEqual(data['id'], self.user.id)
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['first_name'], 'Test')
        self.assertEqual(data['last_name'], 'User')

    def test_user_serializer_validation(self):
        """Test validation của UserSerializer"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class TaiKhoanSerializerTest(TestCase):
    """Test cases cho TaiKhoanSerializer"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho TaiKhoanSerializer"""
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
        self.serializer = TaiKhoanSerializer(instance=self.tai_khoan)

    def test_tai_khoan_serializer_fields(self):
        """Test các trường của TaiKhoanSerializer"""
        data = self.serializer.data
        self.assertEqual(data['id'], self.tai_khoan.id)
        self.assertEqual(data['hovaten'], 'Test User')
        self.assertEqual(data['sodienthoai'], '0123456789')
        self.assertEqual(data['vaitro'], 'admin')
        self.assertEqual(data['trangthai'], 'Active')
        self.assertEqual(data['user']['username'], 'testuser')
        self.assertEqual(data['email_display'], 'test@example.com')

    def test_tai_khoan_serializer_create_success(self):
        """Test tạo mới TaiKhoan thành công"""
        data = {
            'username': 'newuser',
            'password': 'newpass123',
            'email': 'new@example.com',
            'hovaten': 'New User',
            'sodienthoai': '0987654321',
            'vaitro': 'user',
            'trangthai': 'Active'
        }
        serializer = TaiKhoanSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        tai_khoan = serializer.save()
        self.assertEqual(tai_khoan.hovaten, 'New User')
        self.assertEqual(tai_khoan.user.username, 'newuser')
        self.assertTrue(tai_khoan.user.check_password('newpass123'))

    def test_tai_khoan_serializer_create_missing_username_password(self):
        """Test tạo mới TaiKhoan thiếu username/password"""
        data = {
            'hovaten': 'New User',
            'sodienthoai': '0987654321',
            'vaitro': 'user',
            'trangthai': 'Active'
        }
        serializer = TaiKhoanSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_tai_khoan_serializer_create_existing_user(self):
        """Test tạo TaiKhoan cho user đã tồn tại"""
        # Tạo user trước
        existing_user = User.objects.create_user(
            username='existinguser',
            password='oldpass123',
            email='existing@example.com'
        )
        
        data = {
            'username': 'existinguser',
            'password': 'newpass123',
            'email': 'newemail@example.com',
            'hovaten': 'Existing User',
            'sodienthoai': '0987654321',
            'vaitro': 'user',
            'trangthai': 'Active'
        }
        serializer = TaiKhoanSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        tai_khoan = serializer.save()
        self.assertEqual(tai_khoan.user, existing_user)
        self.assertTrue(tai_khoan.user.check_password('newpass123'))
        self.assertEqual(tai_khoan.user.email, 'newemail@example.com')

    def test_tai_khoan_serializer_update(self):
        """Test cập nhật TaiKhoan"""
        data = {
            'username': 'updateduser',
            'password': 'updatedpass123',
            'email': 'updated@example.com',
            'hovaten': 'Updated User',
            'sodienthoai': '1111111111',
            'vaitro': 'user',
            'trangthai': 'Block'
        }
        serializer = TaiKhoanSerializer(instance=self.tai_khoan, data=data)
        self.assertTrue(serializer.is_valid())
        tai_khoan = serializer.save()
        self.assertEqual(tai_khoan.hovaten, 'Updated User')
        self.assertEqual(tai_khoan.user.username, 'updateduser')
        self.assertTrue(tai_khoan.user.check_password('updatedpass123'))
        self.assertEqual(tai_khoan.user.email, 'updated@example.com')


class LoaiSanhSerializerTest(TestCase):
    """Test cases cho LoaiSanhSerializer"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho LoaiSanhSerializer"""
        self.loai_sanh = LoaiSanh.objects.create(
            ten_loai_sanh='Sảnh VIP',
            gia_ban_toi_thieu=5000000.0
        )
        self.serializer = LoaiSanhSerializer(instance=self.loai_sanh)

    def test_loai_sanh_serializer_fields(self):
        """Test các trường của LoaiSanhSerializer"""
        data = self.serializer.data
        self.assertEqual(data['id'], self.loai_sanh.id)
        self.assertEqual(data['ten_loai_sanh'], 'Sảnh VIP')
        self.assertEqual(data['gia_ban_toi_thieu'], 5000000.0)

    def test_loai_sanh_serializer_create(self):
        """Test tạo mới LoaiSanh"""
        data = {
            'ten_loai_sanh': 'Sảnh Thường',
            'gia_ban_toi_thieu': 3000000.0
        }
        serializer = LoaiSanhSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        loai_sanh = serializer.save()
        self.assertEqual(loai_sanh.ten_loai_sanh, 'Sảnh Thường')
        self.assertEqual(loai_sanh.gia_ban_toi_thieu, 3000000.0)

    def test_loai_sanh_serializer_update(self):
        """Test cập nhật LoaiSanh"""
        data = {
            'ten_loai_sanh': 'Sảnh VIP Plus',
            'gia_ban_toi_thieu': 7000000.0
        }
        serializer = LoaiSanhSerializer(instance=self.loai_sanh, data=data)
        self.assertTrue(serializer.is_valid())
        loai_sanh = serializer.save()
        self.assertEqual(loai_sanh.ten_loai_sanh, 'Sảnh VIP Plus')
        self.assertEqual(loai_sanh.gia_ban_toi_thieu, 7000000.0)


class SanhSerializerTest(TestCase):
    """Test cases cho SanhSerializer"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho SanhSerializer"""
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
        self.serializer = SanhSerializer(instance=self.sanh)

    def test_sanh_serializer_fields(self):
        """Test các trường của SanhSerializer"""
        data = self.serializer.data
        self.assertEqual(data['id'], self.sanh.id)
        self.assertEqual(data['ten_sanh'], 'Sảnh Hoa Hồng')
        self.assertEqual(data['so_luong_ban_toi_da'], 50)
        self.assertEqual(data['trang_thai'], 'Active')
        self.assertEqual(data['loai_sanh']['id'], self.loai_sanh.id)
        self.assertEqual(data['loai_sanh']['ten_loai_sanh'], 'Sảnh VIP')

    def test_sanh_serializer_create(self):
        """Test tạo mới Sanh"""
        data = {
            'loai_sanh_id': self.loai_sanh.id,
            'ten_sanh': 'Sảnh Hoa Cúc',
            'so_luong_ban_toi_da': 30,
            'trang_thai': 'Maintaining'
        }
        serializer = SanhSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        sanh = serializer.save()
        self.assertEqual(sanh.ten_sanh, 'Sảnh Hoa Cúc')
        self.assertEqual(sanh.loai_sanh, self.loai_sanh)
        self.assertEqual(sanh.trang_thai, 'Maintaining')

    def test_sanh_serializer_update(self):
        """Test cập nhật Sanh"""
        data = {
            'loai_sanh_id': self.loai_sanh.id,
            'ten_sanh': 'Sảnh Hoa Hồng VIP',
            'so_luong_ban_toi_da': 60,
            'trang_thai': 'Active'
        }
        serializer = SanhSerializer(instance=self.sanh, data=data)
        self.assertTrue(serializer.is_valid())
        sanh = serializer.save()
        self.assertEqual(sanh.ten_sanh, 'Sảnh Hoa Hồng VIP')
        self.assertEqual(sanh.so_luong_ban_toi_da, 60)


class MonAnSerializerTest(TestCase):
    """Test cases cho MonAnSerializer"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho MonAnSerializer"""
        self.mon_an = MonAn.objects.create(
            ten_mon_an='Gà nướng',
            don_gia=150000.0,
            ghi_chu='Gà ta nướng lá chanh'
        )
        self.serializer = MonAnSerializer(instance=self.mon_an)

    def test_mon_an_serializer_fields(self):
        """Test các trường của MonAnSerializer"""
        data = self.serializer.data
        self.assertEqual(data['id'], self.mon_an.id)
        self.assertEqual(data['ten_mon_an'], 'Gà nướng')
        self.assertEqual(data['don_gia'], 150000.0)
        self.assertEqual(data['ghi_chu'], 'Gà ta nướng lá chanh')

    def test_mon_an_serializer_create(self):
        """Test tạo mới MonAn"""
        data = {
            'ten_mon_an': 'Cơm trắng',
            'don_gia': 20000.0,
            'ghi_chu': 'Cơm gạo tám'
        }
        serializer = MonAnSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        mon_an = serializer.save()
        self.assertEqual(mon_an.ten_mon_an, 'Cơm trắng')
        self.assertEqual(mon_an.don_gia, 20000.0)

    def test_mon_an_serializer_create_blank_ghi_chu(self):
        """Test tạo MonAn với ghi_chu để trống"""
        data = {
            'ten_mon_an': 'Canh chua',
            'don_gia': 50000.0
        }
        serializer = MonAnSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        mon_an = serializer.save()
        self.assertEqual(mon_an.ghi_chu, '')


class DichVuSerializerTest(TestCase):
    """Test cases cho DichVuSerializer"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho DichVuSerializer"""
        self.dich_vu = DichVu.objects.create(
            ten_dich_vu='Trang trí sảnh',
            mo_ta='Trang trí hoa và bóng bay',
            don_gia=2000000.0
        )
        self.serializer = DichVuSerializer(instance=self.dich_vu)

    def test_dich_vu_serializer_fields(self):
        """Test các trường của DichVuSerializer"""
        data = self.serializer.data
        self.assertEqual(data['id'], self.dich_vu.id)
        self.assertEqual(data['ten_dich_vu'], 'Trang trí sảnh')
        self.assertEqual(data['mo_ta'], 'Trang trí hoa và bóng bay')
        self.assertEqual(data['don_gia'], 2000000.0)

    def test_dich_vu_serializer_create(self):
        """Test tạo mới DichVu"""
        data = {
            'ten_dich_vu': 'Âm thanh',
            'mo_ta': 'Hệ thống âm thanh chuyên nghiệp',
            'don_gia': 500000.0
        }
        serializer = DichVuSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        dich_vu = serializer.save()
        self.assertEqual(dich_vu.ten_dich_vu, 'Âm thanh')
        self.assertEqual(dich_vu.don_gia, 500000.0)


class QuyDinhSerializerTest(TestCase):
    """Test cases cho QuyDinhSerializer"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho QuyDinhSerializer"""
        self.quy_dinh = QuyDinh.objects.create(
            ma_quy_dinh='QD001',
            mo_ta='Quy định về tiền cọc',
            gia_tri='30%',
            dang_ap_dung=True
        )
        self.serializer = QuyDinhSerializer(instance=self.quy_dinh)

    def test_quy_dinh_serializer_fields(self):
        """Test các trường của QuyDinhSerializer"""
        data = self.serializer.data
        self.assertEqual(data['id'], self.quy_dinh.id)
        self.assertEqual(data['ma_quy_dinh'], 'QD001')
        self.assertEqual(data['mo_ta'], 'Quy định về tiền cọc')
        self.assertEqual(data['gia_tri'], '30%')
        self.assertTrue(data['dang_ap_dung'])

    def test_quy_dinh_serializer_create(self):
        """Test tạo mới QuyDinh"""
        data = {
            'ma_quy_dinh': 'QD002',
            'mo_ta': 'Quy định về thời gian',
            'gia_tri': '2 giờ',
            'dang_ap_dung': False
        }
        serializer = QuyDinhSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        quy_dinh = serializer.save()
        self.assertEqual(quy_dinh.ma_quy_dinh, 'QD002')
        self.assertFalse(quy_dinh.dang_ap_dung)


class TiecCuoiSerializerTest(TestCase):
    """Test cases cho TiecCuoiSerializer"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho TiecCuoiSerializer"""
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
        
        self.serializer = TiecCuoiSerializer(instance=self.tiec_cuoi)

    def test_tiec_cuoi_serializer_fields(self):
        """Test các trường của TiecCuoiSerializer"""
        data = self.serializer.data
        self.assertEqual(data['id'], self.tiec_cuoi.id)
        self.assertEqual(data['ten_chu_re'], 'Nguyễn Văn A')
        self.assertEqual(data['ten_co_dau'], 'Trần Thị B')
        self.assertEqual(data['so_luong_ban'], 20)
        self.assertEqual(data['ca'], 'Trưa')
        self.assertEqual(data['tien_dat_coc'], 3000000.0)
        self.assertEqual(data['sanh']['ten_sanh'], 'Sảnh Hoa Hồng')

    def test_tiec_cuoi_serializer_create(self):
        """Test tạo mới TiecCuoi"""
        data = {
            'sanh_id': self.sanh.id,
            'ten_chu_re': 'Lê Văn C',
            'ten_co_dau': 'Phạm Thị D',
            'ngay_dai_tiec': (date.today() + timedelta(days=60)).isoformat(),
            'so_luong_ban': 25,
            'so_luong_ban_du_tru': 3,
            'ca': 'Tối',
            'tien_dat_coc': 4000000.0,
            'so_dien_thoai': '0123456789'
        }
        serializer = TiecCuoiSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        tiec_cuoi = serializer.save()
        self.assertEqual(tiec_cuoi.ten_chu_re, 'Lê Văn C')
        self.assertEqual(tiec_cuoi.sanh, self.sanh)
        self.assertEqual(tiec_cuoi.ca, 'Tối')


class HoaDonSerializerTest(TestCase):
    """Test cases cho HoaDonSerializer"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho HoaDonSerializer"""
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
        
        self.serializer = HoaDonSerializer(instance=self.hoa_don)

    def test_hoa_don_serializer_fields(self):
        """Test các trường của HoaDonSerializer"""
        data = self.serializer.data
        self.assertEqual(data['id'], self.hoa_don.id)
        self.assertEqual(data['ma_hoa_don'], self.hoa_don.id)
        self.assertEqual(data['ma_tiec'], self.tiec_cuoi.id)
        self.assertEqual(data['trang_thai'], 'Đã thanh toán')
        self.assertEqual(data['so_luong_ban'], 20)
        self.assertEqual(data['tien_coc'], 3000000.0)
        self.assertEqual(data['tiec_cuoi']['ten_chu_re'], 'Nguyễn Văn A')

    def test_hoa_don_serializer_create(self):
        """Test tạo mới HoaDon"""
        data = {
            'tiec_cuoi_id': self.tiec_cuoi.id,
            'ngay_thanh_toan': date.today().isoformat(),
            'so_ngay_tre': 0,
            'trang_thai': 'Chưa thanh toán',
            'so_luong_ban': 20
        }
        serializer = HoaDonSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        hoa_don = serializer.save()
        self.assertEqual(hoa_don.tiec_cuoi, self.tiec_cuoi)
        self.assertEqual(hoa_don.trang_thai, 'Chưa thanh toán')

    def test_hoa_don_serializer_get_tien_con_lai(self):
        """Test phương thức get_tien_con_lai"""
        data = self.serializer.data
        tien_con_lai = data['tien_con_lai']
        # Tien con lai = tong tien - tien coc
        expected_tien_con_lai = data['tong_tien'] - data['tien_coc']
        self.assertEqual(tien_con_lai, expected_tien_con_lai)


class ChiTietThucDonSerializerTest(TestCase):
    """Test cases cho ChiTietThucDonSerializer"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho ChiTietThucDonSerializer"""
        # Tạo MonAn
        self.mon_an = MonAn.objects.create(
            ten_mon_an='Gà nướng',
            don_gia=150000.0,
            ghi_chu='Gà ta nướng lá chanh'
        )
        
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
        
        # Tạo ChiTietThucDon
        self.chi_tiet_thuc_don = ChiTietThucDon.objects.create(
            mon_an=self.mon_an,
            tiec_cuoi=self.tiec_cuoi,
            so_luong=1,
            thanh_tien=150000.0,
            ghi_chu='Ghi chú test'
        )
        
        self.serializer = ChiTietThucDonSerializer(instance=self.chi_tiet_thuc_don)

    def test_chi_tiet_thuc_don_serializer_fields(self):
        """Test các trường của ChiTietThucDonSerializer"""
        data = self.serializer.data
        self.assertEqual(data['ten_mon_an'], 'Gà nướng')
        self.assertEqual(data['don_gia'], 150000.0)
        self.assertEqual(data['ghi_chu'], 'Ghi chú test')


class ChiTietDichVuSerializerTest(TestCase):
    """Test cases cho ChiTietDichVuSerializer"""
    
    def setUp(self):
        """Thiết lập dữ liệu test cho ChiTietDichVuSerializer"""
        # Tạo DichVu
        self.dich_vu = DichVu.objects.create(
            ten_dich_vu='Trang trí sảnh',
            mo_ta='Trang trí hoa và bóng bay',
            don_gia=2000000.0
        )
        
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
        
        # Tạo ChiTietDichVu
        self.chi_tiet_dich_vu = ChiTietDichVu.objects.create(
            dich_vu=self.dich_vu,
            tiec_cuoi=self.tiec_cuoi,
            so_luong=1,
            thanh_tien=2000000.0
        )
        
        self.serializer = ChiTietDichVuSerializer(instance=self.chi_tiet_dich_vu)

    def test_chi_tiet_dich_vu_serializer_fields(self):
        """Test các trường của ChiTietDichVuSerializer"""
        data = self.serializer.data
        self.assertEqual(data['ten_dich_vu'], 'Trang trí sảnh')
        self.assertEqual(data['don_gia'], 2000000.0)
        self.assertEqual(data['so_luong'], 1)

    def test_chi_tiet_dich_vu_serializer_create(self):
        """Test tạo mới ChiTietDichVu"""
        data = {
            'so_luong': 2,
            'ghi_chu': 'Ghi chú test'
        }
        serializer = ChiTietDichVuSerializer(data=data)
        self.assertTrue(serializer.is_valid()) 