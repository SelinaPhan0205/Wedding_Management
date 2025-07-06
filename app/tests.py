from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import TaiKhoan, LoaiSanh, Sanh, MonAn, DichVu, QuyDinh, TiecCuoi, HoaDon, ChiTietThucDon, ChiTietDichVu
from .serializers import TaiKhoanSerializer, UserSerializer, LoaiSanhSerializer, SanhSerializer, DichVuSerializer, MonAnSerializer, QuyDinhSerializer, ChiTietThucDonSerializer, ChiTietDichVuSerializer, TiecCuoiSerializer, HoaDonSerializer
import datetime

class AuthViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        TaiKhoan.objects.create(user=self.user, hovaten='Test User', sodienthoai='0123456789')

    def test_login_logout(self):
        c = Client()
        response = c.post(reverse('dangnhap'), {'username': 'testuser', 'password': 'testpass'})
        self.assertIn(response.status_code, [200, 302])
        response = c.get(reverse('dangxuat'))
        self.assertIn(response.status_code, [200, 302])

    def test_trangchu_requires_login(self):
        c = Client()
        response = c.get(reverse('trangchu'))
        self.assertIn(response.status_code, [302, 401, 403])
        c.login(username='testuser', password='testpass')
        response = c.get(reverse('trangchu'))
        self.assertEqual(response.status_code, 200)

class ViewTemplateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='viewuser', password='viewpass')
        TaiKhoan.objects.create(user=self.user, hovaten='View User', sodienthoai='0123456789')

    def test_login_view_get(self):
        response = self.client.get(reverse('dangnhap'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/dangnhap.html')

    def test_login_view_post_success(self):
        response = self.client.post(reverse('dangnhap'), {'username': 'viewuser', 'password': 'viewpass'})
        self.assertIn(response.status_code, [200, 302])

    def test_login_view_post_fail(self):
        response = self.client.post(reverse('dangnhap'), {'username': 'viewuser', 'password': 'sai'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'không đúng', status_code=200)

    def test_logout_view(self):
        self.client.login(username='viewuser', password='viewpass')
        response = self.client.get(reverse('dangxuat'))
        self.assertIn(response.status_code, [200, 302])

    def test_trangchu_requires_login(self):
        response = self.client.get(reverse('trangchu'))
        self.assertIn(response.status_code, [302, 401, 403])
        self.client.login(username='viewuser', password='viewpass')
        response = self.client.get(reverse('trangchu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/trangchu.html')

    def test_all_management_views_require_login(self):
        view_names = [
            'quanlytaikhoan', 'quanlysanh', 'quanlytieccuoi', 'quanlyhoadon',
            'quanlythucdon', 'quanlydichvu', 'quanlyquydinh', 'xembaocao',
            'baocaodoanhthu', 'baocaocongno', 'baocaothucthu'
        ]
        for name in view_names:
            url = reverse(name)
            resp = self.client.get(url)
            self.assertIn(resp.status_code, [302, 401, 403])
            self.client.login(username='viewuser', password='viewpass')
            resp2 = self.client.get(url)
            self.assertEqual(resp2.status_code, 200)
            # Kiểm tra template nếu có
            if name.startswith('quanly') or name.startswith('baocao') or name == 'xembaocao':
                self.assertTrue(resp2.templates)

class TaiKhoanSerializerTests(TestCase):
    def test_create_taikhoan_serializer(self):
        data = {
            'username': 'newuser',
            'password': 'newpass',
            'email': 'new@example.com',
            'hovaten': 'Người Mới',
            'sodienthoai': '0987654321',
            'vaitro': 'user',
            'trangthai': 'Active',
        }
        serializer = TaiKhoanSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        tk = serializer.save()
        self.assertEqual(tk.user.username, 'newuser')
        self.assertEqual(tk.hovaten, 'Người Mới')

class SanhAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='sanhuser', password='sanhpass')
        self.taikhoan = TaiKhoan.objects.create(user=self.user, hovaten='Sanh User', sodienthoai='0123456789')
        self.client.force_authenticate(user=self.user)
        self.loai_sanh = LoaiSanh.objects.create(ten_loai_sanh='VIP', gia_ban_toi_thieu=10000000)

    def test_create_sanh(self):
        url = '/api/sanh/'
        data = {
            'ten_sanh': 'Sảnh A',
            'loai_sanh_id': self.loai_sanh.id,
            'so_luong_ban_toi_da': 20,
            'trang_thai': 'Active',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sanh.objects.count(), 1)

    def test_list_sanh(self):
        Sanh.objects.create(ten_sanh='Sảnh B', loai_sanh=self.loai_sanh, so_luong_ban_toi_da=15, trang_thai='Active')
        response = self.client.get('/api/sanh/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_search_sanh(self):
        Sanh.objects.create(ten_sanh='Sảnh VIP', loai_sanh=self.loai_sanh, so_luong_ban_toi_da=15, trang_thai='Active')
        response = self.client.get('/api/sanh/?search=VIP')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_count_sanh(self):
        Sanh.objects.create(ten_sanh='Sảnh C', loai_sanh=self.loai_sanh, so_luong_ban_toi_da=15, trang_thai='Active')
        response = self.client.get('/api/sanh/count/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total', response.data)

    def test_tracuu_sanh(self):
        Sanh.objects.create(ten_sanh='Sảnh D', loai_sanh=self.loai_sanh, so_luong_ban_toi_da=15, trang_thai='Active')
        response = self.client.get('/api/sanh/tracuu/?ngay=2025-12-31&ca=Trưa')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

class TiecCuoiAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='tiecuser', password='tieccuoi')
        self.taikhoan = TaiKhoan.objects.create(user=self.user, hovaten='Tiec User', sodienthoai='0123456789')
        self.client.force_authenticate(user=self.user)
        self.loai_sanh = LoaiSanh.objects.create(ten_loai_sanh='VIP', gia_ban_toi_thieu=10000000)
        self.sanh = Sanh.objects.create(ten_sanh='Sảnh C', loai_sanh=self.loai_sanh, so_luong_ban_toi_da=30, trang_thai='Active')

    def test_create_tieccuoi(self):
        url = '/api/tieccuoi/'
        data = {
            'ten_chu_re': 'A',
            'ten_co_dau': 'B',
            'so_dien_thoai': '0123456789',
            'ngay_dai_tiec': '2025-12-31',
            'ca': 'Trưa',
            'sanh_id': self.sanh.id,
            'so_luong_ban': 10,
            'so_luong_ban_du_tru': 2,
            'tien_dat_coc': 5000000,
            'mon_an': [],
            'dich_vu': [],
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TiecCuoi.objects.count(), 1)

    def test_list_tieccuoi(self):
        TiecCuoi.objects.create(
            ten_chu_re='A', ten_co_dau='B', so_dien_thoai='0123456789',
            ngay_dai_tiec='2025-12-31', ca='Trưa', sanh=self.sanh,
            so_luong_ban=10, so_luong_ban_du_tru=2, tien_dat_coc=5000000
        )
        response = self.client.get('/api/tieccuoi/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_search_tieccuoi(self):
        TiecCuoi.objects.create(
            ten_chu_re='A', ten_co_dau='B', so_dien_thoai='0123456789',
            ngay_dai_tiec='2025-12-31', ca='Trưa', sanh=self.sanh,
            so_luong_ban=10, so_luong_ban_du_tru=2, tien_dat_coc=5000000
        )
        response = self.client.get('/api/tieccuoi/?search=A')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_count_tieccuoi(self):
        TiecCuoi.objects.create(
            ten_chu_re='A', ten_co_dau='B', so_dien_thoai='0123456789',
            ngay_dai_tiec='2025-12-31', ca='Trưa', sanh=self.sanh,
            so_luong_ban=10, so_luong_ban_du_tru=2, tien_dat_coc=5000000
        )
        response = self.client.get('/api/tieccuoi/count/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total', response.data)

class HoaDonAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='hduser', password='hdpass')
        self.taikhoan = TaiKhoan.objects.create(user=self.user, hovaten='HD User', sodienthoai='0123456789')
        self.client.force_authenticate(user=self.user)
        self.loai_sanh = LoaiSanh.objects.create(ten_loai_sanh='VIP', gia_ban_toi_thieu=10000000)
        self.sanh = Sanh.objects.create(ten_sanh='Sảnh D', loai_sanh=self.loai_sanh, so_luong_ban_toi_da=30, trang_thai='Active')
        self.tiec = TiecCuoi.objects.create(
            ten_chu_re='A', ten_co_dau='B', so_dien_thoai='0123456789',
            ngay_dai_tiec='2025-12-31', ca='Trưa', sanh=self.sanh,
            so_luong_ban=10, so_luong_ban_du_tru=2, tien_dat_coc=5000000
        )

    def test_create_hoadon(self):
        url = '/api/hoadon/'
        data = {
            'tiec_cuoi_id': self.tiec.id,
            'so_luong_ban': 10,
            'ngay_thanh_toan': None,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HoaDon.objects.count(), 1)

    def test_list_hoadon(self):
        HoaDon.objects.create(tiec_cuoi=self.tiec, so_luong_ban=10, trang_thai='Chưa thanh toán')
        response = self.client.get('/api/hoadon/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_search_hoadon(self):
        HoaDon.objects.create(tiec_cuoi=self.tiec, so_luong_ban=10, trang_thai='Chưa thanh toán')
        response = self.client.get('/api/hoadon/?search=A')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_count_hoadon(self):
        HoaDon.objects.create(tiec_cuoi=self.tiec, so_luong_ban=10, trang_thai='Chưa thanh toán')
        response = self.client.get('/api/hoadon/count/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total', response.data)

class MonAnDichVuQuyDinhAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='otheruser', password='otherpass')
        self.taikhoan = TaiKhoan.objects.create(user=self.user, hovaten='Other User', sodienthoai='0123456789')
        self.client.force_authenticate(user=self.user)

    def test_create_monan(self):
        url = '/api/monan/'
        data = {'ten_mon_an': 'Gà quay', 'don_gia': 500000, 'ghi_chu': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MonAn.objects.count(), 1)

    def test_create_dichvu(self):
        url = '/api/dichvu/'
        data = {'ten_dich_vu': 'MC', 'don_gia': 2000000, 'mo_ta': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DichVu.objects.count(), 1)

    def test_create_quydinh(self):
        url = '/api/quydinh/'
        data = {'ma_quy_dinh': 'QD01', 'mo_ta': 'Quy định test', 'gia_tri': '100', 'dang_ap_dung': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(QuyDinh.objects.count(), 1)

class TaiKhoanModelTest(TestCase):
    def test_create_update_delete_taikhoan(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        tk = TaiKhoan.objects.create(user=user, hovaten='Test User', sodienthoai='0123456789')
        self.assertEqual(str(tk), 'testuser')
        tk.hovaten = 'User Updated'
        tk.save()
        self.assertEqual(TaiKhoan.objects.get(id=tk.id).hovaten, 'User Updated')
        tk.delete()
        self.assertFalse(TaiKhoan.objects.filter(id=tk.id).exists())
        self.assertFalse(User.objects.filter(username='testuser').exists())

class LoaiSanhModelTest(TestCase):
    def test_create_update_delete_loaisanh(self):
        ls = LoaiSanh.objects.create(ten_loai_sanh='VIP', gia_ban_toi_thieu=10000000)
        self.assertEqual(str(ls), 'VIP')
        ls.ten_loai_sanh = 'Thường'
        ls.save()
        self.assertEqual(LoaiSanh.objects.get(id=ls.id).ten_loai_sanh, 'Thường')
        ls.delete()
        self.assertFalse(LoaiSanh.objects.filter(id=ls.id).exists())

class SanhModelTest(TestCase):
    def setUp(self):
        self.loai_sanh = LoaiSanh.objects.create(ten_loai_sanh='VIP', gia_ban_toi_thieu=10000000)
    def test_create_update_delete_sanh(self):
        sanh = Sanh.objects.create(ten_sanh='Sảnh A', loai_sanh=self.loai_sanh, so_luong_ban_toi_da=20, trang_thai='Active')
        self.assertEqual(str(sanh), 'Sảnh A')
        sanh.ten_sanh = 'Sảnh B'
        sanh.save()
        self.assertEqual(Sanh.objects.get(id=sanh.id).ten_sanh, 'Sảnh B')
        sanh.delete()
        self.assertFalse(Sanh.objects.filter(id=sanh.id).exists())

class MonAnModelTest(TestCase):
    def test_create_update_delete_monan(self):
        mon = MonAn.objects.create(ten_mon_an='Gà quay', don_gia=500000, ghi_chu='')
        self.assertEqual(str(mon), 'Gà quay')
        mon.ten_mon_an = 'Bò né'
        mon.save()
        self.assertEqual(MonAn.objects.get(id=mon.id).ten_mon_an, 'Bò né')
        mon.delete()
        self.assertFalse(MonAn.objects.filter(id=mon.id).exists())

class DichVuModelTest(TestCase):
    def test_create_update_delete_dichvu(self):
        dv = DichVu.objects.create(ten_dich_vu='MC', don_gia=2000000, mo_ta='')
        self.assertEqual(str(dv), 'MC')
        dv.ten_dich_vu = 'Ca sĩ'
        dv.save()
        self.assertEqual(DichVu.objects.get(id=dv.id).ten_dich_vu, 'Ca sĩ')
        dv.delete()
        self.assertFalse(DichVu.objects.filter(id=dv.id).exists())

class QuyDinhModelTest(TestCase):
    def test_create_update_delete_quydinh(self):
        qd = QuyDinh.objects.create(ma_quy_dinh='QD01', mo_ta='Quy định test', gia_tri='100', dang_ap_dung=True)
        self.assertEqual(str(qd), 'QD01')
        qd.mo_ta = 'Quy định sửa'
        qd.save()
        self.assertEqual(QuyDinh.objects.get(id=qd.id).mo_ta, 'Quy định sửa')
        qd.delete()
        self.assertFalse(QuyDinh.objects.filter(id=qd.id).exists())

class TiecCuoiModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tcuser', password='123')
        self.tk = TaiKhoan.objects.create(user=self.user, hovaten='TC User', sodienthoai='0123456789')
        self.loai_sanh = LoaiSanh.objects.create(ten_loai_sanh='VIP', gia_ban_toi_thieu=10000000)
        self.sanh = Sanh.objects.create(ten_sanh='Sảnh TC', loai_sanh=self.loai_sanh, so_luong_ban_toi_da=20, trang_thai='Active')
    def test_create_update_delete_tieccuoi(self):
        tc = TiecCuoi.objects.create(
            tai_khoan=self.tk, sanh=self.sanh, ten_chu_re='A', ten_co_dau='B',
            ngay_dai_tiec=datetime.date(2025, 12, 31), so_luong_ban=10, so_luong_ban_du_tru=2,
            ca='Trưa', tong_tien_tiec_cuoi=0, tien_dat_coc=5000000, so_dien_thoai='0123456789'
        )
        self.assertIn('A', str(tc))
        tc.ten_chu_re = 'C'
        tc.save()
        self.assertEqual(TiecCuoi.objects.get(id=tc.id).ten_chu_re, 'C')
        tc.delete()
        self.assertFalse(TiecCuoi.objects.filter(id=tc.id).exists())
    def test_tinh_tong_tien(self):
        tc = TiecCuoi.objects.create(
            tai_khoan=self.tk, sanh=self.sanh, ten_chu_re='A', ten_co_dau='B',
            ngay_dai_tiec=datetime.date(2025, 12, 31), so_luong_ban=2, so_luong_ban_du_tru=0,
            ca='Trưa', tong_tien_tiec_cuoi=0, tien_dat_coc=5000000, so_dien_thoai='0123456789'
        )
        mon = MonAn.objects.create(ten_mon_an='Gà quay', don_gia=1000000, ghi_chu='')
        ChiTietThucDon.objects.create(mon_an=mon, tiec_cuoi=tc, so_luong=1, thanh_tien=1000000)
        dv = DichVu.objects.create(ten_dich_vu='MC', don_gia=2000000, mo_ta='')
        ChiTietDichVu.objects.create(dich_vu=dv, tiec_cuoi=tc, so_luong=1, thanh_tien=2000000)
        tong = tc.tinh_tong_tien()
        self.assertEqual(tong, 1000000*2 + 2000000)

class HoaDonModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='hduser', password='123')
        self.tk = TaiKhoan.objects.create(user=self.user, hovaten='HD User', sodienthoai='0123456789')
        self.loai_sanh = LoaiSanh.objects.create(ten_loai_sanh='VIP', gia_ban_toi_thieu=10000000)
        self.sanh = Sanh.objects.create(ten_sanh='Sảnh HD', loai_sanh=self.loai_sanh, so_luong_ban_toi_da=20, trang_thai='Active')
        self.tc = TiecCuoi.objects.create(
            tai_khoan=self.tk, sanh=self.sanh, ten_chu_re='A', ten_co_dau='B',
            ngay_dai_tiec=datetime.date(2025, 12, 31), so_luong_ban=2, so_luong_ban_du_tru=0,
            ca='Trưa', tong_tien_tiec_cuoi=0, tien_dat_coc=5000000, so_dien_thoai='0123456789'
        )
    def test_create_update_delete_hoadon(self):
        hd = HoaDon.objects.create(tiec_cuoi=self.tc, so_luong_ban=2, trang_thai='Chưa thanh toán')
        self.assertIn('HĐ', str(hd))
        hd.trang_thai = 'Đã thanh toán'
        hd.save()
        self.assertEqual(HoaDon.objects.get(id=hd.id).trang_thai, 'Đã thanh toán')
        hd.delete()
        self.assertFalse(HoaDon.objects.filter(id=hd.id).exists())
    def test_tinh_tong_tien(self):
        hd = HoaDon.objects.create(tiec_cuoi=self.tc, so_luong_ban=2, trang_thai='Chưa thanh toán')
        mon = MonAn.objects.create(ten_mon_an='Gà quay', don_gia=1000000, ghi_chu='')
        ChiTietThucDon.objects.create(mon_an=mon, tiec_cuoi=self.tc, so_luong=1, thanh_tien=1000000)
        dv = DichVu.objects.create(ten_dich_vu='MC', don_gia=2000000, mo_ta='')
        ChiTietDichVu.objects.create(dich_vu=dv, tiec_cuoi=self.tc, so_luong=1, thanh_tien=2000000)
        tong = hd.tinh_tong_tien()
        self.assertEqual(tong, 1000000*2 + 2000000)

class ChiTietThucDonModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cttduser', password='123')
        self.tk = TaiKhoan.objects.create(user=self.user, hovaten='CTTD User', sodienthoai='0123456789')
        self.loai_sanh = LoaiSanh.objects.create(ten_loai_sanh='VIP', gia_ban_toi_thieu=10000000)
        self.sanh = Sanh.objects.create(ten_sanh='Sảnh CTTD', loai_sanh=self.loai_sanh, so_luong_ban_toi_da=20, trang_thai='Active')
        self.tc = TiecCuoi.objects.create(
            tai_khoan=self.tk, sanh=self.sanh, ten_chu_re='A', ten_co_dau='B',
            ngay_dai_tiec=datetime.date(2025, 12, 31), so_luong_ban=2, so_luong_ban_du_tru=0,
            ca='Trưa', tong_tien_tiec_cuoi=0, tien_dat_coc=5000000, so_dien_thoai='0123456789'
        )
        self.mon = MonAn.objects.create(ten_mon_an='Gà quay', don_gia=1000000, ghi_chu='')
    def test_create_update_delete_chitietthucdon(self):
        cttd = ChiTietThucDon.objects.create(mon_an=self.mon, tiec_cuoi=self.tc, so_luong=1, thanh_tien=1000000)
        self.assertIn('Gà quay', str(cttd))
        cttd.so_luong = 2
        cttd.save()
        self.assertEqual(ChiTietThucDon.objects.get(id=cttd.id).so_luong, 2)
        cttd.delete()
        self.assertFalse(ChiTietThucDon.objects.filter(id=cttd.id).exists())

class ChiTietDichVuModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ctdvuser', password='123')
        self.tk = TaiKhoan.objects.create(user=self.user, hovaten='CTDV User', sodienthoai='0123456789')
        self.loai_sanh = LoaiSanh.objects.create(ten_loai_sanh='VIP', gia_ban_toi_thieu=10000000)
        self.sanh = Sanh.objects.create(ten_sanh='Sảnh CTDV', loai_sanh=self.loai_sanh, so_luong_ban_toi_da=20, trang_thai='Active')
        self.tc = TiecCuoi.objects.create(
            tai_khoan=self.tk, sanh=self.sanh, ten_chu_re='A', ten_co_dau='B',
            ngay_dai_tiec=datetime.date(2025, 12, 31), so_luong_ban=2, so_luong_ban_du_tru=0,
            ca='Trưa', tong_tien_tiec_cuoi=0, tien_dat_coc=5000000, so_dien_thoai='0123456789'
        )
        self.dv = DichVu.objects.create(ten_dich_vu='MC', don_gia=2000000, mo_ta='')
    def test_create_update_delete_chitietdichvu(self):
        ctdv = ChiTietDichVu.objects.create(dich_vu=self.dv, tiec_cuoi=self.tc, so_luong=1, thanh_tien=2000000)
        self.assertIn('MC', str(ctdv))
        ctdv.so_luong = 2
        ctdv.save()
        self.assertEqual(ChiTietDichVu.objects.get(id=ctdv.id).so_luong, 2)
        ctdv.delete()
        self.assertFalse(ChiTietDichVu.objects.filter(id=ctdv.id).exists())

class UserSerializerTest(TestCase):
    def test_valid_data(self):
        user = User.objects.create_user(username='user1', email='user1@example.com', password='123')
        serializer = UserSerializer(user)
        self.assertEqual(serializer.data['username'], 'user1')
        self.assertEqual(serializer.data['email'], 'user1@example.com')

class LoaiSanhSerializerTest(TestCase):
    def test_valid_data(self):
        data = {'ten_loai_sanh': 'VIP', 'gia_ban_toi_thieu': 10000000}
        serializer = LoaiSanhSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        obj = serializer.save()
        self.assertEqual(obj.ten_loai_sanh, 'VIP')
    def test_invalid_data(self):
        data = {'ten_loai_sanh': '', 'gia_ban_toi_thieu': None}
        serializer = LoaiSanhSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class SanhSerializerTest(TestCase):
    def setUp(self):
        self.loai_sanh = LoaiSanh.objects.create(ten_loai_sanh='VIP', gia_ban_toi_thieu=10000000)
    def test_valid_data(self):
        data = {'ten_sanh': 'Sảnh A', 'loai_sanh_id': self.loai_sanh.id, 'so_luong_ban_toi_da': 20, 'trang_thai': 'Active'}
        serializer = SanhSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        obj = serializer.save()
        self.assertEqual(obj.ten_sanh, 'Sảnh A')
    def test_invalid_data(self):
        data = {'ten_sanh': '', 'loai_sanh_id': None, 'so_luong_ban_toi_da': None, 'trang_thai': ''}
        serializer = SanhSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class TaiKhoanSerializerTest(TestCase):
    def test_valid_data(self):
        data = {
            'username': 'newuser',
            'password': 'newpass',
            'email': 'new@example.com',
            'hovaten': 'Người Mới',
            'sodienthoai': '0987654321',
            'vaitro': 'user',
            'trangthai': 'Active',
        }
        serializer = TaiKhoanSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        obj = serializer.save()
        self.assertEqual(obj.user.username, 'newuser')
    def test_invalid_data(self):
        data = {'username': '', 'password': '', 'hovaten': '', 'sodienthoai': '', 'vaitro': '', 'trangthai': ''}
        serializer = TaiKhoanSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class DichVuSerializerTest(TestCase):
    def test_valid_data(self):
        data = {'ten_dich_vu': 'MC', 'don_gia': 2000000, 'mo_ta': ''}
        serializer = DichVuSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        obj = serializer.save()
        self.assertEqual(obj.ten_dich_vu, 'MC')
    def test_invalid_data(self):
        data = {'ten_dich_vu': '', 'don_gia': None}
        serializer = DichVuSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class MonAnSerializerTest(TestCase):
    def test_valid_data(self):
        data = {'ten_mon_an': 'Gà quay', 'don_gia': 500000, 'ghi_chu': ''}
        serializer = MonAnSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        obj = serializer.save()
        self.assertEqual(obj.ten_mon_an, 'Gà quay')
    def test_invalid_data(self):
        data = {'ten_mon_an': '', 'don_gia': None}
        serializer = MonAnSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class QuyDinhSerializerTest(TestCase):
    def test_valid_data(self):
        data = {'ma_quy_dinh': 'QD01', 'mo_ta': 'Quy định test', 'gia_tri': '100', 'dang_ap_dung': True}
        serializer = QuyDinhSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        obj = serializer.save()
        self.assertEqual(obj.ma_quy_dinh, 'QD01')
    def test_invalid_data(self):
        data = {'ma_quy_dinh': '', 'mo_ta': '', 'gia_tri': '', 'dang_ap_dung': None}
        serializer = QuyDinhSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class ChiTietThucDonSerializerTest(TestCase):
    def setUp(self):
        self.mon = MonAn.objects.create(ten_mon_an='Gà quay', don_gia=1000000, ghi_chu='')
        self.user = User.objects.create_user(username='cttduser', password='123')
        self.tk = TaiKhoan.objects.create(user=self.user, hovaten='CTTD User', sodienthoai='0123456789')
        self.loai_sanh = LoaiSanh.objects.create(ten_loai_sanh='VIP', gia_ban_toi_thieu=10000000)
        self.sanh = Sanh.objects.create(ten_sanh='Sảnh CTTD', loai_sanh=self.loai_sanh, so_luong_ban_toi_da=20, trang_thai='Active')
        self.tc = TiecCuoi.objects.create(
            tai_khoan=self.tk, sanh=self.sanh, ten_chu_re='A', ten_co_dau='B',
            ngay_dai_tiec=datetime.date(2025, 12, 31), so_luong_ban=2, so_luong_ban_du_tru=0,
            ca='Trưa', tong_tien_tiec_cuoi=0, tien_dat_coc=5000000, so_dien_thoai='0123456789'
        )
    def test_valid_data(self):
        cttd = ChiTietThucDon.objects.create(mon_an=self.mon, tiec_cuoi=self.tc, so_luong=1, thanh_tien=1000000)
        serializer = ChiTietThucDonSerializer(cttd)
        self.assertEqual(serializer.data['ten_mon_an'], 'Gà quay')
    def test_invalid_data(self):
        data = {'ten_mon_an': '', 'don_gia': None}
        serializer = ChiTietThucDonSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class ChiTietDichVuSerializerTest(TestCase):
    def setUp(self):
        self.dv = DichVu.objects.create(ten_dich_vu='MC', don_gia=2000000, mo_ta='')
        self.user = User.objects.create_user(username='ctdvuser', password='123')
        self.tk = TaiKhoan.objects.create(user=self.user, hovaten='CTDV User', sodienthoai='0123456789')
        self.loai_sanh = LoaiSanh.objects.create(ten_loai_sanh='VIP', gia_ban_toi_thieu=10000000)
        self.sanh = Sanh.objects.create(ten_sanh='Sảnh CTDV', loai_sanh=self.loai_sanh, so_luong_ban_toi_da=20, trang_thai='Active')
        self.tc = TiecCuoi.objects.create(
            tai_khoan=self.tk, sanh=self.sanh, ten_chu_re='A', ten_co_dau='B',
            ngay_dai_tiec=datetime.date(2025, 12, 31), so_luong_ban=2, so_luong_ban_du_tru=0,
            ca='Trưa', tong_tien_tiec_cuoi=0, tien_dat_coc=5000000, so_dien_thoai='0123456789'
        )
    def test_valid_data(self):
        ctdv = ChiTietDichVu.objects.create(dich_vu=self.dv, tiec_cuoi=self.tc, so_luong=1, thanh_tien=2000000)
        serializer = ChiTietDichVuSerializer(ctdv)
        self.assertEqual(serializer.data['ten_dich_vu'], 'MC')
    def test_invalid_data(self):
        data = {'ten_dich_vu': '', 'don_gia': None, 'so_luong': None}
        serializer = ChiTietDichVuSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class TiecCuoiSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tcuser', password='123')
        self.tk = TaiKhoan.objects.create(user=self.user, hovaten='TC User', sodienthoai='0123456789')
        self.loai_sanh = LoaiSanh.objects.create(ten_loai_sanh='VIP', gia_ban_toi_thieu=10000000)
        self.sanh = Sanh.objects.create(ten_sanh='Sảnh TC', loai_sanh=self.loai_sanh, so_luong_ban_toi_da=20, trang_thai='Active')
    def test_valid_data(self):
        data = {
            'tai_khoan': self.tk.id,
            'sanh_id': self.sanh.id,
            'ten_chu_re': 'A',
            'ten_co_dau': 'B',
            'ngay_dai_tiec': '2025-12-31',
            'so_luong_ban': 10,
            'so_luong_ban_du_tru': 2,
            'ca': 'Trưa',
            'tong_tien_tiec_cuoi': 0,
            'tien_dat_coc': 5000000,
            'so_dien_thoai': '0123456789',
        }
        serializer = TiecCuoiSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        obj = serializer.save()
        self.assertEqual(obj.ten_chu_re, 'A')
    def test_invalid_data(self):
        data = {'ten_chu_re': '', 'ten_co_dau': '', 'ngay_dai_tiec': '', 'so_luong_ban': None}
        serializer = TiecCuoiSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class HoaDonSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='hduser', password='123')
        self.tk = TaiKhoan.objects.create(user=self.user, hovaten='HD User', sodienthoai='0123456789')
        self.loai_sanh = LoaiSanh.objects.create(ten_loai_sanh='VIP', gia_ban_toi_thieu=10000000)
        self.sanh = Sanh.objects.create(ten_sanh='Sảnh HD', loai_sanh=self.loai_sanh, so_luong_ban_toi_da=20, trang_thai='Active')
        self.tc = TiecCuoi.objects.create(
            tai_khoan=self.tk, sanh=self.sanh, ten_chu_re='A', ten_co_dau='B',
            ngay_dai_tiec=datetime.date(2025, 12, 31), so_luong_ban=2, so_luong_ban_du_tru=0,
            ca='Trưa', tong_tien_tiec_cuoi=0, tien_dat_coc=5000000, so_dien_thoai='0123456789'
        )
    def test_valid_data(self):
        data = {
            'tiec_cuoi_id': self.tc.id,
            'so_luong_ban': 2,
            'ngay_thanh_toan': None,
        }
        serializer = HoaDonSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        obj = serializer.save()
        self.assertEqual(obj.tiec_cuoi.id, self.tc.id)
    def test_invalid_data(self):
        data = {'tiec_cuoi_id': None, 'so_luong_ban': None}
        serializer = HoaDonSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class LoaiSanhAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='lsuser', password='lspass')
        self.taikhoan = TaiKhoan.objects.create(user=self.user, hovaten='LS User', sodienthoai='0123456789')
        self.client.force_authenticate(user=self.user)

    def test_create_loaisanh(self):
        url = '/api/loaisanh/'
        data = {'ten_loai_sanh': 'VIP', 'gia_ban_toi_thieu': 10000000}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LoaiSanh.objects.count(), 1)

    def test_list_loaisanh(self):
        LoaiSanh.objects.create(ten_loai_sanh='VIP', gia_ban_toi_thieu=10000000)
        response = self.client.get('/api/loaisanh/')
        self.assertEqual(response.status_code, 200)

    def test_update_loaisanh(self):
        ls = LoaiSanh.objects.create(ten_loai_sanh='VIP', gia_ban_toi_thieu=10000000)
        url = f'/api/loaisanh/{ls.id}/'
        data = {'ten_loai_sanh': 'Thường', 'gia_ban_toi_thieu': 5000000}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LoaiSanh.objects.get(id=ls.id).ten_loai_sanh, 'Thường')

    def test_delete_loaisanh(self):
        ls = LoaiSanh.objects.create(ten_loai_sanh='VIP', gia_ban_toi_thieu=10000000)
        url = f'/api/loaisanh/{ls.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(LoaiSanh.objects.filter(id=ls.id).exists())

class TaiKhoanAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='tkuser', password='tkpass')
        self.taikhoan = TaiKhoan.objects.create(user=self.user, hovaten='TK User', sodienthoai='0123456789')
        self.client.force_authenticate(user=self.user)

    def test_create_taikhoan(self):
        url = '/api/taikhoan/'
        data = {
            'username': 'newuser',
            'password': 'newpass',
            'email': 'new@example.com',
            'hovaten': 'Người Mới',
            'sodienthoai': '0987654321',
            'vaitro': 'user',
            'trangthai': 'Active',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaiKhoan.objects.count(), 2)

    def test_list_taikhoan(self):
        response = self.client.get('/api/taikhoan/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_search_taikhoan(self):
        response = self.client.get('/api/taikhoan/?search=User')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_count_taikhoan(self):
        response = self.client.get('/api/taikhoan/count/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total', response.data)

class DichVuAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='dvuser', password='dvpass')
        self.taikhoan = TaiKhoan.objects.create(user=self.user, hovaten='DV User', sodienthoai='0123456789')
        self.client.force_authenticate(user=self.user)

    def test_create_dichvu(self):
        url = '/api/dichvu/'
        data = {'ten_dich_vu': 'MC', 'don_gia': 2000000, 'mo_ta': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DichVu.objects.count(), 1)

    def test_list_dichvu(self):
        DichVu.objects.create(ten_dich_vu='MC', don_gia=2000000, mo_ta='')
        response = self.client.get('/api/dichvu/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_search_dichvu(self):
        DichVu.objects.create(ten_dich_vu='MC', don_gia=2000000, mo_ta='')
        response = self.client.get('/api/dichvu/?search=MC')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_count_dichvu(self):
        DichVu.objects.create(ten_dich_vu='MC', don_gia=2000000, mo_ta='')
        response = self.client.get('/api/dichvu/count/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total', response.data)

class MonAnAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='mauser', password='mapass')
        self.taikhoan = TaiKhoan.objects.create(user=self.user, hovaten='MA User', sodienthoai='0123456789')
        self.client.force_authenticate(user=self.user)

    def test_create_monan(self):
        url = '/api/monan/'
        data = {'ten_mon_an': 'Gà quay', 'don_gia': 500000, 'ghi_chu': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MonAn.objects.count(), 1)

    def test_list_monan(self):
        MonAn.objects.create(ten_mon_an='Gà quay', don_gia=500000, ghi_chu='')
        response = self.client.get('/api/monan/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_search_monan(self):
        MonAn.objects.create(ten_mon_an='Gà quay', don_gia=500000, ghi_chu='')
        response = self.client.get('/api/monan/?search=Gà')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_count_monan(self):
        MonAn.objects.create(ten_mon_an='Gà quay', don_gia=500000, ghi_chu='')
        response = self.client.get('/api/monan/count/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total', response.data)

class QuyDinhAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='qduser', password='qdpass')
        self.taikhoan = TaiKhoan.objects.create(user=self.user, hovaten='QD User', sodienthoai='0123456789')
        self.client.force_authenticate(user=self.user)

    def test_create_quydinh(self):
        url = '/api/quydinh/'
        data = {'ma_quy_dinh': 'QD01', 'mo_ta': 'Quy định test', 'gia_tri': '100', 'dang_ap_dung': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(QuyDinh.objects.count(), 1)

    def test_list_quydinh(self):
        QuyDinh.objects.create(ma_quy_dinh='QD01', mo_ta='Quy định test', gia_tri='100', dang_ap_dung=True)
        response = self.client.get('/api/quydinh/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_search_quydinh(self):
        QuyDinh.objects.create(ma_quy_dinh='QD01', mo_ta='Quy định test', gia_tri='100', dang_ap_dung=True)
        response = self.client.get('/api/quydinh/?search=QD01')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_count_quydinh(self):
        QuyDinh.objects.create(ma_quy_dinh='QD01', mo_ta='Quy định test', gia_tri='100', dang_ap_dung=True)
        response = self.client.get('/api/quydinh/count/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total', response.data)

class ReportAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='reportuser', password='reportpass')
        self.taikhoan = TaiKhoan.objects.create(user=self.user, hovaten='Report User', sodienthoai='0123456789')
        self.client.force_authenticate(user=self.user)

    def test_total_tiec_cuoi(self):
        response = self.client.get('/api/report/total-tiec-cuoi/')
        self.assertEqual(response.status_code, 200)

    def test_overview(self):
        response = self.client.get('/api/report/overview/')
        self.assertEqual(response.status_code, 200)

    def test_top_mon_an(self):
        response = self.client.get('/api/report/top-mon-an/')
        self.assertEqual(response.status_code, 200)

    def test_top_dich_vu(self):
        response = self.client.get('/api/report/top-dich-vu/')
        self.assertEqual(response.status_code, 200)

    def test_sanh_usage(self):
        response = self.client.get('/api/report/sanh-usage/')
        self.assertEqual(response.status_code, 200)

    def test_revenue_report(self):
        response = self.client.get('/api/report/revenue/')
        self.assertEqual(response.status_code, 200)

    def test_debt_report(self):
        response = self.client.get('/api/report/debt/')
        self.assertEqual(response.status_code, 200)

    def test_actual_receipt_report(self):
        response = self.client.get('/api/report/actual-receipt/')
        self.assertEqual(response.status_code, 200)
