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

    trang_thai = fields.Selection(
        [
            ('khong_nghe', 'Không nghe máy'),
            ('hen_goi_lai', 'Hẹn gọi lại'),
            ('da_goi', 'Đã gọi'),
        ],
        string="Trạng thái"
    )

    cong_viec_id = fields.Many2one(
        'cong_viec',
        string="Công việc phát sinh",
        readonly=True,
        ondelete='set null'
    )

    # MAP TRẠNG THÁI GỌI ĐIỆN → CÔNG VIỆC
    def _map_trang_thai_cong_viec(self):
        self.ensure_one()
        return {
            'khong_nghe': 'dang_thuc_hien',
            'hen_goi_lai': 'tam_dung',
            'da_goi': 'hoan_thanh',
        }.get(self.trang_thai, 'moi')

    # TẠO CÔNG VIỆC TỪ GỌI ĐIỆN
    def _tao_cong_viec_tu_goi_dien(self):
        for rec in self:
            if rec.cong_viec_id:
                continue

            cong_viec = self.env['cong_viec'].create({
                'ten_cong_viec': f"Gọi điện KH {rec.khach_hang_id.name}",
                'mo_ta': "Tạo từ tương tác gọi điện",
                'ngay_bat_dau': (
                    rec.ngay_tuong_tac.date()
                    if rec.ngay_tuong_tac
                    else fields.Date.today()
                ),
                'khach_hang_id': rec.khach_hang_id.id,
                'nhan_vien_id': rec.nhan_vien_id.id if rec.nhan_vien_id else False,
                'nguon_phat_sinh': 'goi_dien',
            })

            rec.cong_viec_id = cong_viec.id

            # BÁO CÁO TIẾN ĐỘ BAN ĐẦU 
            tien_do = 0
            noi_dung = "Khởi tạo gọi điện khách hàng"

            if rec.trang_thai == 'khong_nghe':
                tien_do = 30
                noi_dung = "Gọi điện nhưng khách không nghe máy"
            elif rec.trang_thai == 'hen_goi_lai':
                tien_do = 50
                noi_dung = "Khách hàng hẹn gọi lại"
            elif rec.trang_thai == 'da_goi':
                tien_do = 100
                noi_dung = "Hoàn thành gọi điện khách hàng"

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

        # TẠO CÔNG VIỆC
        record._tao_cong_viec_tu_goi_dien()

        # CẬP NHẬT TRẠNG THÁI KHÁCH HÀNG
        if record.khach_hang_id and record.trang_thai:
            record.khach_hang_id.cap_nhat_trang_thai_tu_tuong_tac(
                'goi_dien',
                record.trang_thai
            )

        return record


    # ONCHANGE TRẠNG THÁI → GHI TIẾN ĐỘ + CẬP NHẬT CÔNG VIỆC
    @api.onchange('trang_thai')
    def _onchange_trang_thai(self):
        for rec in self:
            if not rec.cong_viec_id:
               continue

            tien_do = None
            noi_dung = ""
            trang_thai_cv = False

            if rec.trang_thai == 'khong_nghe':
                tien_do = 30
                noi_dung = "Gọi điện nhưng khách không nghe máy"
                trang_thai_cv = 'dang_thuc_hien'

            elif rec.trang_thai == 'hen_goi_lai':
                tien_do = 50
                noi_dung = "Khách hàng hẹn gọi lại"
                trang_thai_cv = 'tam_dung'

            elif rec.trang_thai == 'da_goi':
                tien_do = 100
                noi_dung = "Hoàn thành gọi điện khách hàng"
                trang_thai_cv = 'hoan_thanh'

            # GHI BÁO CÁO TIẾN ĐỘ 
            if tien_do is not None:
                self.env['bao_cao_tien_do'].create({
                    'cong_viec_id': rec.cong_viec_id.id,
                    'nhan_vien_id': rec.cong_viec_id.nhan_vien_id.id,
                    'tien_do': tien_do,
                    'noi_dung': noi_dung,
                    'ngay_bao_cao': fields.Date.today(),
                })

            # CẬP NHẬT CÔNG VIỆC 
            if trang_thai_cv:
                vals = {'trang_thai': trang_thai_cv}

                # CHỈ SET NGÀY KẾT THÚC KHI HOÀN THÀNH
                if trang_thai_cv == 'hoan_thanh':
                    vals['ngay_ket_thuc'] = fields.Date.today()

                rec.cong_viec_id.write(vals)

    # WRITE
    def write(self, vals):
        res = super().write(vals)

        if 'trang_thai' in vals:
            for rec in self:
                if rec.khach_hang_id:
                    rec.khach_hang_id.cap_nhat_trang_thai_tu_tuong_tac(
                        'goi_dien',
                        rec.trang_thai
                    )
        return res
    
    # UNLINK
    def unlink(self):
        for rec in self:
            if rec.cong_viec_id:
                rec.cong_viec_id.unlink()
        return super().unlink()