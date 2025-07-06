# Hướng Dẫn Chạy Test

## Tổng Quan

Bộ test này bao gồm các test cases toàn diện cho hệ thống quản lý tiệc cưới, bao gồm:

- **Test Models**: Kiểm tra các model và business logic
- **Test Serializers**: Kiểm tra validation và data transformation
- **Test API**: Kiểm tra các API endpoints
- **Test Views**: Kiểm tra các Django views
- **Test Integration**: Kiểm tra tích hợp toàn bộ hệ thống

## Cấu Trúc Thư Mục

```
app/tests/
├── test_models.py          # Test các model
├── test_serializers.py     # Test các serializer
├── test_api.py            # Test các API endpoints
├── test_views.py          # Test các Django views
├── test_all.py            # Test tích hợp/system test
├── conftest.py            # Pytest fixtures (nâng cao)
└── README.md              # File này
```

## Cách Chạy Test

### 1. Chạy Tất Cả Test

```bash
python manage.py test
```

### 2. Chạy Từng File Test

```bash
# Test models
python manage.py test app.tests.test_models

# Test serializers
python manage.py test app.tests.test_serializers

# Test API
python manage.py test app.tests.test_api

# Test views
python manage.py test app.tests.test_views

# Test tích hợp
python manage.py test app.tests.test_all
```

### 3. Chạy Test Cụ Thể

```bash
# Chạy test class cụ thể
python manage.py test app.tests.test_models.TaiKhoanModelTest

# Chạy test method cụ thể
python manage.py test app.tests.test_models.TaiKhoanModelTest.test_tai_khoan_creation
```

### 4. Chạy Test Với Coverage

```bash
# Cài đặt coverage (nếu chưa có)
pip install coverage

# Chạy test với coverage
coverage run --source='.' manage.py test

# Xem báo cáo coverage
coverage report

# Tạo báo cáo HTML
coverage html
```

## Các Loại Test

### 1. Model Tests (`test_models.py`)

Kiểm tra:
- Tạo mới, đọc, cập nhật, xóa (CRUD) các model
- Business logic và validation
- Relationships giữa các model
- Cascade delete
- Choices và constraints

**Ví dụ:**
```python
def test_tai_khoan_creation(self):
    """Test tạo mới TaiKhoan"""
    self.assertEqual(self.tai_khoan.user.username, 'testuser')
    self.assertEqual(self.tai_khoan.vaitro, 'admin')
```

### 2. Serializer Tests (`test_serializers.py`)

Kiểm tra:
- Validation dữ liệu
- Data transformation
- Create và update operations
- Custom fields và methods

**Ví dụ:**
```python
def test_tai_khoan_serializer_create_success(self):
    """Test tạo mới TaiKhoan thành công"""
    data = {
        'username': 'newuser',
        'password': 'newpass123',
        'hovaten': 'New User'
    }
    serializer = TaiKhoanSerializer(data=data)
    self.assertTrue(serializer.is_valid())
```

### 3. API Tests (`test_api.py`)

Kiểm tra:
- HTTP status codes
- Response data structure
- Authentication và authorization
- Error handling
- Search và pagination

**Ví dụ:**
```python
def test_login_success(self):
    """Test đăng nhập thành công"""
    response = self.client.post('/api/dangnhap/', {
        'username': 'testuser',
        'password': 'testpass123'
    }, format='json')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data['success'])
```

### 4. View Tests (`test_views.py`)

Kiểm tra:
- Template rendering
- Authentication redirects
- Form submission
- Context data

**Ví dụ:**
```python
def test_quanlytaikhoan_authenticated(self):
    """Test truy cập trang quản lý tài khoản khi đã đăng nhập"""
    self.client.login(username='testuser', password='testpass123')
    response = self.client.get(reverse('quanlytaikhoan'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'app/quanlytaikhoan.html')
```

### 5. Integration Tests (`test_all.py`)

Kiểm tra:
- End-to-end workflows
- Data consistency
- Performance với dữ liệu lớn
- Error handling toàn hệ thống

**Ví dụ:**
```python
def test_complete_workflow(self):
    """Test quy trình hoàn chỉnh từ đăng nhập đến tạo tiệc cưới"""
    # 1. Đăng nhập
    # 2. Tạo tiệc cưới
    # 3. Tạo hóa đơn
    # 4. Kiểm tra tính nhất quán
```

## Test Data

Mỗi test class có phương thức `setUp()` để tạo dữ liệu test cần thiết:

```python
def setUp(self):
    """Thiết lập dữ liệu test"""
    self.user = User.objects.create_user(
        username='testuser',
        password='testpass123'
    )
    self.tai_khoan = TaiKhoan.objects.create(
        user=self.user,
        hovaten='Test User',
        vaitro='admin'
    )
```

## Best Practices

### 1. Test Naming
- Tên test method phải mô tả rõ ràng chức năng được test
- Sử dụng format: `test_<functionality>_<scenario>`

### 2. Test Isolation
- Mỗi test phải độc lập, không phụ thuộc vào test khác
- Sử dụng `setUp()` và `tearDown()` để quản lý test data

### 3. Assertions
- Sử dụng assertions cụ thể và có ý nghĩa
- Test cả positive cases và negative cases

### 4. Documentation
- Viết docstring cho mỗi test method
- Giải thích mục đích và logic của test

## Troubleshooting

### 1. Database Issues
```bash
# Reset database test
python manage.py test --keepdb
```

### 2. Import Errors
```bash
# Kiểm tra PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/your/project"
```

### 3. Coverage Issues
```bash
# Xóa cache coverage
coverage erase
```

## Kết Quả Test

### 1. Test Results
```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...................
----------------------------------------------------------------------
Ran 17 tests in 2.345s

OK
Destroying test database for alias 'default'...
```

### 2. Coverage Report
```
Name                           Stmts   Miss  Cover
--------------------------------------------------
app/__init__.py                    0      0   100%
app/admin.py                      35      0   100%
app/api.py                        73      0   100%
app/models.py                    142      0   100%
app/serializers.py               297      0   100%
app/views.py                     705      0   100%
--------------------------------------------------
TOTAL                           1252      0   100%
```

## Lưu Ý

1. **Test Database**: Django tự động tạo database test riêng biệt
2. **Fixtures**: Có thể sử dụng fixtures để load dữ liệu test
3. **Mocking**: Sử dụng unittest.mock cho external dependencies
4. **Performance**: Test hiệu suất với dữ liệu lớn
5. **Security**: Test authentication và authorization

## Báo Cáo

Khi chạy test cho báo cáo, hãy:

1. **Screenshot** kết quả test
2. **Ghi lại** coverage percentage
3. **Document** các test cases quan trọng
4. **Giải thích** ý nghĩa của từng loại test
5. **Đánh giá** chất lượng test coverage 