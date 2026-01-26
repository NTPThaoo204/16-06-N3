# -*- coding: utf-8 -*-
{
    'name': "quan_ly_khach_hang",

    'summary': """
        Module quản lý khách hàng và công việc tích hợp với nhân sự""",

    'description': """
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Project Management',
    'version': '0.1',

    # Quan trọng: Phải phụ thuộc vào module quan_ly_nhan_su
    'depends': ['base', 'quan_ly_nhan_su', 'quan_ly_cong_viec'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/dashboard.xml',
        'views/khach_hang.xml',
        'views/bao_gia.xml',
        'views/lich_hen.xml',
        'views/goi_dien.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
