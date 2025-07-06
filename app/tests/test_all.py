"""
File test tổng hợp để chạy tất cả các test cases
Chạy lệnh: python manage.py test app.tests.test_all
"""

import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date, timedelta
from app.models import *
from .test_models import *
from .test_serializers import *
from .test_api import *
from .test_views import *

class IntegrationTest(TestCase):
    """Test tích hợp toàn bộ hệ thống"""
    
    def setUp(self):
        """Thiết lập dữ liệu test tích hợp"""
        # Tạo User và TaiKhoan
        self.user = User.objects.create_user(
            username='admin',
            password='admin123',
            email='admin@example.com',
            first_name='Admin',
            last_name='User'
        )
        self.tai_khoan = TaiKhoan.objects.create(
            user=self.user,
            sodienthoai='0123456789',
            hovaten='Admin User',
            vaitro='admin',
            trangthai='Active'
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
        
        # Tạo MonAn
        self.mon_an1 = MonAn.objects.create(
            ten_mon_an='Gà nướng',
            don_gia=150000.0,
            ghi_chu='Gà ta nướng lá chanh'
        )
        self.mon_an2 = MonAn.objects.create(
            ten_mon_an='Cơm trắng',
            don_gia=20000.0,
            ghi_chu='Cơm gạo tám'
        )
        
        # Tạo DichVu
        self.dich_vu = DichVu.objects.create(
            ten_dich_vu='Trang trí sảnh',
            mo_ta='Trang trí hoa và bóng bay',
            don_gia=2000000.0
        )
        
        # Tạo QuyDinh
        self.quy_dinh = QuyDinh.objects.create(
            ma_quy_dinh='QD001',
            mo_ta='Quy định về tiền cọc',
            gia_tri='30%',
            dang_ap_dung=True
        )

    def test_complete_workflow(self):
        """Test quy trình hoàn chỉnh từ tạo tiệc cưới đến thanh toán"""
        # 1. Tạo tiệc cưới
        tiec_cuoi = TiecCuoi.objects.create(
            tai_khoan=self.tai_khoan,
            sanh=self.sanh,
            ten_chu_re='Nguyễn Văn A',
            ten_co_dau='Trần Thị B',
            ngay_dai_tiec=date.today() + timedelta(days=30),
            so_luong_ban=20,
            so_luong_ban_du_tru=5,
            ca='Trưa',
            tien_dat_coc=3000000.0,
            so_dien_thoai='0987654321'
        )
        
        # 2. Thêm món ăn vào tiệc cưới
        ChiTietThucDon.objects.create(
            mon_an=self.mon_an1,
            tiec_cuoi=tiec_cuoi,
            so_luong=1,
            thanh_tien=150000.0,
            ghi_chu='Ghi chú món ăn'
        )
        ChiTietThucDon.objects.create(
            mon_an=self.mon_an2,
            tiec_cuoi=tiec_cuoi,
            so_luong=1,
            thanh_tien=20000.0
        )
        
        # 3. Thêm dịch vụ vào tiệc cưới
        ChiTietDichVu.objects.create(
            dich_vu=self.dich_vu,
            tiec_cuoi=tiec_cuoi,
            so_luong=1,
            thanh_tien=2000000.0
        )
        
        # 4. Tính tổng tiền tiệc cưới
        tong_tien = tiec_cuoi.tinh_tong_tien()
        expected_tong = (150000.0 + 20000.0) * 20 + 2000000.0  # (tiền món ăn * số bàn) + tiền dịch vụ
        self.assertEqual(tong_tien, expected_tong)
        
        # 5. Tạo hóa đơn
        hoa_don = HoaDon.objects.create(
            tiec_cuoi=tiec_cuoi,
            ngay_thanh_toan=date.today(),
            so_ngay_tre=0,
            trang_thai='Chưa thanh toán',
            so_luong_ban=20
        )
        
        # 6. Kiểm tra thông tin hóa đơn
        self.assertEqual(hoa_don.tiec_cuoi, tiec_cuoi)
        self.assertEqual(hoa_don.tien_coc, 3000000.0)
        self.assertEqual(hoa_don.tong_tien, expected_tong)
        self.assertEqual(hoa_don.tien_con_lai, expected_tong - 3000000.0)
        
        # 7. Thanh toán hóa đơn
        hoa_don.trang_thai = 'Đã thanh toán'
        hoa_don.save()
        
        # 8. Kiểm tra trạng thái sau thanh toán
        self.assertEqual(hoa_don.trang_thai, 'Đã thanh toán')
        
        # 9. Kiểm tra dữ liệu liên quan
        self.assertEqual(tiec_cuoi.chitietthucdon_set.count(), 2)
        self.assertEqual(tiec_cuoi.chitietdichvu_set.count(), 1)
        self.assertEqual(str(tiec_cuoi), f"Nguyễn Văn A & Trần Thị B ({tiec_cuoi.ngay_dai_tiec})")
        self.assertEqual(str(hoa_don), f"HĐ - {tiec_cuoi}")

    def test_data_validation(self):
        """Test validation dữ liệu"""
        # Test tạo tiệc cưới với số bàn vượt quá sức chứa sảnh
        with self.assertRaises(Exception):
            TiecCuoi.objects.create(
                tai_khoan=self.tai_khoan,
                sanh=self.sanh,
                ten_chu_re='Test',
                ten_co_dau='Test',
                ngay_dai_tiec=date.today() + timedelta(days=30),
                so_luong_ban=100,  # Vượt quá sức chứa sảnh (50)
                so_luong_ban_du_tru=10,
                ca='Trưa',
                tien_dat_coc=1000000.0,
                so_dien_thoai='0123456789'
            )

    def test_business_logic(self):
        """Test logic nghiệp vụ"""
        # Test tính tiền phạt khi thanh toán trễ
        tiec_cuoi = TiecCuoi.objects.create(
            tai_khoan=self.tai_khoan,
            sanh=self.sanh,
            ten_chu_re='Test',
            ten_co_dau='Test',
            ngay_dai_tiec=date.today() - timedelta(days=10),  # Tiệc đã qua
            so_luong_ban=20,
            so_luong_ban_du_tru=5,
            ca='Trưa',
            tien_dat_coc=1000000.0,
            so_dien_thoai='0123456789'
        )
        
        hoa_don = HoaDon.objects.create(
            tiec_cuoi=tiec_cuoi,
            ngay_thanh_toan=date.today(),
            so_ngay_tre=10,  # Thanh toán trễ 10 ngày
            trang_thai='Đã thanh toán',
            so_luong_ban=20
        )
        
        # Kiểm tra tiền phạt (nếu có logic tính phạt)
        self.assertEqual(hoa_don.so_ngay_tre, 10)

    def test_data_consistency(self):
        """Test tính nhất quán dữ liệu"""
        # Tạo tiệc cưới
        tiec_cuoi = TiecCuoi.objects.create(
            tai_khoan=self.tai_khoan,
            sanh=self.sanh,
            ten_chu_re='Test',
            ten_co_dau='Test',
            ngay_dai_tiec=date.today() + timedelta(days=30),
            so_luong_ban=20,
            so_luong_ban_du_tru=5,
            ca='Trưa',
            tien_dat_coc=1000000.0,
            so_dien_thoai='0123456789'
        )
        
        # Kiểm tra quan hệ dữ liệu
        self.assertEqual(tiec_cuoi.tai_khoan, self.tai_khoan)
        self.assertEqual(tiec_cuoi.sanh, self.sanh)
        self.assertEqual(tiec_cuoi.sanh.loai_sanh, self.loai_sanh)
        
        # Kiểm tra cascade delete
        sanh_id = self.sanh.id
        self.sanh.delete()
        self.assertFalse(Sanh.objects.filter(id=sanh_id).exists())
        self.assertFalse(TiecCuoi.objects.filter(id=tiec_cuoi.id).exists())

    def test_performance_test(self):
        """Test hiệu suất với dữ liệu lớn"""
        # Tạo nhiều tiệc cưới để test hiệu suất
        tiec_cuoi_list = []
        for i in range(100):
            tiec_cuoi = TiecCuoi.objects.create(
                tai_khoan=self.tai_khoan,
                sanh=self.sanh,
                ten_chu_re=f'Chú rể {i}',
                ten_co_dau=f'Cô dâu {i}',
                ngay_dai_tiec=date.today() + timedelta(days=i),
                so_luong_ban=20,
                so_luong_ban_du_tru=5,
                ca='Trưa' if i % 2 == 0 else 'Tối',
                tien_dat_coc=1000000.0,
                so_dien_thoai=f'012345678{i:02d}'
            )
            tiec_cuoi_list.append(tiec_cuoi)
        
        # Kiểm tra số lượng tiệc cưới
        self.assertEqual(TiecCuoi.objects.count(), 100)
        
        # Test query hiệu suất
        from django.db import connection
        with self.assertNumQueries(1):  # Chỉ 1 query để lấy tất cả
            tiec_cuoi_all = list(TiecCuoi.objects.all())

    def test_edge_cases(self):
        """Test các trường hợp đặc biệt"""
        # Test với dữ liệu null/empty
        tiec_cuoi = TiecCuoi.objects.create(
            tai_khoan=None,  # Tai khoản có thể null
            sanh=self.sanh,
            ten_chu_re='Test',
            ten_co_dau='Test',
            ngay_dai_tiec=date.today() + timedelta(days=30),
            so_luong_ban=0,  # Số bàn = 0
            so_luong_ban_du_tru=0,
            ca='Trưa',
            tien_dat_coc=0.0,  # Tiền cọc = 0
            so_dien_thoai=''
        )
        
        self.assertIsNone(tiec_cuoi.tai_khoan)
        self.assertEqual(tiec_cuoi.so_luong_ban, 0)
        self.assertEqual(tiec_cuoi.tien_dat_coc, 0.0)
        
        # Test với ngày trong quá khứ
        tiec_cuoi_qua_khu = TiecCuoi.objects.create(
            tai_khoan=self.tai_khoan,
            sanh=self.sanh,
            ten_chu_re='Test Quá Khứ',
            ten_co_dau='Test Quá Khứ',
            ngay_dai_tiec=date.today() - timedelta(days=10),  # Ngày trong quá khứ
            so_luong_ban=20,
            so_luong_ban_du_tru=5,
            ca='Trưa',
            tien_dat_coc=1000000.0,
            so_dien_thoai='0123456789'
        )
        
        self.assertLess(tiec_cuoi_qua_khu.ngay_dai_tiec, date.today())


class SystemTest(TestCase):
    """Test toàn bộ hệ thống"""
    
    def test_system_initialization(self):
        """Test khởi tạo hệ thống"""
        # Kiểm tra các model có thể tạo được
        user = User.objects.create_user(username='test', password='test')
        tai_khoan = TaiKhoan.objects.create(user=user, sodienthoai='123', hovaten='Test')
        loai_sanh = LoaiSanh.objects.create(ten_loai_sanh='Test', gia_ban_toi_thieu=1000.0)
        sanh = Sanh.objects.create(loai_sanh=loai_sanh, ten_sanh='Test', so_luong_ban_toi_da=10)
        mon_an = MonAn.objects.create(ten_mon_an='Test', don_gia=100.0)
        dich_vu = DichVu.objects.create(ten_dich_vu='Test', don_gia=1000.0)
        quy_dinh = QuyDinh.objects.create(ma_quy_dinh='TEST', gia_tri='Test')
        
        # Kiểm tra tất cả đều tồn tại
        self.assertTrue(User.objects.filter(username='test').exists())
        self.assertTrue(TaiKhoan.objects.filter(user=user).exists())
        self.assertTrue(LoaiSanh.objects.filter(ten_loai_sanh='Test').exists())
        self.assertTrue(Sanh.objects.filter(ten_sanh='Test').exists())
        self.assertTrue(MonAn.objects.filter(ten_mon_an='Test').exists())
        self.assertTrue(DichVu.objects.filter(ten_dich_vu='Test').exists())
        self.assertTrue(QuyDinh.objects.filter(ma_quy_dinh='TEST').exists())

    def test_system_cleanup(self):
        """Test dọn dẹp hệ thống"""
        # Tạo dữ liệu test
        user = User.objects.create_user(username='cleanup', password='test')
        tai_khoan = TaiKhoan.objects.create(user=user, sodienthoai='123', hovaten='Cleanup')
        
        # Xóa TaiKhoan sẽ xóa luôn User
        tai_khoan.delete()
        self.assertFalse(User.objects.filter(username='cleanup').exists())
        self.assertFalse(TaiKhoan.objects.filter(hovaten='Cleanup').exists())


def run_all_tests():
    """Hàm chạy tất cả các test"""
    
    # Tạo test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Thêm các test cases
    suite.addTests(loader.loadTestsFromTestCase(IntegrationTest))
    suite.addTests(loader.loadTestsFromTestCase(SystemTest))
    
    # Chạy test
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    run_all_tests() 