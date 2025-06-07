from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'loaisanh', LoaiSanhViewSet, basename='loaisanh')
router.register(r'sanh', SanhViewSet, basename='sanh')
router.register(r'taikhoan', TaiKhoanViewSet, basename='taikhoan')
router.register(r'dichvu', DichVuViewSet, basename='dichvu')
router.register(r'monan', MonAnViewSet, basename='monan')

urlpatterns = router.urls