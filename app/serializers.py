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
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True, required=False
    )

    class Meta:
        model = TaiKhoan
        fields = ['id', 'user', 'user_id', 'hovaten', 'sodienthoai', 'vaitro', 'trangthai']

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data and 'user_id' in validated_data:
            user = validated_data['user_id']
        elif user_data and 'username' in validated_data.get('user', {}):
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data.get('email', ''),
                password=user_data.get('password', ''),
                first_name=validated_data.get('hovaten', '').split(' ')[0],
                last_name=validated_data.get('hovaten', '').split(' ')[-1]
            )
        else:
            raise serializers.ValidationError("Username or user_id is required.")
        tai_khoan = TaiKhoan.objects.create(user=user, **validated_data)
        return tai_khoan

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data and 'user_id' in validated_data:
            instance.user = validated_data['user_id']
        elif user_data and 'password' in user_data:
            instance.user.set_password(user_data['password'])
            instance.user.save()
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