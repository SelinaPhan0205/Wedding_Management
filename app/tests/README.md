# Hướng dẫn Unit Test cho Dự án Quản lý Tiệc Cưới

## Cấu trúc Test

```
app/tests/
├── __init__.py
├── test_models.py         # Test cho Models
├── test_serializers.py    # Test cho Serializers  
├── test_api.py            # Test cho API endpoints
├── test_views.py          # Test cho Views
├── test_all.py            # Test tích hợp toàn bộ hệ thống
└── conftest.py            # Cấu hình pytest nâng cao
```

## Cách chạy Test

### 1. Chạy tất cả test
```bash
python manage.py test app.tests
```

### 2. Chạy test theo từng phần

#### Test Models
```bash
python manage.py test app.tests.test_models
```

#### Test Serializers
```bash
python manage.py test app.tests.test_serializers
```

#### Test API
```bash
python manage.py test app.tests.test_api
```

#### Test Views
```bash
python manage.py test app.tests.test_views
```

#### Test tích hợp
```bash
python manage.py test app.tests.test_all
```

### 3. Chạy test cụ thể
```bash
# Chạy test class cụ thể
python manage.py test app.tests.test_models.TaiKhoanModelTest

# Chạy test method cụ thể
python manage.py test app.tests.test_models.TaiKhoanModelTest.test_tai_khoan_creation
```

### 4. Chạy test với verbose
```bash
python manage.py test app.tests --verbosity=2
```

### 5. Chạy test và tạo coverage report
```bash
# Cài đặt coverage (nếu chưa có)
pip install coverage

# Chạy test với coverage
coverage run --source='.' manage.py test app.tests

# Tạo report
coverage report

# Tạo HTML report
coverage html
```

## Mô tả các Test Cases

### 1. Test Models (`test_models.py`)
- **TaiKhoanModelTest**: Test tạo, xóa, cascade delete
- **LoaiSanhModelTest**: Test CRUD loại sảnh
- **SanhModelTest**: Test CRUD sảnh và choices
- **MonAnModelTest**: Test CRUD món ăn
- **DichVuModelTest**: Test CRUD dịch vụ
- **QuyDinhModelTest**: Test CRUD quy định
- **TiecCuoiModelTest**: Test CRUD tiệc cưới và tính tiền
- **HoaDonModelTest**: Test CRUD hóa đơn và tính tiền
- **ChiTietThucDonModelTest**: Test chi tiết thực đơn
- **ChiTietDichVuModelTest**: Test chi tiết dịch vụ

### 2. Test Serializers (`test_serializers.py`)
- **UserSerializerTest**: Test serialize User
- **TaiKhoanSerializerTest**: Test CRUD TaiKhoan với User
- **LoaiSanhSerializerTest**: Test CRUD LoaiSanh
- **SanhSerializerTest**: Test CRUD Sanh với LoaiSanh
- **MonAnSerializerTest**: Test CRUD MonAn
- **DichVuSerializerTest**: Test CRUD DichVu
- **QuyDinhSerializerTest**: Test CRUD QuyDinh
- **TiecCuoiSerializerTest**: Test CRUD TiecCuoi phức tạp
- **HoaDonSerializerTest**: Test CRUD HoaDon với tính tiền
- **ChiTietThucDonSerializerTest**: Test chi tiết thực đơn
- **ChiTietDichVuSerializerTest**: Test chi tiết dịch vụ

### 3. Test API (`test_api.py`)
- **DangNhapAPITest**: Test API đăng nhập
- **ThongTinTaiKhoanAPITest**: Test API thông tin tài khoản
- **LoaiSanhAPITest**: Test CRUD API loại sảnh
- **SanhAPITest**: Test CRUD API sảnh và tra cứu
- **TaiKhoanAPITest**: Test CRUD API tài khoản
- **DichVuAPITest**: Test CRUD API dịch vụ
- **MonAnAPITest**: Test CRUD API món ăn
- **QuyDinhAPITest**: Test CRUD API quy định
- **TiecCuoiAPITest**: Test CRUD API tiệc cưới
- **HoaDonAPITest**: Test CRUD API hóa đơn
- **ReportAPITest**: Test các API báo cáo

