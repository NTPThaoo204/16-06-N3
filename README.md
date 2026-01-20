---
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![GitLab](https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)


# 1. Giao diện khách hàng
<img width="1850" height="441" alt="image" src="https://github.com/user-attachments/assets/e9933362-befc-467c-b461-3fee335ebf82" />

# 2. Giao diện công việc
<img width="1850" height="817" alt="image" src="https://github.com/user-attachments/assets/068d417d-8550-4001-b13b-5325b0389e6b" />

# 3. Giao diện báo cáo tiến độ
<img width="1864" height="834" alt="image" src="https://github.com/user-attachments/assets/6fadf584-99c2-42dc-853d-29ddac1d95f1" />

# 4. Giao diện một số biểu đồ
<img width="1864" height="998" alt="image" src="https://github.com/user-attachments/assets/a8730899-75d3-4fe6-b293-10af1b24f6d4" />
<img width="1864" height="998" alt="image" src="https://github.com/user-attachments/assets/c83f101b-4b81-48e9-8e7d-ecdffa7c5ac8" />



# 1. Clone project
```
git clone https://github.com/NTPThaoo204/16-06-N3.git
```
```
cd odoo-fitdnu
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
