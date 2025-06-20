from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import TaiKhoan

@receiver(post_save, sender=User)
def create_or_update_taikhoan(sender, instance, created, **kwargs):
    if created:
        # Khi User mới được tạo, tạo luôn TaiKhoan tương ứng
        TaiKhoan.objects.create(user=instance, hovaten='', sodienthoai='')
    else:
        # Khi User được cập nhật, nếu đã có TaiKhoan thì lưu lại để đồng bộ
        if hasattr(instance, 'taikhoan'):
            instance.taikhoan.save()
