"""
File test tổng hợp để chạy tất cả các test cases
Chạy lệnh: python manage.py test app.tests.test_all
"""

import unittest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from datetime import date, timedelta
from app.models import *
from .test_models import *
from .test_serializers import *
from .test_api import *
from .test_views import *

class IntegrationTest(TestCase):
    """Test cases tích hợp cho toàn bộ hệ thống"""
    
    def setUp(self):
        """Thiết lập dữ liệu test tích hợp"""
        self.client = Client()
        
        # Tạo user và tài khoản
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
        
        # Tạo loại sảnh và sảnh
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
        
        # Tạo món ăn và dịch vụ
        self.mon_an = MonAn.objects.create(
            ten_mon_an='Gà nướng',
            don_gia=150000.0,
            ghi_chu='Gà ta nướng lá chanh'
        )
        self.dich_vu = DichVu.objects.create(
            ten_dich_vu='Trang trí sảnh',
            mo_ta='Trang trí hoa và bóng bay',
            don_gia=2000000.0
        )
        
        # Tạo quy định
        self.quy_dinh = QuyDinh.objects.create(
            ma_quy_dinh='QD001',
            mo_ta='Quy định về tiền cọc',
            gia_tri='30%',
            dang_ap_dung=True
        )

    def test_complete_workflow(self):
        """Test quy trình hoàn chỉnh từ đăng nhập đến tạo tiệc cưới"""
        # 1. Đăng nhập
        response = self.client.post(reverse('dangnhap'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to trang chủ
        
        # 2. Truy cập trang quản lý tiệc cưới
        response = self.client.get(reverse('quanlytieccuoi'))
        self.assertEqual(response.status_code, 200)
        
        # 3. Tạo tiệc cưới qua API
        tiec_cuoi_data = {
            'sanh_id': self.sanh.id,
            'ten_chu_re': 'Nguyễn Văn A',
            'ten_co_dau': 'Trần Thị B',
            'ngay_dai_tiec': '2024-12-25',
            'so_luong_ban': 30,
            'so_luong_ban_du_tru': 5,
            'ca': 'Tối',
            'tien_dat_coc': 5000000.0,
            'so_dien_thoai': '0123456789',
            'mon_an': [
                {'ten_mon_an': 'Gà nướng', 'ghi_chu': 'Gà ta'}
            ],
            'dich_vu': [
                {'ten_dich_vu': 'Trang trí sảnh', 'so_luong': 1}
            ]
        }
        response = self.client.post('/api/tieccuoi/', tiec_cuoi_data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        # 4. Kiểm tra tiệc cưới đã được tạo
        tiec_cuoi = TiecCuoi.objects.get(ten_chu_re='Nguyễn Văn A')
        self.assertEqual(tiec_cuoi.ten_co_dau, 'Trần Thị B')
        self.assertEqual(tiec_cuoi.sanh, self.sanh)
        
        # 5. Kiểm tra chi tiết thực đơn và dịch vụ đã được tạo
        chi_tiet_thuc_don = ChiTietThucDon.objects.filter(tiec_cuoi=tiec_cuoi)
        self.assertEqual(chi_tiet_thuc_don.count(), 1)
        self.assertEqual(chi_tiet_thuc_don.first().mon_an, self.mon_an)
        
        chi_tiet_dich_vu = ChiTietDichVu.objects.filter(tiec_cuoi=tiec_cuoi)
        self.assertEqual(chi_tiet_dich_vu.count(), 1)
        self.assertEqual(chi_tiet_dich_vu.first().dich_vu, self.dich_vu)
        
        # 6. Tạo hóa đơn
        hoa_don_data = {
            'tiec_cuoi_id': tiec_cuoi.id,
            'so_luong_ban': 30
        }
        response = self.client.post('/api/hoadon/', hoa_don_data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        # 7. Kiểm tra hóa đơn đã được tạo
        hoa_don = HoaDon.objects.get(tiec_cuoi=tiec_cuoi)
        self.assertEqual(hoa_don.so_luong_ban, 30)
        
        # 8. Cập nhật hóa đơn thanh toán
        hoa_don_update_data = {
            'ngay_thanh_toan': '2024-12-25',
            'trang_thai': 'Đã thanh toán'
        }
        response = self.client.patch(f'/api/hoadon/{hoa_don.id}/', hoa_don_update_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # 9. Kiểm tra hóa đơn đã được cập nhật
        hoa_don.refresh_from_db()
        self.assertEqual(hoa_don.trang_thai, 'Đã thanh toán')

    def test_search_functionality(self):
        """Test chức năng tìm kiếm"""
        # Đăng nhập
        self.client.login(username='testuser', password='testpass123')
        
        # Test tìm kiếm sảnh
        response = self.client.get('/api/sanh/?search=Hoa Hồng')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)
        
        # Test tìm kiếm tài khoản
        response = self.client.get('/api/taikhoan/?search=Test User')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)
        
        # Test tìm kiếm dịch vụ
        response = self.client.get('/api/dichvu/?search=Trang trí')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)
        
        # Test tìm kiếm món ăn
        response = self.client.get('/api/monan/?search=Gà')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)

    def test_pagination_functionality(self):
        """Test chức năng phân trang"""
        # Đăng nhập
        self.client.login(username='testuser', password='testpass123')
        
        # Tạo thêm dữ liệu để test phân trang
        for i in range(10):
            MonAn.objects.create(
                ten_mon_an=f'Món ăn {i}',
                don_gia=100000.0 + i * 10000
            )
        
        # Test phân trang
        response = self.client.get('/api/monan/?page=1&limit=5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 5)
        self.assertEqual(response.data['total'], 11)  # 10 món mới + 1 món cũ

    def test_report_functionality(self):
        """Test chức năng báo cáo"""
        # Đăng nhập
        self.client.login(username='testuser', password='testpass123')
        
        # Tạo tiệc cưới và hóa đơn để test báo cáo
        tiec_cuoi = TiecCuoi.objects.create(
            tai_khoan=self.tai_khoan,
            sanh=self.sanh,
            ten_chu_re='Nguyễn Văn A',
            ten_co_dau='Trần Thị B',
            ngay_dai_tiec=date(2024, 12, 25),
            so_luong_ban=30,
            so_luong_ban_du_tru=5,
            ca='Tối',
            tien_dat_coc=5000000.0,
            so_dien_thoai='0123456789'
        )
        
        hoa_don = HoaDon.objects.create(
            tiec_cuoi=tiec_cuoi,
            so_luong_ban=30
        )
        
        # Test báo cáo tổng quan
        response = self.client.get('/api/report/overview/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_tiec', response.data)
        self.assertIn('doanh_thu_du_kien', response.data)
        
        # Test báo cáo doanh thu
        response = self.client.get('/api/report/revenue/')
        self.assertEqual(response.status_code, 200)
        
        # Test báo cáo công nợ
        response = self.client.get('/api/report/debt/')
        self.assertEqual(response.status_code, 200)

    def test_authentication_and_authorization(self):
        """Test xác thực và phân quyền"""
        # Test truy cập trang khi chưa đăng nhập
        response = self.client.get(reverse('quanlytieccuoi'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Test truy cập API khi chưa đăng nhập
        response = self.client.get('/api/tieccuoi/')
        self.assertEqual(response.status_code, 200)  # API có thể cho phép truy cập
        
        # Đăng nhập
        self.client.login(username='testuser', password='testpass123')
        
        # Test truy cập trang khi đã đăng nhập
        response = self.client.get(reverse('quanlytieccuoi'))
        self.assertEqual(response.status_code, 200)
        
        # Test truy cập API khi đã đăng nhập
        response = self.client.get('/api/tieccuoi/')
        self.assertEqual(response.status_code, 200)

    def test_data_consistency(self):
        """Test tính nhất quán của dữ liệu"""
        # Tạo tiệc cưới
        tiec_cuoi = TiecCuoi.objects.create(
            tai_khoan=self.tai_khoan,
            sanh=self.sanh,
            ten_chu_re='Nguyễn Văn A',
            ten_co_dau='Trần Thị B',
            ngay_dai_tiec=date(2024, 12, 25),
            so_luong_ban=30,
            so_luong_ban_du_tru=5,
            ca='Tối',
            tien_dat_coc=5000000.0,
            so_dien_thoai='0123456789'
        )
        
        # Tạo chi tiết thực đơn và dịch vụ
        ChiTietThucDon.objects.create(
            tiec_cuoi=tiec_cuoi,
            mon_an=self.mon_an,
            so_luong=1,
            thanh_tien=150000.0
        )
        ChiTietDichVu.objects.create(
            tiec_cuoi=tiec_cuoi,
            dich_vu=self.dich_vu,
            so_luong=1,
            thanh_tien=2000000.0
        )
        
        # Tạo hóa đơn
        hoa_don = HoaDon.objects.create(
            tiec_cuoi=tiec_cuoi,
            so_luong_ban=30
        )
        
        # Kiểm tra tính nhất quán
        # 1. Tổng tiền tiệc cưới phải bằng tổng tiền hóa đơn
        tong_tien_tiec = tiec_cuoi.tinh_tong_tien()
        tong_tien_hoa_don = hoa_don.tinh_tong_tien()
        self.assertEqual(tong_tien_tiec, tong_tien_hoa_don)
        
        # 2. Số lượng bàn trong hóa đơn phải bằng số lượng bàn trong tiệc cưới
        self.assertEqual(hoa_don.so_luong_ban, tiec_cuoi.so_luong_ban)
        
        # 3. Xóa tiệc cưới phải xóa luôn hóa đơn và chi tiết
        tiec_cuoi.delete()
        self.assertFalse(HoaDon.objects.filter(id=hoa_don.id).exists())
        # Không thể filter với tiec_cuoi đã bị xóa
        self.assertFalse(ChiTietThucDon.objects.filter(tiec_cuoi_id=tiec_cuoi.id).exists())
        self.assertFalse(ChiTietDichVu.objects.filter(tiec_cuoi_id=tiec_cuoi.id).exists())

    def test_error_handling(self):
        """Test xử lý lỗi"""
        # Đăng nhập
        self.client.login(username='testuser', password='testpass123')
        
        # Test tạo tiệc cưới với dữ liệu không hợp lệ
        invalid_data = {
            'ten_chu_re': '',  # Tên chú rể không được để trống
            'ngay_dai_tiec': 'invalid-date'  # Ngày không hợp lệ
        }
        response = self.client.post('/api/tieccuoi/', invalid_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test truy cập API không tồn tại
        response = self.client.get('/api/nonexistent/')
        self.assertEqual(response.status_code, 404)
        
        # Test tạo hóa đơn cho tiệc cưới không tồn tại
        invalid_hoa_don_data = {
            'tiec_cuoi_id': 99999,  # ID không tồn tại
            'so_luong_ban': 30
        }
        response = self.client.post('/api/hoadon/', invalid_hoa_don_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)


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