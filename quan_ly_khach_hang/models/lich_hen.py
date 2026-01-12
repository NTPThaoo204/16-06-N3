from odoo import models, fields
class LichHen(models.Model):
    _name = "lich_hen"
    _description = "Lịch hẹn"
    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng")
    ngay = fields.Datetime(string="Ngày hẹn")
