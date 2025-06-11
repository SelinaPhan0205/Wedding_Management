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

        # Nếu user đã tồn tại thì lấy user đó, không tạo mới
        user = None
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                if not password:
                    raise serializers.ValidationError({'password': 'Password là bắt buộc khi tạo user mới!'})
                user = User.objects.create_user(username=username, password=password, email=email)
        else:
            raise serializers.ValidationError({'username': 'Username là bắt buộc!'})

        # Kiểm tra user này đã có TaiKhoan chưa
        if TaiKhoan.objects.filter(user=user).exists():
            raise serializers.ValidationError({'username': 'Tài khoản cho user này đã tồn tại!'})

        tai_khoan = TaiKhoan.objects.create(user=user, **validated_data)
        return tai_khoan

    def update(self, instance, validated_data):
        # Không cho update username, password, email qua TaiKhoanSerializer
        validated_data.pop('username', None)
        validated_data.pop('password', None)
        validated_data.pop('email', None)

        instance.hovaten = validated_data.get('hovaten', instance.hovaten)
        instance.sodienthoai = validated_data.get('sodienthoai', instance.sodienthoai)
        instance.vaitro = validated_data.get('vaitro', instance.vaitro)
        instance.trangthai = validated_data.get('trangthai', instance.trangthai)
        instance.save()
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

    class Meta:
        model = TiecCuoi
        fields = [
            'id', 'tai_khoan', 'sanh', 'sanh_id', 'ten_chu_re', 'ten_co_dau', 'ngay_dai_tiec',
            'so_luong_ban', 'so_luong_ban_du_tru', 'ca', 'tong_tien_tiec_cuoi', 'tien_dat_coc', 'so_dien_thoai',
            'mon_an', 'dich_vu'
        ]
        read_only_fields = ['id', 'mon_an', 'dich_vu']

    def create(self, validated_data):
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
        return instance