---
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![GitLab](https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)



# 1. Giao diện khách hàng
<img width="1866" height="603" alt="image" src="https://github.com/user-attachments/assets/8e0ae998-c6bf-4ee9-bd2b-8ec3dafa1121" />

# 2. Giao diện tương tác
<img width="1866" height="406" alt="image" src="https://github.com/user-attachments/assets/fb6d7eae-abe2-4253-ad64-8fcef6ff521c" />
<img width="1866" height="367" alt="image" src="https://github.com/user-attachments/assets/c3653519-4069-4d93-85fd-c5fc6c07960e" />
<img width="1866" height="336" alt="image" src="https://github.com/user-attachments/assets/7db8c655-b018-4389-a0c0-dc1ad4acaf33" />

# 3. Giao diện công việc
<img width="1866" height="1003" alt="image" src="https://github.com/user-attachments/assets/0e7c5f50-ca2c-4aef-9bda-85116db886fb" />

# 4. Giao diện báo cáo tiến độ
<img width="1866" height="705" alt="image" src="https://github.com/user-attachments/assets/9ff0bdeb-1b66-4fcf-9a5f-d165b9ad3134" />

# 5. Giao diện một số biểu đồ
<img width="1866" height="1002" alt="image" src="https://github.com/user-attachments/assets/c390f228-da75-4c29-ae7d-63c9a3f45830" />
<img width="1866" height="997" alt="image" src="https://github.com/user-attachments/assets/aa1f7c4f-3006-48a6-8e2c-f6757b6b9f8a" />
<img width="1866" height="997" alt="image" src="https://github.com/user-attachments/assets/081e863c-ea37-4b98-a713-79cbdc153205" />
<img width="1866" height="997" alt="image" src="https://github.com/user-attachments/assets/05274add-1940-469a-9040-45b1de11e4ae" />


# 1. Clone project
```
git clone https://github.com/NTPThaoo204/16-06-N3.git
```
```
cd 16-06-N3
```
```
code .
```


# 2. Cài đặt các thư viện cần thiết
```
sudo apt-get update
```
```
sudo apt-get install -y \
  libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev \
  python3.10-distutils python3.10-dev build-essential libffi-dev \
  zlib1g-dev python3.10-venv libpq-dev
```
Kiểm tra Python 3.10 có sẵn:
```
python3.10 --version
```


# 3. Khởi tạo môi trường ảo
```
python3.10 -m venv ./venv
```

## 3.1. Kích hoạt môi trường ảo
```
source venv/bin/activate
```

## 3.2. Cài requirements
```
pip3 install -r requirements.txt
```

# 4. Setup database bằng Docker Compose

## 4.1. Bảo đảm Docker chạy được trong Ubuntu
```
docker ps
```
```
docker compose version
```

## 4.2. Chạy database
```
docker compose up -d
```

## 4.3. Kiểm tra container DB đang chạy
```
docker ps
```


# 5. Tạo file cấu hình odoo.conf

Tạo tệp **odoo.conf** có nội dung như sau:
```
[options]
addons_path = addons
db_host = localhost
db_password = matkhau
db_user = odoo
db_port = 5432
xmlrpc_port = 8040
```

# 6. Chạy odoo
```
python3 odoo-bin.py -c odoo.conf -u all
```

Người sử dụng truy cập theo đường dẫn _http://localhost:8040/_ để đăng nhập vào hệ thống.

# 7. Tham khảo

https://github.com/hieuht09/TTDN-15-02-N1.git

https://github.com/FIT-DNU/Business-Internship.git
