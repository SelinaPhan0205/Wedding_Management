"""
Pytest configuration và fixtures cho test suite.

File này chứa các fixtures được chia sẻ giữa các test modules,
giúp tái sử dụng code và tối ưu hóa performance của test suite.
"""

import pytest
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date, timedelta
from app.models import *


@pytest.fixture
def user():
    """Fixture tạo user cơ bản cho test."""
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com',
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def admin_user():
    """Fixture tạo admin user cho test."""
    user = User.objects.create_user(
        username='admin',
        password='adminpass123',
        email='admin@example.com',
        first_name='Admin',
        last_name='User'
    )
    return user


@pytest.fixture
def tai_khoan(user):
    """Fixture tạo tài khoản cho test."""
    return TaiKhoan.objects.create(
        user=user,
        sodienthoai='0123456789',
        hovaten='Test User',
        vaitro='admin',
        trangthai='Active'
    )


@pytest.fixture
def admin_tai_khoan(admin_user):
    """Fixture tạo admin tài khoản cho test."""
    return TaiKhoan.objects.create(
        user=admin_user,
        sodienthoai='0987654321',
        hovaten='Admin User',
        vaitro='admin',
        trangthai='Active'
    )


@pytest.fixture
def user_tai_khoan(user):
    """Fixture tạo user tài khoản cho test."""
    return TaiKhoan.objects.create(
        user=user,
        sodienthoai='0123456789',
        hovaten='Test User',
        vaitro='user',
        trangthai='Active'
    )


@pytest.fixture
def loai_sanh():
    """Fixture tạo loại sảnh cho test."""
    return LoaiSanh.objects.create(
        ten_loai_sanh='Sảnh VIP',
        gia_ban_toi_thieu=5000000.0
    )


@pytest.fixture
def loai_sanh_thuong():
    """Fixture tạo loại sảnh thường cho test."""
    return LoaiSanh.objects.create(
        ten_loai_sanh='Sảnh Thường',
        gia_ban_toi_thieu=3000000.0
    )


@pytest.fixture
def sanh(loai_sanh):
    """Fixture tạo sảnh cho test."""
    return Sanh.objects.create(
        loai_sanh=loai_sanh,
        ten_sanh='Sảnh Hoa Hồng',
        so_luong_ban_toi_da=50,
        trang_thai='Active'
    )


@pytest.fixture
def sanh_thuong(loai_sanh_thuong):
    """Fixture tạo sảnh thường cho test."""
    return Sanh.objects.create(
        loai_sanh=loai_sanh_thuong,
        ten_sanh='Sảnh Hoa Cúc',
        so_luong_ban_toi_da=30,
        trang_thai='Active'
    )


@pytest.fixture
def mon_an():
    """Fixture tạo món ăn cho test."""
    return MonAn.objects.create(
        ten_mon_an='Gà nướng',
        don_gia=150000.0,
        ghi_chu='Gà ta nướng lá chanh'
    )


@pytest.fixture
def mon_an_list():
    """Fixture tạo danh sách món ăn cho test."""
    mon_ans = []
    for i in range(5):
        mon_an = MonAn.objects.create(
            ten_mon_an=f'Món ăn {i}',
            don_gia=100000.0 + i * 10000,
            ghi_chu=f'Ghi chú món ăn {i}'
        )
        mon_ans.append(mon_an)
    return mon_ans


@pytest.fixture
def dich_vu():
    """Fixture tạo dịch vụ cho test."""
    return DichVu.objects.create(
        ten_dich_vu='Trang trí sảnh',
        mo_ta='Trang trí hoa và bóng bay',
        don_gia=2000000.0
    )


@pytest.fixture
def dich_vu_list():
    """Fixture tạo danh sách dịch vụ cho test."""
    dich_vus = []
    for i in range(3):
        dich_vu = DichVu.objects.create(
            ten_dich_vu=f'Dịch vụ {i}',
            mo_ta=f'Mô tả dịch vụ {i}',
            don_gia=1000000.0 + i * 500000
        )
        dich_vus.append(dich_vu)
    return dich_vus


@pytest.fixture
def quy_dinh():
    """Fixture tạo quy định cho test."""
    return QuyDinh.objects.create(
        ma_quy_dinh='QD001',
        mo_ta='Quy định về tiền cọc',
        gia_tri='30%',
        dang_ap_dung=True
    )


