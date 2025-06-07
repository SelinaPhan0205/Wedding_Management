from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

admin.site.register((TaiKhoan))
admin.site.register((LoaiSanh))
admin.site.register((Sanh))
admin.site.register((MonAn))
admin.site.register((DichVu))
admin.site.register((QuyDinh))
admin.site.register((TiecCuoi))
admin.site.register((HoaDon))
admin.site.register((ChiTietThucDon))
admin.site.register((ChiTietDichVu))

class TaiKhoanInline(admin.StackedInline):  # hoặc TabularInline
    model = TaiKhoan
    can_delete = False
    verbose_name_plural = 'Thông tin tài khoản'
    fk_name = 'user'

class CustomUserAdmin(BaseUserAdmin):
    inlines = (TaiKhoanInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

# Gỡ bỏ User mặc định và đăng ký lại với CustomUserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)