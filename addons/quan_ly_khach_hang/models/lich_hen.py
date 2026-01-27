# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LichHen(models.Model):
    _name = "lich_hen"
    _description = "Lịch hẹn khách hàng"
    _inherits = {'tuong_tac': 'tuong_tac_id'}

    tuong_tac_id = fields.Many2one(
        'tuong_tac',
        required=True,
        ondelete='cascade'
    )

    dia_diem = fields.Char(string="Địa điểm")

    trang_thai = fields.Selection(
        [
            ('sap_dien_ra', 'Sắp diễn ra'),
            ('da_hoan_thanh', 'Đã hoàn thành'),
            ('huy', 'Hủy'),
        ],
        string="Trạng thái",
        default='sap_dien_ra'
    )

    cong_viec_id = fields.Many2one(
        'cong_viec',
        string="Công việc phát sinh",
        readonly=True,
        ondelete='set null'
    )

    # MAP TRẠNG THÁI LỊCH HẸN → CÔNG VIỆC
    def _map_trang_thai_cong_viec(self):
        self.ensure_one()
        return {
            'sap_dien_ra': 'dang_thuc_hien',
            'da_hoan_thanh': 'hoan_thanh',
            'huy': 'huy_bo',
        }.get(self.trang_thai, 'moi')

    # TẠO CÔNG VIỆC TỪ LỊCH HẸN
    def _tao_cong_viec_tu_lich_hen(self):
        for rec in self:
            if rec.cong_viec_id:
                continue

            cong_viec = self.env['cong_viec'].create({
                'ten_cong_viec': f"Lịch hẹn KH {rec.khach_hang_id.name}",
                'mo_ta': f"Hẹn gặp tại {rec.dia_diem or 'chưa xác định'}",
                'ngay_bat_dau': (
                    rec.ngay_tuong_tac.date()
                    if rec.ngay_tuong_tac
                    else fields.Date.today()
                ),
                'khach_hang_id': rec.khach_hang_id.id,
                'nhan_vien_id': rec.nhan_vien_id.id if rec.nhan_vien_id else False,
                'nguon_phat_sinh': 'lich_hen',
                'trang_thai': rec._map_trang_thai_cong_viec(),
            })

            rec.cong_viec_id = cong_viec.id

            # BÁO CÁO TIẾN ĐỘ BAN ĐẦU
            if rec.trang_thai == 'da_hoan_thanh':
                tien_do = 100
                noi_dung = "Hoàn thành lịch"
            elif rec.trang_thai == 'huy':
                tien_do = 0
                noi_dung = "Khách hàng hủy lịch"
            else:
                tien_do = 20
                noi_dung = "Lịch sắp diễn ra"

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

        # Tạo công việc
        record._tao_cong_viec_tu_lich_hen()

        # Cập nhật trạng thái khách hàng
        if record.khach_hang_id and record.trang_thai:
            record.khach_hang_id.cap_nhat_trang_thai_tu_tuong_tac(
                'lich_hen',
                record.trang_thai
            ) 

        return record

    # GHI BÁO CÁO THEO TRẠNG THÁI
    def _ghi_bao_cao_tu_trang_thai(self):
        for rec in self:
            if not rec.cong_viec_id:
                continue

            if rec.trang_thai == 'sap_dien_ra':
                tien_do = 20
                noi_dung = "Lịch sắp diễn ra"
            elif rec.trang_thai == 'da_hoan_thanh':
                tien_do = 100
                noi_dung = "Hoàn thành lịch"
            elif rec.trang_thai == 'huy':
                tien_do = 0
                noi_dung = "Khách hàng hủy lịch"
            else:
                continue

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
                        'lich_hen',
                        rec.trang_thai
                    )

        return res

    # UNLINK
    def unlink(self):
        for rec in self:
            if rec.cong_viec_id:
                rec.cong_viec_id.unlink()
        return super().unlink()    