# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BaoCaoTienDo(models.Model):
    _name = "bao_cao_tien_do"
    _description = "Báo cáo tiến độ công việc"
    _rec_name = "cong_viec_id"
    _order = "ngay_bao_cao desc"

    cong_viec_id = fields.Many2one(
        'cong_viec',
        string="Công việc",
        required=True,
        ondelete='cascade'
    )

    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string="Nhân viên",
        required=True
    )

    ngay_bao_cao = fields.Date(
        string="Ngày báo cáo",
        required=True,
        default=fields.Date.today
    )

    noi_dung = fields.Text(
        string="Nội dung báo cáo",
        required=True
    )

    tien_do = fields.Integer(
        string="Tiến độ (%)",
        required=True,
        digits=(3, 0),
        help="Đánh giá phần trăm hoàn thành của công việc"
    )

    # VẤN ĐỀ – GIẢI PHÁP
    van_de_phat_sinh = fields.Text(
        string="Vấn đề phát sinh"
    )

    giai_phap = fields.Text(
        string="Giải pháp đề xuất"
    )

    # ĐÍNH KÈM
    file_dinh_kem = fields.Binary(
        string="File đính kèm"
    )

    ten_file = fields.Char(
        string="Tên file"
    )

    # THÔNG TIN LIÊN QUAN
    ten_cong_viec = fields.Char(
        related='cong_viec_id.ten_cong_viec',
        string="Tên công việc",
        store=True,
        readonly=True
    )

    # VALIDATION
    @api.constrains('tien_do')
    def _check_tien_do(self):
        for record in self:
            if record.tien_do < 0 or record.tien_do > 100:
                raise ValidationError(
                    _("Tiến độ phải nằm trong khoảng từ 0 đến 100!")
                )

    @api.constrains('tien_do', 'cong_viec_id')
    def _check_tien_do_tang_dan(self):
        for rec in self:
            bc_cu = self.search(
                [
                    ('cong_viec_id', '=', rec.cong_viec_id.id),
                    ('id', '!=', rec.id)
                ],
                order='ngay_bao_cao desc',
                limit=1
            )
            if bc_cu and rec.tien_do < bc_cu.tien_do:
                raise ValidationError(
                    _("Tiến độ không được nhỏ hơn báo cáo trước đó!")
                )

    # ONCHANGE 
    @api.onchange('cong_viec_id')
    def _onchange_cong_viec_id(self):
        if self.cong_viec_id and self.cong_viec_id.nhan_vien_id:
            self.nhan_vien_id = self.cong_viec_id.nhan_vien_id.id
