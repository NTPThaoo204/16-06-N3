from odoo import models, fields

class LichHen(models.Model):
    _name = "lich_hen"
    _description = "Lịch hẹn"

    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng")
    ghi_chu = fields.Text(string="Ghi chú")

    cong_viec_id = fields.Many2one(
        'cong_viec',
        string="Công việc thực hiện lịch hẹn"
    )