@pytest.fixture
def quy_dinh_list():
    """Fixture tạo danh sách quy định cho test."""
    quy_dinhs = []
    for i in range(3):
        quy_dinh = QuyDinh.objects.create(
            ma_quy_dinh=f'QD00{i+1}',
            mo_ta=f'Quy định {i+1}',
            gia_tri=f'{20 + i*10}%',
            dang_ap_dung=True
        )
        quy_dinhs.append(quy_dinh)
    return quy_dinhs


@pytest.fixture
def tiec_cuoi(tai_khoan, sanh):
    """Fixture tạo tiệc cưới cho test."""
    return TiecCuoi.objects.create(
        tai_khoan=tai_khoan,
        sanh=sanh,
        ten_chu_re='Nguyễn Văn A',
        ten_co_dau='Trần Thị B',
        ngay_dai_tiec=date(2024, 12, 25),
        so_luong_ban=30,
        so_luong_ban_du_tru=5,
        ca='Tối',
        tien_dat_coc=5000000.0,
        so_dien_thoai='0123456789'
    )


@pytest.fixture
def tiec_cuoi_list(tai_khoan, sanh):
    """Fixture tạo danh sách tiệc cưới cho test."""
    tiec_cuois = []
    for i in range(3):
        tiec_cuoi = TiecCuoi.objects.create(
            tai_khoan=tai_khoan,
            sanh=sanh,
            ten_chu_re=f'Chú rể {i}',
            ten_co_dau=f'Cô dâu {i}',
            ngay_dai_tiec=date(2024, 12, 25) + timedelta(days=i*7),
            so_luong_ban=20 + i*5,
            so_luong_ban_du_tru=3 + i,
            ca='Tối' if i % 2 == 0 else 'Trưa',
            tien_dat_coc=3000000.0 + i*1000000,
            so_dien_thoai=f'012345678{i}'
        )
        tiec_cuois.append(tiec_cuoi)
    return tiec_cuois


@pytest.fixture
def hoa_don(tiec_cuoi):
    """Fixture tạo hóa đơn cho test."""
    return HoaDon.objects.create(
        tiec_cuoi=tiec_cuoi,
        so_luong_ban=30
    )


@pytest.fixture
def hoa_don_thanh_toan(tiec_cuoi):
    """Fixture tạo hóa đơn đã thanh toán cho test."""
    return HoaDon.objects.create(
        tiec_cuoi=tiec_cuoi,
        ngay_thanh_toan=date(2024, 12, 25),
        so_ngay_tre=0,
        trang_thai='Đã thanh toán',
        tien_phat=Decimal('0.00'),
        so_luong_ban=30
    )


@pytest.fixture
def chi_tiet_thuc_don(tiec_cuoi, mon_an):
    """Fixture tạo chi tiết thực đơn cho test."""
    return ChiTietThucDon.objects.create(
        tiec_cuoi=tiec_cuoi,
        mon_an=mon_an,
        so_luong=1,
        thanh_tien=150000.0,
        ghi_chu='Gà ta nướng lá chanh'
    )


@pytest.fixture
def chi_tiet_dich_vu(tiec_cuoi, dich_vu):
    """Fixture tạo chi tiết dịch vụ cho test."""
    return ChiTietDichVu.objects.create(
        tiec_cuoi=tiec_cuoi,
        dich_vu=dich_vu,
        so_luong=1,
        thanh_tien=2000000.0
    )


@pytest.fixture
def complete_tiec_cuoi_setup(tiec_cuoi, mon_an, dich_vu):
    """Fixture tạo tiệc cưới hoàn chỉnh với thực đơn và dịch vụ."""
    ChiTietThucDon.objects.create(
        tiec_cuoi=tiec_cuoi,
        mon_an=mon_an,
        so_luong=1,
        thanh_tien=150000.0
    )
    ChiTietDichVu.objects.create(
        tiec_cuoi=tiec_cuoi,
        dich_vu=dich_vu,
        so_luong=1,
        thanh_tien=2000000.0
    )
    return tiec_cuoi


@pytest.fixture
def authenticated_client(client, user):
    """Fixture tạo authenticated client cho test."""
    client.login(username='testuser', password='testpass123')
    return client


@pytest.fixture
def admin_client(client, admin_user):
    """Fixture tạo admin authenticated client cho test."""
    client.login(username='admin', password='adminpass123')
    return client


