
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import TaiKhoan

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        TaiKhoan.objects.create(user=instance, hovaten='', sodienthoai='')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.taikhoan.save()