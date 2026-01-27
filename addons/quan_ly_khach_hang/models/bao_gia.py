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

    tong_tien = fields.Float(
        string="Tổng tiền",
        digits=(16, 0)
    )

    trang_thai = fields.Selection(
        [
            ('da_gui', 'Đã gửi'),
            ('dong_y', 'Đồng ý'),
            ('tu_choi', 'Từ chối'),
        ],
        string="Trạng thái"
    )

    cong_viec_id = fields.Many2one(
        'cong_viec',
        string="Công việc phát sinh",
        readonly=True,
        ondelete='set null'
    )

    # MAP TRẠNG THÁI BÁO GIÁ → CÔNG VIỆC
    def _map_trang_thai_cong_viec(self):
        self.ensure_one()
        return {
            'da_gui': 'dang_thuc_hien',
            'dong_y': 'hoan_thanh',
            'tu_choi': 'huy_bo',
        }.get(self.trang_thai, 'moi')
    
    # TẠO CÔNG VIỆC 
    def _tao_cong_viec_tu_bao_gia(self):
        for rec in self:
            if rec.cong_viec_id:
                continue

            cong_viec = self.env['cong_viec'].create({
                'ten_cong_viec': f"Báo giá KH {rec.khach_hang_id.name}",
                'mo_ta': 'Tạo từ tương tác báo giá',
                'ngay_bat_dau': (
                    rec.ngay_tuong_tac.date()
                    if rec.ngay_tuong_tac
                    else fields.Date.today()
                ),
                'khach_hang_id': rec.khach_hang_id.id,
                'nhan_vien_id': rec.nhan_vien_id.id if rec.nhan_vien_id else False,
                'nguon_phat_sinh': 'bao_gia',
            })

            rec.cong_viec_id = cong_viec.id

            # TẠO BÁO CÁO TIẾN ĐỘ BAN ĐẦU
            tien_do = 0
            noi_dung = "Khởi tạo báo giá"

            if rec.trang_thai == 'da_gui':
                tien_do = 50
                noi_dung = "Đã gửi báo giá cho khách hàng"
            elif rec.trang_thai == 'dong_y':
                tien_do = 100
                noi_dung = "Khách hàng đồng ý báo giá"
            elif rec.trang_thai == 'tu_choi':
                tien_do = 0
                noi_dung = "Khách hàng từ chối báo giá"

            self.env['bao_cao_tien_do'].create({
                'cong_viec_id': cong_viec.id,
                'nhan_vien_id': cong_viec.nhan_vien_id.id,
                'tien_do': tien_do,
                'noi_dung': noi_dung,
                'ngay_bao_cao': fields.Date.today(),
            })

    # CREATE 
    @api.model
    def create(self, vals):
        record = super().create(vals)

        # TẠO CÔNG VIỆC TỪ BÁO GIÁ
        record._tao_cong_viec_tu_bao_gia()

        # CẬP NHẬT TRẠNG THÁI KHÁCH HÀNG
        if record.khach_hang_id and record.trang_thai:
            record.khach_hang_id.cap_nhat_trang_thai_tu_tuong_tac(
                'bao_gia',
                record.trang_thai
            )

        return record

    # ONCHANGE TRẠNG THÁI
    @api.onchange('trang_thai')
    def _onchange_trang_thai(self):
        for rec in self:
            if not rec.cong_viec_id:
                continue

            tien_do = None
            noi_dung = ""

            if rec.trang_thai == 'da_gui':
                tien_do = 50
                noi_dung = "Đã gửi báo giá"
            elif rec.trang_thai == 'dong_y':
                tien_do = 100
                noi_dung = "Khách hàng đồng ý báo giá"
            elif rec.trang_thai == 'tu_choi':
                tien_do = 0
                noi_dung = "Khách hàng từ chối báo giá"

            if tien_do is not None:
                self.env['bao_cao_tien_do'].create({
                    'cong_viec_id': rec.cong_viec_id.id,
                    'nhan_vien_id': rec.cong_viec_id.nhan_vien_id.id,
                    'tien_do': tien_do,
                    'noi_dung': noi_dung,
                    'ngay_bao_cao': fields.Date.today(),
                })
    
    # WRITE
    def write(self, vals):
        res = super().write(vals)

        if 'trang_thai' in vals:
            for rec in self:
                # Ghi báo cáo tiến độ
                rec._ghi_bao_cao_tu_trang_thai()

                # Cập nhật trạng thái khách hàng
                if rec.khach_hang_id:
                    rec.khach_hang_id.cap_nhat_trang_thai_tu_tuong_tac(
                        'bao_gia',
                        rec.trang_thai
                    )
        return res
    
    # UNLINK
    def unlink(self):
        for rec in self:
            if rec.cong_viec_id:
                rec.cong_viec_id.unlink()
        return super().unlink()