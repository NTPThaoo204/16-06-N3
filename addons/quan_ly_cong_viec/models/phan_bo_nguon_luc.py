from odoo import models, fields

class PhanBoNguonLuc(models.Model):
    _name = 'phan_bo_nguon_luc'
    _description = 'Phân bổ nguồn lực (tạm)'

    name = fields.Char()
