from odoo import models, fields

class KhachHang(models.Model):
    _name = 'khach_hang'
    _description = 'Khách hàng'

    name = fields.Char(string='Tên khách hàng', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Điện thoại')
    ghi_chu = fields.Text(string='Ghi chú')
