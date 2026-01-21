# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LichHen(models.Model):
    _name = "lich_hen"
    _description = "Lịch hẹn khách hàng"
    _inherits = {'tuong_tac': 'tuong_tac_id'}

    tuong_tac_id = fields.Many2one(
        'tuong_tac',
        required=True,
        ondelete='cascade'
    )

    thoi_gian_bat_dau = fields.Datetime(required=True)
    thoi_gian_ket_thuc = fields.Datetime(required=True)
    dia_diem = fields.Char()
    trang_thai = fields.Selection([
        ('sap_dien_ra', 'Sắp diễn ra'),
        ('da_hoan_thanh', 'Đã hoàn thành'),
        ('huy', 'Hủy'),
    ], string="Trạng thái", default='sap_dien_ra')

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
    
    @api.constrains('thoi_gian_bat_dau', 'thoi_gian_ket_thuc')
    def _check_thoi_gian(self):
        for rec in self:
            if rec.thoi_gian_ket_thuc < rec.thoi_gian_bat_dau:
                raise ValidationError(
                    "Thời gian kết thúc phải sau thời gian bắt đầu!"
                )