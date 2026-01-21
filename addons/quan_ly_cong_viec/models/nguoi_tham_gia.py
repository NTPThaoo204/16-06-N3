from odoo import models, fields

class NguoiThamGia(models.Model):
    _name = 'nguoi_tham_gia'
    _description = 'Người tham gia công việc'

    name = fields.Char()
