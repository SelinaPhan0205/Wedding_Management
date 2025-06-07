from rest_framework.routers import DefaultRouter
from .views import LoaiSanhViewSet, SanhViewSet, TaiKhoanViewSet

router = DefaultRouter()
router.register(r'loaisanh', LoaiSanhViewSet, basename='loaisanh')
router.register(r'sanh', SanhViewSet, basename='sanh')
router.register(r'taikhoan', TaiKhoanViewSet, basename='taikhoan')

urlpatterns = router.urls