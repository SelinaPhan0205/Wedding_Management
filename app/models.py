from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class TaiKhoan(models.Model):
    TRANG_THAI_CHOICES = [
        ('Active', 'Hoạt động'),
        ('Block', 'Bị khoá'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sodienthoai = models.CharField(max_length=15)
    hovaten = models.CharField(max_length=100, default="")
    vaitro = models.CharField(
        max_length=20,
        choices=[('admin', 'Admin'), ('user', 'User')],
        default='user'
    )
    trangthai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='Active')

    def __str__(self):
        return self.user.username
    def delete(self, *args, **kwargs):
        # Xóa luôn user liên kết khi xóa TaiKhoan
        user = self.user
        super().delete(*args, **kwargs)
        user.delete()
    
class LoaiSanh(models.Model):
    ten_loai_sanh = models.CharField(max_length=50)
    gia_ban_toi_thieu = models.FloatField()

    def __str__(self):
        return self.ten_loai_sanh

class Sanh(models.Model):
    TRANG_THAI_CHOICES = [
        ('Active', 'Đang hoạt động'),
        ('Maintaining', 'Đang bảo trì'),
    ]

    loai_sanh = models.ForeignKey(LoaiSanh, on_delete=models.CASCADE)
    ten_sanh = models.CharField(max_length=50)
    so_luong_ban_toi_da = models.IntegerField()
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES,default='Đang hoạt động')

    def __str__(self):
        return self.ten_sanh

class MonAn(models.Model):
    ten_mon_an = models.CharField(max_length=50)
    don_gia = models.FloatField()
    ghi_chu = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.ten_mon_an

class DichVu(models.Model):
    ten_dich_vu = models.CharField(max_length=255)
    mo_ta = models.CharField(max_length=200, blank=True)
    don_gia = models.FloatField()

    def __str__(self):
        return self.ten_dich_vu

class QuyDinh(models.Model):
    ma_quy_dinh = models.CharField(max_length=50)
    mo_ta = models.TextField(blank=True)
    gia_tri = models.TextField()
    dang_ap_dung = models.BooleanField(default=True)

    def __str__(self):
        return self.ma_quy_dinh

class TiecCuoi(models.Model):
    CA_CHOICES = [('Trưa', 'Trưa'), ('Tối', 'Tối')]

    tai_khoan = models.ForeignKey(TaiKhoan, on_delete=models.SET_NULL, null=True, blank=True)
    sanh = models.ForeignKey(Sanh, on_delete=models.CASCADE)
    ten_chu_re = models.CharField(max_length=50)
    ten_co_dau = models.CharField(max_length=50)
    ngay_dai_tiec = models.DateField()
    so_luong_ban = models.IntegerField()
    so_luong_ban_du_tru = models.IntegerField()
    ca = models.CharField(max_length=10, choices=CA_CHOICES)
    tong_tien_tiec_cuoi = models.FloatField(default=0)
    tien_dat_coc = models.FloatField()
    so_dien_thoai = models.CharField(max_length=15)

    def tinh_tong_tien(self, so_luong_ban=None):
        """Tính tổng tiền tiệc cưới, cho phép truyền vào số lượng bàn thực tế."""
        tong_mon_an = sum(ct.thanh_tien for ct in self.chitietthucdon_set.all())
        tong_dich_vu = sum(ct.thanh_tien for ct in self.chitietdichvu_set.all())
        if so_luong_ban is None:
            so_luong_ban = self.so_luong_ban
        tong = tong_mon_an * so_luong_ban + tong_dich_vu
        return tong

    def __str__(self):
        return f"{self.ten_chu_re} & {self.ten_co_dau} ({self.ngay_dai_tiec})"

class HoaDon(models.Model):
    TRANG_THAI_CHOICES = [
        ('Chưa Thanh Toán', 'Chưa Thanh Toán'),
        ('Đã thanh toán', 'Đã thanh toán'),
        ('Trễ hạn', 'Trễ hạn'),
    ]

    tiec_cuoi = models.ForeignKey(TiecCuoi, on_delete=models.CASCADE)
    ngay_thanh_toan = models.DateField()
    so_ngay_tre = models.IntegerField(default=0)
    trang_thai = models.CharField(max_length=30, choices=TRANG_THAI_CHOICES, default='Chưa Thanh Toán')
    tien_phat = models.FloatField(default=0)
    so_luong_ban = models.IntegerField(default=0)

    def tinh_tong_tien(self):
        return self.tiec_cuoi.tinh_tong_tien(self.so_luong_ban)
    
    def __str__(self):
        return f"HĐ - {self.tiec_cuoi}"

class ChiTietThucDon(models.Model):
    mon_an = models.ForeignKey(MonAn, on_delete=models.CASCADE)
    tiec_cuoi = models.ForeignKey(TiecCuoi, on_delete=models.CASCADE)
    so_luong = models.IntegerField()
    thanh_tien = models.FloatField()
    ghi_chu = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.mon_an} - {self.tiec_cuoi}"

class ChiTietDichVu(models.Model):
    dich_vu = models.ForeignKey(DichVu, on_delete=models.CASCADE)
    tiec_cuoi = models.ForeignKey(TiecCuoi, on_delete=models.CASCADE)
    so_luong = models.IntegerField()
    thanh_tien = models.FloatField()

    def __str__(self):
        return f"{self.dich_vu} - {self.tiec_cuoi}"
    
