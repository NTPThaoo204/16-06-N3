# -*- coding: utf-8 -*-
from odoo import api, models, fields


class TuongTac(models.Model):
    _name = "tuong_tac"
    _description = "Tương tác khách hàng"

    khach_hang_id = fields.Many2one(
        'khach_hang',
        string="Khách hàng",
        required=True
    )

    cong_viec_id = fields.Many2one(
        'cong_viec',
        string="Công việc liên quan"
    )

    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string="Nhân viên phụ trách"
    )

    ngay_tuong_tac = fields.Datetime(
        string="Ngày tương tác",
        default=fields.Datetime.now
    )

    ghi_chu = fields.Text(string="Ghi chú")