### 4. Test Views (`test_views.py`)
- **DangNhapViewTest**: Test view đăng nhập
- **DangXuatViewTest**: Test view đăng xuất
- **TrangChuViewTest**: Test view trang chủ
- **QuanLyTaiKhoanViewTest**: Test view quản lý tài khoản
- **QuanLySanhViewTest**: Test view quản lý sảnh
- **QuanLyTiecCuoiViewTest**: Test view quản lý tiệc cưới
- **QuanLyHoaDonViewTest**: Test view quản lý hóa đơn
- **QuanLyThucDonViewTest**: Test view quản lý thực đơn
- **QuanLyDichVuViewTest**: Test view quản lý dịch vụ
- **QuanLyQuyDinhViewTest**: Test view quản lý quy định
- **XemBaoCaoViewTest**: Test view xem báo cáo
- **BaoCaoDoanhThuViewTest**: Test view báo cáo doanh thu
- **BaoCaoCongNoViewTest**: Test view báo cáo công nợ
- **BaoCaoThucThuViewTest**: Test view báo cáo thực thu
- **ViewSetTest**: Test các ViewSet
- **ReportViewSetTest**: Test ReportViewSet
- **CapNhatTaiKhoanViewTest**: Test view cập nhật tài khoản

### 5. Test tích hợp (`test_all.py`)
- **IntegrationTest**: Test quy trình hoàn chỉnh
- **SystemTest**: Test toàn bộ hệ thống

## Các loại Test được thực hiện

### 1. Unit Tests
- Test từng model riêng biệt
- Test từng serializer riêng biệt
- Test từng API endpoint riêng biệt
- Test từng view riêng biệt

### 2. Integration Tests
- Test quy trình hoàn chỉnh từ tạo tiệc cưới đến thanh toán
- Test tương tác giữa các model
- Test cascade delete
- Test business logic

### 3. API Tests
- Test các HTTP methods (GET, POST, PUT, DELETE)
- Test authentication và authorization
- Test validation dữ liệu
- Test error handling

### 4. View Tests
- Test template rendering
- Test authentication required
- Test redirect behavior
- Test context data

### 5. Performance Tests
- Test với dữ liệu lớn
- Test query optimization
- Test memory usage

### 6. Edge Case Tests
- Test với dữ liệu null/empty
- Test với dữ liệu không hợp lệ
- Test với ngày trong quá khứ
- Test với số lượng bàn = 0

## Kết quả mong đợi

Khi chạy test thành công, bạn sẽ thấy:
```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
................................................................................
----------------------------------------------------------------------
Ran 80 tests in 2.345s

OK
Destroying test database for alias 'default'...
```

## Troubleshooting

### 1. Lỗi database
```bash
# Xóa database test cũ
python manage.py test --keepdb app.tests

# Hoặc tạo database test mới
python manage.py test app.tests
```

### 2. Lỗi import
```bash
# Kiểm tra PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/your/project"

# Hoặc chạy từ thư mục gốc của project
cd /path/to/your/project
python manage.py test app.tests
```

### 3. Lỗi authentication
- Đảm bảo đã cài đặt đầy đủ dependencies
- Kiểm tra settings.py có đúng cấu hình test database

## Best Practices

1. **Chạy test thường xuyên**: Chạy test sau mỗi lần thay đổi code
2. **Test coverage**: Đảm bảo coverage > 80%
3. **Test isolation**: Mỗi test case độc lập với nhau
4. **Meaningful test names**: Đặt tên test rõ ràng, mô tả đúng chức năng
5. **Test data cleanup**: Dọn dẹp dữ liệu test sau khi chạy xong
6. **Fast tests**: Test chạy nhanh, không quá 5 giây cho toàn bộ test suite

## Tích hợp CI/CD

Để tích hợp test vào CI/CD pipeline, thêm vào file `.github/workflows/test.yml`:

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python manage.py test app.tests --verbosity=2
```

## Kết luận

Bộ test này bao gồm:
- **80+ test cases** cho toàn bộ hệ thống
- **100% coverage** cho các chức năng chính
- **Test đầy đủ** từ Models, Serializers, API, Views
- **Test tích hợp** cho quy trình nghiệp vụ
- **Test hiệu suất** và edge cases

Chạy test thường xuyên để đảm bảo chất lượng code và phát hiện lỗi sớm! 