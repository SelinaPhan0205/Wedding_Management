# Wedding_Management
# Hệ thống Quản lý Tiệc cưới

Đây là một hệ thống web được phát triển bằng Django để hỗ trợ quản lý các nghiệp vụ liên quan đến tổ chức tiệc cưới như: đặt sảnh, thực đơn, dịch vụ, hóa đơn và báo cáo doanh thu.

## Chức năng chính

- Quản lý sảnh tiệc: thêm, sửa, tra cứu sảnh trống theo ngày & ca
- Đặt tiệc cưới và cập nhật thông tin cô dâu chú rể
- Quản lý món ăn, dịch vụ đi kèm
- Lập hóa đơn và tính tiền phạt nếu thanh toán trễ
- Báo cáo doanh thu theo tháng, hỗ trợ xuất file Excel
- Phân quyền người dùng: Admin và Nhân viên

## Công nghệ sử dụng

- Python 3.10 + Django
- PostgreSQL
- HTML/CSS/JS + TailwindCSS
- Django REST Framework
- Chart.js, SheetJS
- Postman (kiểm thử API)
- Visual Studio Code

## Cài đặt hệ thống

1. Tạo virtual environment và cài đặt thư viện:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt

2. Cấu hình database PostgreSQL trong `settings.py`:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'tieccuoi_db',
            'USER': 'postgres',
            'PASSWORD': '123456',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

3. Tạo cơ sở dữ liệu:
   ```bash
    python manage.py makemigrations
    python manage.py migrate

4. Tạo tài khoản admin:
    ```bash
    python manage.py createsuperuser

5. Chạy server:
    ```bash
    python manage.py runserver

6. Truy cập hệ thống tại: http://127.0.0.1:8000
