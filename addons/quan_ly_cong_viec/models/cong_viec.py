# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CongViec(models.Model):
    _name = "cong_viec"
    _description = "Công việc"
    _rec_name = "ten_cong_viec"
    _order = "ngay_bat_dau, ma_cong_viec"
    
    ma_cong_viec = fields.Char(string="Mã công việc", required=True, index=True)
    ten_cong_viec = fields.Char(string="Tên công việc", required=True)
    mo_ta = fields.Text(string="Mô tả")
    
    # Thời gian
    ngay_bat_dau = fields.Date(string="Ngày bắt đầu", required=True)
    ngay_ket_thuc = fields.Date(string="Ngày kết thúc")
    
    # Quan hệ
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên")
    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", required=True)

    # Các trường quan hệ tham chiếu ngược
    bao_cao_tien_do_ids = fields.One2many('bao_cao_tien_do', 'cong_viec_id', string="Báo cáo tiến độ")
    # Thông tin tiến độ
    tien_do = fields.Integer(string="Tiến độ (%)", compute="_compute_tien_do", store=True, readonly=True)

    # Độ ưu tiên, trạng thái
    do_uu_tien = fields.Selection([
        ('thap', 'Thấp'),
        ('trung_binh', 'Trung bình'),
        ('cao', 'Cao'),
        ('rat_cao', 'Rất cao')
    ], string="Độ ưu tiên", default='trung_binh')
    
    trang_thai = fields.Selection([
        ('moi', 'Mới'),
        ('dang_thuc_hien', 'Đang thực hiện'),
        ('tam_dung', 'Tạm dừng'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy_bo', 'Hủy bỏ')
    ], string="Trạng thái", default='moi', tracking=True)
    
    nguon_phat_sinh = fields.Selection([
       ('bao_gia', 'Báo giá'),
        ('lich_hen', 'Lịch hẹn'),
        ('tuong_tac', 'Tương tác'),
        ('khac', 'Khác'),
    ], string="Nguồn phát sinh", default='khac')

    _sql_constraints = [
        ('ma_cong_viec_unique', 'unique(ma_cong_viec)', 'Mã công việc phải là duy nhất!'),
    ]
   
    @api.depends('bao_cao_tien_do_ids.tien_do', 'bao_cao_tien_do_ids.ngay_bao_cao')
    def _compute_tien_do(self):
        for record in self:
            if record.bao_cao_tien_do_ids:
                bao_cao_moi_nhat = record.bao_cao_tien_do_ids.sorted(
                   key=lambda r: r.ngay_bao_cao or fields.Date.today(),
                   reverse=True
                )[0]
                record.tien_do = bao_cao_moi_nhat.tien_do
            else:
                record.tien_do = 0

    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_dates(self):
        for record in self:
            if record.ngay_ket_thuc and record.ngay_bat_dau > record.ngay_ket_thuc:
                raise ValidationError(_("Ngày bắt đầu không thể sau ngày kết thúc!"))