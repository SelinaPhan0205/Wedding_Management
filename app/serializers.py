from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class LoaiSanhSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoaiSanh
        fields = ['id', 'ten_loai_sanh']

class SanhSerializer(serializers.ModelSerializer):
    loai_sanh = LoaiSanhSerializer(read_only=True)
    loai_sanh_id = serializers.PrimaryKeyRelatedField(
        queryset=LoaiSanh.objects.all(), source='loai_sanh', write_only=True
    )

    class Meta:
        model = Sanh
        fields = ['id', 'ten_sanh', 'loai_sanh', 'loai_sanh_id', 'so_luong_ban_toi_da', 'trang_thai']


from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TaiKhoan

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TaiKhoanSerializer(serializers.ModelSerializer):
    # Trả về thông tin user (username, email, ...)
    user = UserSerializer(read_only=True)
    # Các trường này chỉ dùng khi tạo mới, không trả về khi GET
    username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)

    class Meta:
        model = TaiKhoan
        fields = [
            'id', 'user', 'hovaten', 'sodienthoai', 'vaitro', 'trangthai',
            'username', 'password', 'email'
        ]
        read_only_fields = ['user']

    def create(self, validated_data):
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)
        email = validated_data.pop('email', '')

        if not username or not password:
            raise serializers.ValidationError({'username': 'Username và password là bắt buộc!'})

        # Kiểm tra user đã tồn tại chưa
        user_qs = User.objects.filter(username=username)
        if user_qs.exists():
            user = user_qs.first()
            # Nếu đã có TaiKhoan cho user này thì báo lỗi
            if TaiKhoan.objects.filter(user=user).exists():
                raise serializers.ValidationError({'user': f"Tài khoản đã tồn tại cho user '{username}'."})
            # Nếu chưa có TaiKhoan thì có thể cập nhật password nếu muốn
            user.set_password(password)
            user.email = email
            user.save()
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()

        tai_khoan = TaiKhoan.objects.create(user=user, **validated_data)
        return tai_khoan

    def update(self, instance, validated_data):
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)
        email = validated_data.pop('email', None)

        # Cập nhật TaiKhoan
        for attr in ['hovaten', 'sodienthoai', 'vaitro', 'trangthai']:
            setattr(instance, attr, validated_data.get(attr, getattr(instance, attr)))
        instance.save()

        # Cập nhật User nếu có dữ liệu
        user = instance.user
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.set_password(password)
        user.save()

        return instance


        
class DichVuSerializer(serializers.ModelSerializer):
    class Meta:
        model = DichVu
        fields = ['id', 'ten_dich_vu', 'don_gia', 'mo_ta']

class MonAnSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonAn
        fields = ['id', 'ten_mon_an', 'don_gia', 'ghi_chu']

class QuyDinhSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuyDinh
        fields = ['id', 'ma_quy_dinh', 'mo_ta', 'gia_tri', 'dang_ap_dung']

class ChiTietThucDonSerializer(serializers.ModelSerializer):
    ten_mon_an = serializers.CharField(source='mon_an.ten_mon_an', read_only=True)
    don_gia = serializers.IntegerField(source='mon_an.don_gia', read_only=True)
    ghi_chu = serializers.CharField(required=False)

    class Meta:
        model = ChiTietThucDon
        fields = ['ten_mon_an', 'don_gia', 'ghi_chu']

class ChiTietDichVuSerializer(serializers.ModelSerializer):
    ten_dich_vu = serializers.CharField(source='dich_vu.ten_dich_vu', read_only=True)
    don_gia = serializers.IntegerField(source='dich_vu.don_gia', read_only=True)
    so_luong = serializers.IntegerField()
    ghi_chu = serializers.CharField(required=False)

    class Meta:
        model = ChiTietDichVu
        fields = ['ten_dich_vu', 'don_gia', 'so_luong', 'ghi_chu']

