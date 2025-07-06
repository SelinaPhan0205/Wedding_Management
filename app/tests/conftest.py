"""
Cấu hình test và fixtures cho pytest
Chạy với: pytest app/tests/ -v
"""

import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date, timedelta
from app.models import (
    TaiKhoan, LoaiSanh, Sanh, MonAn, DichVu, QuyDinh, 
    TiecCuoi, HoaDon, ChiTietThucDon, ChiTietDichVu
)


@pytest.fixture
def user():
    """Fixture tạo user test"""
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com',
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def tai_khoan(user):
    """Fixture tạo tài khoản test"""
    return TaiKhoan.objects.create(
        user=user,
        sodienthoai='0123456789',
        hovaten='Test User',
        vaitro='admin',
        trangthai='Active'
    )


@pytest.fixture
def loai_sanh():
    """Fixture tạo loại sảnh test"""
    return LoaiSanh.objects.create(
        ten_loai_sanh='Sảnh VIP',
        gia_ban_toi_thieu=5000000.0
    )


@pytest.fixture
def sanh(loai_sanh):
    """Fixture tạo sảnh test"""
    return Sanh.objects.create(
        loai_sanh=loai_sanh,
        ten_sanh='Sảnh Hoa Hồng',
        so_luong_ban_toi_da=50,
        trang_thai='Active'
    )


@pytest.fixture
def mon_an():
    """Fixture tạo món ăn test"""
    return MonAn.objects.create(
        ten_mon_an='Gà nướng',
        don_gia=150000.0,
        ghi_chu='Gà ta nướng lá chanh'
    )


@pytest.fixture
def dich_vu():
    """Fixture tạo dịch vụ test"""
    return DichVu.objects.create(
        ten_dich_vu='Trang trí sảnh',
        mo_ta='Trang trí hoa và bóng bay',
        don_gia=2000000.0
    )


@pytest.fixture
def quy_dinh():
    """Fixture tạo quy định test"""
    return QuyDinh.objects.create(
        ma_quy_dinh='QD001',
        mo_ta='Quy định về tiền cọc',
        gia_tri='30%',
        dang_ap_dung=True
    )


