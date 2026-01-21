# -*- coding: utf-8 -*-
from odoo import api, models, fields

class GoiDien(models.Model):
    _name = "goi_dien"
    _description = "Gọi điện khách hàng"
    _inherits = {'tuong_tac': 'tuong_tac_id'}

    tuong_tac_id = fields.Many2one(
        'tuong_tac',
        required=True,
        ondelete='cascade'
    )

    thoi_luong_phut = fields.Integer(
        string="Thời lượng gọi (phút)"
    )

    ket_qua_goi = fields.Selection([
        ('khong_nghe', 'Không nghe máy'),
        ('da_goi', 'Đã trao đổi'),
        ('hen_goi_lai', 'Hẹn gọi lại'),
    ], string="Kết quả gọi điện")

    
    @api.onchange('khach_hang_id')
    def _onchange_khach_hang(self):
        self.nhan_vien_id = False
        self.cong_viec_id = False
        
    @api.onchange('nhan_vien_id', 'khach_hang_id')
    def _onchange_nhan_vien(self):
        self.cong_viec_id = False
        return {
            'domain': {
                'cong_viec_id': [
                    ('nhan_vien_id', '=', self.nhan_vien_id.id),
                    ('khach_hang_id', '=', self.khach_hang_id.id),
                ]
            }
        }