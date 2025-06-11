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