@pytest.fixture
def tiec_cuoi(tai_khoan, sanh):
    """Fixture tạo tiệc cưới test"""
    return TiecCuoi.objects.create(
        tai_khoan=tai_khoan,
        sanh=sanh,
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


@pytest.fixture
def hoa_don(tiec_cuoi):
    """Fixture tạo hóa đơn test"""
    return HoaDon.objects.create(
        tiec_cuoi=tiec_cuoi,
        ngay_thanh_toan=date.today(),
        so_ngay_tre=0,
        trang_thai='Đã thanh toán',
        tien_phat=Decimal('0.00'),
        so_luong_ban=20
    )


@pytest.fixture
def chi_tiet_thuc_don(tiec_cuoi, mon_an):
    """Fixture tạo chi tiết thực đơn test"""
    return ChiTietThucDon.objects.create(
        mon_an=mon_an,
        tiec_cuoi=tiec_cuoi,
        so_luong=1,
        thanh_tien=150000.0,
        ghi_chu='Ghi chú test'
    )


@pytest.fixture
def chi_tiet_dich_vu(tiec_cuoi, dich_vu):
    """Fixture tạo chi tiết dịch vụ test"""
    return ChiTietDichVu.objects.create(
        dich_vu=dich_vu,
        tiec_cuoi=tiec_cuoi,
        so_luong=1,
        thanh_tien=2000000.0
    )


@pytest.fixture
def complete_test_data(user, tai_khoan, loai_sanh, sanh, mon_an, dich_vu, quy_dinh, tiec_cuoi, hoa_don, chi_tiet_thuc_don, chi_tiet_dich_vu):
    """Fixture tạo dữ liệu test hoàn chỉnh"""
    return {
        'user': user,
        'tai_khoan': tai_khoan,
        'loai_sanh': loai_sanh,
        'sanh': sanh,
        'mon_an': mon_an,
        'dich_vu': dich_vu,
        'quy_dinh': quy_dinh,
        'tiec_cuoi': tiec_cuoi,
        'hoa_don': hoa_don,
        'chi_tiet_thuc_don': chi_tiet_thuc_don,
        'chi_tiet_dich_vu': chi_tiet_dich_vu
    }


# Cấu hình pytest
def pytest_configure(config):
    """Cấu hình pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


# Cấu hình test database
@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """Cấu hình database cho test"""
    with django_db_blocker.unblock():
        # Tạo dữ liệu test cơ bản nếu cần
        pass


# Cấu hình test client
@pytest.fixture
def client():
    """Fixture tạo test client"""
    from django.test import Client
    return Client()


@pytest.fixture
def authenticated_client(client, user):
    """Fixture tạo authenticated test client"""
    client.login(username='testuser', password='testpass123')
    return client


# Cấu hình API client
@pytest.fixture
def api_client():
    """Fixture tạo API test client"""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, user):
    """Fixture tạo authenticated API test client"""
    api_client.force_authenticate(user=user)
    return api_client


# Test data factories
class TestDataFactory:
    """Factory để tạo dữ liệu test"""
    
    @staticmethod
    def create_user(username='testuser', **kwargs):
        """Tạo user test"""
        defaults = {
            'password': 'testpass123',
            'email': f'{username}@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        defaults.update(kwargs)
        return User.objects.create_user(username=username, **defaults)
    
    @staticmethod
    def create_tai_khoan(user=None, **kwargs):
        """Tạo tài khoản test"""
        if user is None:
            user = TestDataFactory.create_user()
        
        defaults = {
            'sodienthoai': '0123456789',
            'hovaten': 'Test User',
            'vaitro': 'admin',
            'trangthai': 'Active'
        }
        defaults.update(kwargs)
        return TaiKhoan.objects.create(user=user, **defaults)
    
    @staticmethod
    def create_loai_sanh(**kwargs):
        """Tạo loại sảnh test"""
        defaults = {
            'ten_loai_sanh': 'Sảnh VIP',
            'gia_ban_toi_thieu': 5000000.0
        }
        defaults.update(kwargs)
        return LoaiSanh.objects.create(**defaults)
    
    @staticmethod
    def create_sanh(loai_sanh=None, **kwargs):
        """Tạo sảnh test"""
        if loai_sanh is None:
            loai_sanh = TestDataFactory.create_loai_sanh()
        
        defaults = {
            'ten_sanh': 'Sảnh Hoa Hồng',
            'so_luong_ban_toi_da': 50,
            'trang_thai': 'Active'
        }
        defaults.update(kwargs)
        return Sanh.objects.create(loai_sanh=loai_sanh, **defaults)
    
    @staticmethod
    def create_mon_an(**kwargs):
        """Tạo món ăn test"""
        defaults = {
            'ten_mon_an': 'Gà nướng',
            'don_gia': 150000.0,
            'ghi_chu': 'Gà ta nướng lá chanh'
        }
        defaults.update(kwargs)
        return MonAn.objects.create(**defaults)
    
    @staticmethod
    def create_dich_vu(**kwargs):
        """Tạo dịch vụ test"""
        defaults = {
            'ten_dich_vu': 'Trang trí sảnh',
            'mo_ta': 'Trang trí hoa và bóng bay',
            'don_gia': 2000000.0
        }
        defaults.update(kwargs)
        return DichVu.objects.create(**defaults)
    
    @staticmethod
    def create_tiec_cuoi(tai_khoan=None, sanh=None, **kwargs):
        """Tạo tiệc cưới test"""
        if tai_khoan is None:
            user = TestDataFactory.create_user()
            tai_khoan = TestDataFactory.create_tai_khoan(user)
        
        if sanh is None:
            sanh = TestDataFactory.create_sanh()
        
        defaults = {
            'ten_chu_re': 'Nguyễn Văn A',
            'ten_co_dau': 'Trần Thị B',
            'ngay_dai_tiec': date.today() + timedelta(days=30),
            'so_luong_ban': 20,
            'so_luong_ban_du_tru': 5,
            'ca': 'Trưa',
            'tong_tien_tiec_cuoi': 10000000.0,
            'tien_dat_coc': 3000000.0,
            'so_dien_thoai': '0987654321'
        }
        defaults.update(kwargs)
        return TiecCuoi.objects.create(tai_khoan=tai_khoan, sanh=sanh, **defaults)
    
    @staticmethod
    def create_hoa_don(tiec_cuoi=None, **kwargs):
        """Tạo hóa đơn test"""
        if tiec_cuoi is None:
            tiec_cuoi = TestDataFactory.create_tiec_cuoi()
        
        defaults = {
            'ngay_thanh_toan': date.today(),
            'so_ngay_tre': 0,
            'trang_thai': 'Đã thanh toán',
            'tien_phat': Decimal('0.00'),
            'so_luong_ban': 20
        }
        defaults.update(kwargs)
        return HoaDon.objects.create(tiec_cuoi=tiec_cuoi, **defaults)


@pytest.fixture
def factory():
    """Fixture cung cấp TestDataFactory"""
    return TestDataFactory 