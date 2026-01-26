from odoo import models, fields

class KhachHang(models.Model):
    _name = 'khach_hang'
    _description = 'Khách hàng'

    name = fields.Char(string='Tên khách hàng', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Điện thoại')
    ghi_chu = fields.Text(string='Ghi chú')

    trang_thai = fields.Selection([
        ('moi', 'Khách hàng mới'),
        ('dang_cham_soc', 'Đang chăm sóc'),
        ('da_chot', 'Đã chốt'),
        ('da_hủy', 'Đã hủy'),
    ], string='Trạng thái', default='moi')

    create_date = fields.Datetime(
        string="Ngày tạo",
        readonly=True
    )
    
    nhan_vien_id = fields.Many2one(
        'res.users',
        string='Nhân viên phụ trách'
    )