@pytest.fixture
def api_client():
    """Fixture tạo API client cho test."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, user):
    """Fixture tạo authenticated API client cho test."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_api_client(api_client, admin_user):
    """Fixture tạo admin authenticated API client cho test."""
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def sample_data(
    user, tai_khoan, loai_sanh, sanh, mon_an, dich_vu, 
    quy_dinh, tiec_cuoi, hoa_don
):
    """Fixture tạo dữ liệu mẫu hoàn chỉnh cho test."""
    return {
        'user': user,
        'tai_khoan': tai_khoan,
        'loai_sanh': loai_sanh,
        'sanh': sanh,
        'mon_an': mon_an,
        'dich_vu': dich_vu,
        'quy_dinh': quy_dinh,
        'tiec_cuoi': tiec_cuoi,
        'hoa_don': hoa_don
    }


@pytest.fixture
def large_dataset():
    """Fixture tạo dataset lớn cho performance test."""
    # Tạo 100 users
    users = []
    for i in range(100):
        user = User.objects.create_user(
            username=f'user{i}',
            password=f'pass{i}',
            email=f'user{i}@example.com'
        )
        users.append(user)
    
    # Tạo 100 tài khoản
    tai_khoans = []
    for i, user in enumerate(users):
        tai_khoan = TaiKhoan.objects.create(
            user=user,
            sodienthoai=f'012345678{i%10}',
            hovaten=f'User {i}',
            vaitro='admin' if i < 10 else 'user',
            trangthai='Active'
        )
        tai_khoans.append(tai_khoan)
    
    # Tạo 50 loại sảnh
    loai_sanhs = []
    for i in range(50):
        loai_sanh = LoaiSanh.objects.create(
            ten_loai_sanh=f'Loại sảnh {i}',
            gia_ban_toi_thieu=1000000.0 + i * 100000
        )
        loai_sanhs.append(loai_sanh)
    
    # Tạo 200 sảnh
    sanhs = []
    for i in range(200):
        sanh = Sanh.objects.create(
            loai_sanh=loai_sanhs[i % 50],
            ten_sanh=f'Sảnh {i}',
            so_luong_ban_toi_da=20 + (i % 30),
            trang_thai='Active' if i % 10 != 0 else 'Maintaining'
        )
        sanhs.append(sanh)
    
    # Tạo 100 món ăn
    mon_ans = []
    for i in range(100):
        mon_an = MonAn.objects.create(
            ten_mon_an=f'Món ăn {i}',
            don_gia=50000.0 + i * 5000,
            ghi_chu=f'Ghi chú món {i}'
        )
        mon_ans.append(mon_an)
    
    # Tạo 50 dịch vụ
    dich_vus = []
    for i in range(50):
        dich_vu = DichVu.objects.create(
            ten_dich_vu=f'Dịch vụ {i}',
            mo_ta=f'Mô tả dịch vụ {i}',
            don_gia=500000.0 + i * 50000
        )
        dich_vus.append(dich_vu)
    
    # Tạo 100 tiệc cưới
    tiec_cuois = []
    for i in range(100):
        tiec_cuoi = TiecCuoi.objects.create(
            tai_khoan=tai_khoans[i],
            sanh=sanhs[i % 200],
            ten_chu_re=f'Chú rể {i}',
            ten_co_dau=f'Cô dâu {i}',
            ngay_dai_tiec=date(2024, 1, 1) + timedelta(days=i),
            so_luong_ban=10 + (i % 20),
            so_luong_ban_du_tru=2 + (i % 5),
            ca='Tối' if i % 2 == 0 else 'Trưa',
            tien_dat_coc=1000000.0 + i * 100000,
            so_dien_thoai=f'012345678{i%10}'
        )
        tiec_cuois.append(tiec_cuoi)
    
    # Tạo 100 hóa đơn
    hoa_dons = []
    for i in range(100):
        hoa_don = HoaDon.objects.create(
            tiec_cuoi=tiec_cuois[i],
            so_luong_ban=10 + (i % 20)
        )
        hoa_dons.append(hoa_don)
    
    return {
        'users': users,
        'tai_khoans': tai_khoans,
        'loai_sanhs': loai_sanhs,
        'sanhs': sanhs,
        'mon_ans': mon_ans,
        'dich_vus': dich_vus,
        'tiec_cuois': tiec_cuois,
        'hoa_dons': hoa_dons
    }


# Pytest markers
def pytest_configure(config):
    """Cấu hình pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "api: marks tests as API tests"
    )
    config.addinivalue_line(
        "markers", "models: marks tests as model tests"
    )
    config.addinivalue_line(
        "markers", "serializers: marks tests as serializer tests"
    )
    config.addinivalue_line(
        "markers", "views: marks tests as view tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )


# Pytest hooks
@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Tự động enable database access cho tất cả tests."""
    pass


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Thiết lập môi trường test."""
    # Có thể thêm các thiết lập chung ở đây
    yield
    # Cleanup sau khi test xong
    pass 