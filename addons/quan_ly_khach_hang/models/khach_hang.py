from odoo import models, fields

class KhachHang(models.Model):
    _name = 'khach_hang'
    _description = 'Khách hàng'

    name = fields.Char(string='Tên khách hàng', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Điện thoại')
    ghi_chu = fields.Text(string='Ghi chú')

    trang_thai = fields.Selection([
        ('moi', 'Khách hàng mới'),
        ('dang_cham_soc', 'Đang chăm sóc'),
        ('da_chot', 'Đã chốt'),
        ('da_huy', 'Đã hủy'),
    ], string='Trạng thái', default='moi')

    create_date = fields.Datetime(
        string="Ngày tạo",
        readonly=True
    )
    
    nhan_vien_id = fields.Many2one(
        'res.users',
        string='Nhân viên phụ trách'
    )

    # HÀM CHUNG CẬP NHẬT TRẠNG THÁI TỪ TƯƠNG TÁC
    def cap_nhat_trang_thai_tu_tuong_tac(self, loai, trang_thai_tuong_tac):
        for kh in self:
            # GỌI ĐIỆN
            if loai == 'goi_dien':
                if trang_thai_tuong_tac in ['da_goi', 'hen_goi_lai']:
                    kh.trang_thai = 'dang_cham_soc'

            # LỊCH HẸN
            elif loai == 'lich_hen':
                if trang_thai_tuong_tac == 'da_hoan_thanh':
                    kh.trang_thai = 'dang_cham_soc'
                elif trang_thai_tuong_tac == 'huy':
                    kh.trang_thai = 'da_huy'

            # BÁO GIÁ
            elif loai == 'bao_gia':
                if trang_thai_tuong_tac == 'dong_y':
                    kh.trang_thai = 'da_chot'
                elif trang_thai_tuong_tac == 'tu_choi':
                    kh.trang_thai = 'da_huy'
                elif trang_thai_tuong_tac == 'da_gui':
                    kh.trang_thai = 'dang_cham_soc'