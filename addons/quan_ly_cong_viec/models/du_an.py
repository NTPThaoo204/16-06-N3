from odoo import models, fields

class DuAn(models.Model):
    _name = 'du_an'
    _description = 'Dự án (tạm)'

    name = fields.Char()
