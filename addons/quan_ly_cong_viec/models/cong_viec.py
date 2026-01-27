# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CongViec(models.Model):
    _name = "cong_viec"
    _description = "Công việc"
    _rec_name = "ten_cong_viec"
    _order = "ngay_bat_dau, ma_cong_viec"

    # THÔNG TIN CƠ BẢN
    ma_cong_viec = fields.Char(
        string="Mã công việc",
        required=True,
        index=True
    )

    ten_cong_viec = fields.Char(
        string="Tên công việc",
        required=True
    )

    mo_ta = fields.Text(string="Mô tả")

    # THỜI GIAN
    ngay_bat_dau = fields.Date(
        string="Ngày bắt đầu",
        required=True
    )

    ngay_ket_thuc = fields.Date(
        string="Ngày kết thúc",
        compute="_compute_ngay_ket_thuc",
        store=True,
        readonly=True
    )

    # QUAN HỆ
    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string="Nhân viên"
    )

    khach_hang_id = fields.Many2one(
        'khach_hang',
        string="Khách hàng",
        required=True
    )

    bao_cao_tien_do_ids = fields.One2many(
        'bao_cao_tien_do',
        'cong_viec_id',
        string="Báo cáo tiến độ"
    )

    # TIẾN ĐỘ
    tien_do = fields.Integer(
        string="Tiến độ (%)",
        compute="_compute_tien_do",
        store=True,
        readonly=True
    )

    # TRẠNG THÁI & ƯU TIÊN
    do_uu_tien = fields.Selection(
        [
            ('thap', 'Thấp'),
            ('trung_binh', 'Trung bình'),
            ('cao', 'Cao'),
            ('rat_cao', 'Rất cao'),
        ],
        string="Độ ưu tiên",
        default='trung_binh'
    )

    trang_thai = fields.Selection(
        [
            ('moi', 'Mới'),
            ('dang_thuc_hien', 'Đang thực hiện'),
            ('tam_dung', 'Tạm dừng'),
            ('hoan_thanh', 'Hoàn thành'),
            ('huy_bo', 'Hủy bỏ'),
        ],
        compute="_compute_trang_thai",
        store=True,
        tracking=True
    )

    nguon_phat_sinh = fields.Selection(
        [
            ('bao_gia', 'Báo giá'),
            ('lich_hen', 'Lịch hẹn'),
            ('goi_dien', 'Gọi điện'),
            ('khac', 'Khác'),
        ],
        string="Nguồn phát sinh",
        default='khac'
    )

    # SQL CONSTRAINT
    _sql_constraints = [
        (
            'ma_cong_viec_unique',
            'unique(ma_cong_viec)',
            'Mã công việc phải là duy nhất!'
        ),
    ]

    # COMPUTE TIẾN ĐỘ (lấy báo cáo mới nhất)
    @api.depends(
        'bao_cao_tien_do_ids.tien_do',
        'bao_cao_tien_do_ids.ngay_bao_cao'
    )
    def _compute_tien_do(self):
        for rec in self:
            if rec.bao_cao_tien_do_ids:
                bc_moi_nhat = rec.bao_cao_tien_do_ids.sorted(
                    key=lambda r: r.ngay_bao_cao or fields.Date.today(),
                    reverse=True
                )[0]
                rec.tien_do = bc_moi_nhat.tien_do
            else:
                rec.tien_do = 0

    # COMPUTE TRẠNG THÁI
    @api.depends(
        'tien_do',
        'bao_cao_tien_do_ids.noi_dung',
        'bao_cao_tien_do_ids.ngay_bao_cao'
    )
    def _compute_trang_thai(self):
        for rec in self:
            if not rec.bao_cao_tien_do_ids:
                rec.trang_thai = 'moi'
                continue

            bc_moi_nhat = rec.bao_cao_tien_do_ids.sorted(
                key=lambda r: r.ngay_bao_cao or fields.Date.today(),
                reverse=True
            )[0]

            noi_dung = (bc_moi_nhat.noi_dung or '').lower()

            if 'hẹn' in noi_dung:
                rec.trang_thai = 'tam_dung'
            elif 'từ chối' in noi_dung or 'hủy' in noi_dung:
                rec.trang_thai = 'huy_bo'
            elif rec.tien_do == 100:
                rec.trang_thai = 'hoan_thanh'
            elif rec.tien_do > 0:
                rec.trang_thai = 'dang_thuc_hien'
            else:
                rec.trang_thai = 'moi'

    # COMPUTE NGÀY KẾT THÚC
    @api.depends('trang_thai')
    def _compute_ngay_ket_thuc(self):
        for rec in self:
            if rec.trang_thai in ('hoan_thanh', 'huy_bo'):
                rec.ngay_ket_thuc = rec.ngay_ket_thuc or fields.Date.today()
            else:
                rec.ngay_ket_thuc = False

    # VALIDATION
    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_dates(self):
        for rec in self:
            if rec.ngay_ket_thuc and rec.ngay_bat_dau > rec.ngay_ket_thuc:
                raise ValidationError(
                    _("Ngày bắt đầu không thể sau ngày kết thúc!")
                )

    # CREATE
    @api.model
    def create(self, vals):
        if not vals.get('ma_cong_viec'):
            while True:
                ma = self.env['ir.sequence'].next_by_code('cong_viec') or 'CV-MOI'
                if not self.search([('ma_cong_viec', '=', ma)], limit=1):
                    vals['ma_cong_viec'] = ma
                    break
        return super().create(vals)
