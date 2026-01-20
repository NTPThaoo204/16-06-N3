from odoo import models, fields

class TuongTac(models.Model):
    _name = "tuong_tac"
    _description = "Tương tác khách hàng"

    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng")
    ghi_chu = fields.Text(string="Ghi chú")
    
    cong_viec_id = fields.Many2one(
        'cong_viec',
        string="Công việc xử lý"
    )