class TiecCuoiSerializer(serializers.ModelSerializer):
    sanh = SanhSerializer(read_only=True)
    sanh_id = serializers.PrimaryKeyRelatedField(
        queryset=Sanh.objects.all(), source='sanh', write_only=True
    )
    mon_an = ChiTietThucDonSerializer(many=True, source='chitietthucdon_set', read_only=True)
    dich_vu = ChiTietDichVuSerializer(many=True, source='chitietdichvu_set', read_only=True)
    tong_tien_tiec_cuoi = serializers.IntegerField(default=0, required=False)
    tai_khoan = serializers.PrimaryKeyRelatedField(
        queryset=TaiKhoan.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = TiecCuoi
        fields = [
            'id', 'tai_khoan', 'sanh', 'sanh_id', 'ten_chu_re', 'ten_co_dau', 'ngay_dai_tiec',
            'so_luong_ban', 'so_luong_ban_du_tru', 'ca', 'tong_tien_tiec_cuoi', 'tien_dat_coc', 'so_dien_thoai',
            'mon_an', 'dich_vu'
        ]
        read_only_fields = ['id', 'mon_an', 'dich_vu']

    def tinh_tong_tien(self, tiec):
        tong_mon_an = sum(ct.thanh_tien for ct in tiec.chitietthucdon_set.all())
        tong_dich_vu = sum(ct.thanh_tien for ct in tiec.chitietdichvu_set.all())
        tong = (tong_mon_an) * tiec.so_luong_ban + tong_dich_vu
        tiec.tong_tien_tiec_cuoi = tong
        tiec.save()

    def create(self, validated_data):
        # Đảm bảo tong_tien_tiec_cuoi mặc định là 0 nếu không truyền lên
        if 'tong_tien_tiec_cuoi' not in validated_data:
            validated_data['tong_tien_tiec_cuoi'] = 0
        # Nếu không truyền tai_khoan thì bỏ khỏi validated_data
        validated_data.pop('tai_khoan', None)
        mon_an_data = self.initial_data.get('mon_an', [])
        dich_vu_data = self.initial_data.get('dich_vu', [])
        tiec = TiecCuoi.objects.create(**validated_data)
        # Thêm món ăn
        for mon in mon_an_data:
            mon_an_obj = MonAn.objects.get(ten_mon_an=mon['ten_mon_an'])
            ChiTietThucDon.objects.create(
                tiec_cuoi=tiec,
                mon_an=mon_an_obj,
                so_luong=1,
                thanh_tien=mon_an_obj.don_gia,
                ghi_chu=mon.get('ghi_chu', '')
            )
        # Thêm dịch vụ
        for dv in dich_vu_data:
            dich_vu_obj = DichVu.objects.get(ten_dich_vu=dv['ten_dich_vu'])
            so_luong = dv.get('so_luong', 1)
            ChiTietDichVu.objects.create(
                tiec_cuoi=tiec,
                dich_vu=dich_vu_obj,
                so_luong=so_luong,
                thanh_tien=dich_vu_obj.don_gia * so_luong
            )
        self.tinh_tong_tien(tiec)
        return tiec

    def update(self, instance, validated_data):
        # Cập nhật các trường cơ bản
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # Xóa và thêm lại chi tiết món ăn, dịch vụ nếu có
        if 'mon_an' in self.initial_data:
            instance.chitietthucdon_set.all().delete()
            for mon in self.initial_data['mon_an']:
                mon_an_obj = MonAn.objects.get(ten_mon_an=mon['ten_mon_an'])
                ChiTietThucDon.objects.create(
                    tiec_cuoi=instance,
                    mon_an=mon_an_obj,
                    so_luong=1,
                    thanh_tien=mon_an_obj.don_gia,
                    ghi_chu=mon.get('ghi_chu', '')
                )
        if 'dich_vu' in self.initial_data:
            instance.chitietdichvu_set.all().delete()
            for dv in self.initial_data['dich_vu']:
                dich_vu_obj = DichVu.objects.get(ten_dich_vu=dv['ten_dich_vu'])
                so_luong = dv.get('so_luong', 1)
                ChiTietDichVu.objects.create(
                    tiec_cuoi=instance,
                    dich_vu=dich_vu_obj,
                    so_luong=so_luong,
                    thanh_tien=dich_vu_obj.don_gia * so_luong
                )
        self.tinh_tong_tien(instance)
        return instance
    
class HoaDonSerializer(serializers.ModelSerializer):
    ma_hoa_don = serializers.IntegerField(source='id', read_only=True)
    ma_tiec = serializers.IntegerField(source='tiec_cuoi.id', read_only=True)
    tong_tien = serializers.FloatField(source='tiec_cuoi.tong_tien_tiec_cuoi', read_only=True)
    tien_coc = serializers.FloatField(source='tiec_cuoi.tien_dat_coc', read_only=True)
    tien_con_lai = serializers.SerializerMethodField()
    dich_vu = serializers.SerializerMethodField()  # Thêm dòng này

    class Meta:
        model = HoaDon
        fields = [
            'id', 'ma_hoa_don', 'ma_tiec', 'ngay_thanh_toan', 'so_ngay_tre',
            'trang_thai', 'tien_phat', 'tong_tien', 'tien_coc', 'tien_con_lai', 'tiec_cuoi',
            'dich_vu', 'so_luong_ban'
        ]

    def get_tien_con_lai(self, obj):
        tong = obj.tiec_cuoi.tong_tien_tiec_cuoi if obj.tiec_cuoi else 0
        coc = obj.tiec_cuoi.tien_dat_coc if obj.tiec_cuoi else 0
        return tong - coc

    def get_dich_vu(self, obj):
        chi_tiet = ChiTietDichVu.objects.filter(tiec_cuoi=obj.tiec_cuoi).select_related('dich_vu')
        return ChiTietDichVuSerializer(chi_tiet, many=True).data