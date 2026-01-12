from odoo import models, fields
class TuongTac(models.Model):
    _name = "tuong_tac"
    _description = "Tương tác khách hàng"
    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng")
    noi_dung = fields.Text(string="Nội dung")