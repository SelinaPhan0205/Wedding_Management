from rest_framework import serializers
from .models import Sanh, TaiKhoan, LoaiSanh, MonAn, DichVu, QuyDinh, TiecCuoi, HoaDon, ChiTietThucDon, ChiTietDichVu

class SanhCuoiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sanh
        fields = '__all__'

class TaiKhoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaiKhoan
        fields = '__all__'

class LoaiSanhSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoaiSanh
        fields = '__all__'

class MonAnSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonAn
        fields = '__all__'

class DichVuSerializer(serializers.ModelSerializer):
    class Meta:
        model = DichVu
        fields = '__all__'

class QuyDinhSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuyDinh
        fields = '__all__'

class ChiTietThucDonSerializer(serializers.ModelSerializer):
    thanh_tien = serializers.FloatField(read_only=True)
    tiec_cuoi = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ChiTietThucDon
        fields = ['id', 'tiec_cuoi', 'mon_an', 'so_luong', 'ghi_chu', 'thanh_tien']

class ChiTietDichVuSerializer(serializers.ModelSerializer):
    thanh_tien = serializers.FloatField(read_only=True)
    tiec_cuoi = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ChiTietDichVu
        fields = ['id', 'tiec_cuoi', 'dich_vu', 'so_luong', 'thanh_tien']

class TiecCuoiSerializer(serializers.ModelSerializer):
    thuc_don = ChiTietThucDonSerializer(many=True, write_only=True)
    dich_vu = ChiTietDichVuSerializer(many=True, write_only=True)

    class Meta:
        model = TiecCuoi
        fields = '__all__'
        extra_fields = ['thuc_don', 'dich_vu']

    def create(self, validated_data):
        thuc_don_data = validated_data.pop('thuc_don', [])
        dich_vu_data = validated_data.pop('dich_vu', [])
        tiec_cuoi = TiecCuoi.objects.create(**validated_data)
        for td in thuc_don_data:
            mon_an = MonAn.objects.get(pk=td['mon_an'].id if hasattr(td['mon_an'], 'id') else td['mon_an'])
            thanh_tien = td['so_luong'] * mon_an.don_gia
            ChiTietThucDon.objects.create(
                tiec_cuoi=tiec_cuoi,
                mon_an=mon_an,
                so_luong=td['so_luong'],
                thanh_tien=thanh_tien,
                ghi_chu=td.get('ghi_chu', '')
            )
        for dv in dich_vu_data:
            dich_vu = DichVu.objects.get(pk=dv['dich_vu'].id if hasattr(dv['dich_vu'], 'id') else dv['dich_vu'])
            thanh_tien = dv['so_luong'] * dich_vu.don_gia
            ChiTietDichVu.objects.create(
                tiec_cuoi=tiec_cuoi,
                dich_vu=dich_vu,
                so_luong=dv['so_luong'],
                thanh_tien=thanh_tien
            )
        return tiec_cuoi

class HoaDonSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoaDon
        fields = '__all__'

