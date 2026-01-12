from odoo import models, fields
class BaoGia(models.Model):
    _name = "bao_gia"
    _description = "Báo giá"

    name = fields.Char(string="Số báo giá")
    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng")  # nội bộ module
    ghi_chu = fields.Text(string="Ghi chú")
