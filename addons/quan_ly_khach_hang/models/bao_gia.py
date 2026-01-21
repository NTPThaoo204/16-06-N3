# -*- coding: utf-8 -*-
from odoo import api, models, fields

class BaoGia(models.Model):
    _name = "bao_gia"
    _description = "Báo giá khách hàng"
    _inherits = {'tuong_tac': 'tuong_tac_id'}

    tuong_tac_id = fields.Many2one(
        'tuong_tac',
        required=True,
        ondelete='cascade'
    )

    so_bao_gia = fields.Char(
        string="Số báo giá",
        required=True
    )

    ngay_bao_gia = fields.Date(
        string="Ngày báo giá",
        default=fields.Date.today
    )

    tong_tien = fields.Float(
        string="Tổng tiền"
    )
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('da_gui', 'Đã gửi'),
        ('dong_y', 'Đồng ý'),
        ('tu_choi', 'Từ chối'),
    ], default='nhap')

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