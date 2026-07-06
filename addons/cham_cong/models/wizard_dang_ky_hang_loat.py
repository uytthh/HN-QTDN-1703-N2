# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta


class DangKyCaLamHangLoatWizard(models.TransientModel):
    """Đăng ký ca làm cho nhiều nhân viên / nhiều ngày trong một đợt đăng ký
    chỉ bằng một thao tác, thay vì phải tạo từng dòng cho từng ngày.
    """
    _name = 'dang_ky_ca_lam.hang_loat.wizard'
    _description = 'Đăng ký ca làm hàng loạt'

    dot_dang_ky_id = fields.Many2one(
        'dot_dang_ky', string="Đợt đăng ký", required=True)
    nhan_vien_ids = fields.Many2many(
        'nhan_vien', string="Nhân viên",
        domain="[('id', 'in', nhan_vien_kha_dung_ids)]",
        required=True,
        help="Chỉ hiển thị nhân viên đã có trong đợt đăng ký đã chọn")
    nhan_vien_kha_dung_ids = fields.Many2many(
        'nhan_vien', compute='_compute_nhan_vien_kha_dung',
        string="Nhân viên khả dụng")

    ngay_bat_dau = fields.Date(string="Từ ngày", required=True)
    ngay_ket_thuc = fields.Date(string="Đến ngày", required=True)

    ca_lam = fields.Selection([
        ("Sáng", "Sáng"),
        ("Chiều", "Chiều"),
        ("Cả ngày", "Cả Ngày"),
    ], string="Ca làm", default="Cả ngày", required=True)

    ap_dung_t2_t6 = fields.Boolean(string="Thứ 2 - Thứ 6", default=True)
    ap_dung_t7 = fields.Boolean(string="Thứ 7", default=False)
    ap_dung_cn = fields.Boolean(string="Chủ nhật", default=False)

    bo_qua_neu_da_co = fields.Boolean(
        string="Bỏ qua nếu đã đăng ký", default=True,
        help="Nếu nhân viên đã có đăng ký cho ngày đó thì sẽ không tạo trùng")

    @api.depends('dot_dang_ky_id')
    def _compute_nhan_vien_kha_dung(self):
        for record in self:
            record.nhan_vien_kha_dung_ids = record.dot_dang_ky_id.nhan_vien_ids

    @api.onchange('dot_dang_ky_id')
    def _onchange_dot_dang_ky_id(self):
        for record in self:
            if record.dot_dang_ky_id:
                record.ngay_bat_dau = record.dot_dang_ky_id.ngay_bat_dau
                record.ngay_ket_thuc = record.dot_dang_ky_id.ngay_ket_thuc
                record.nhan_vien_ids = record.dot_dang_ky_id.nhan_vien_ids

    def action_tao_dang_ky(self):
        self.ensure_one()
        if self.ngay_bat_dau > self.ngay_ket_thuc:
            raise UserError("'Từ ngày' phải trước hoặc bằng 'Đến ngày'!")
        if self.ngay_bat_dau < self.dot_dang_ky_id.ngay_bat_dau or \
                self.ngay_ket_thuc > self.dot_dang_ky_id.ngay_ket_thuc:
            raise UserError(
                "Khoảng ngày phải nằm trong phạm vi của đợt đăng ký "
                f"({self.dot_dang_ky_id.ngay_bat_dau} - {self.dot_dang_ky_id.ngay_ket_thuc})!")
        if not any([self.ap_dung_t2_t6, self.ap_dung_t7, self.ap_dung_cn]):
            raise UserError("Vui lòng chọn ít nhất một nhóm ngày trong tuần để áp dụng!")

        DangKy = self.env['dang_ky_ca_lam_theo_ngay']
        so_tao = 0
        so_bo_qua = 0

        ngay = self.ngay_bat_dau
        danh_sach_ngay = []
        while ngay <= self.ngay_ket_thuc:
            weekday = ngay.weekday()  # 0=T2 ... 5=T7, 6=CN
            if weekday <= 4 and self.ap_dung_t2_t6:
                danh_sach_ngay.append(ngay)
            elif weekday == 5 and self.ap_dung_t7:
                danh_sach_ngay.append(ngay)
            elif weekday == 6 and self.ap_dung_cn:
                danh_sach_ngay.append(ngay)
            ngay += timedelta(days=1)

        for nv in self.nhan_vien_ids:
            for ngay_lam in danh_sach_ngay:
                da_co = DangKy.search([
                    ('nhan_vien_id', '=', nv.id),
                    ('ngay_lam', '=', ngay_lam),
                ], limit=1)
                if da_co:
                    if self.bo_qua_neu_da_co:
                        so_bo_qua += 1
                        continue
                    else:
                        da_co.write({
                            'ca_lam': self.ca_lam,
                            'dot_dang_ky_id': self.dot_dang_ky_id.id,
                        })
                        so_tao += 1
                        continue

                DangKy.create({
                    'ma_dot_ngay': f"DKCA-{nv.id}-{ngay_lam.strftime('%Y%m%d')}",
                    'dot_dang_ky_id': self.dot_dang_ky_id.id,
                    'nhan_vien_id': nv.id,
                    'ngay_lam': ngay_lam,
                    'ca_lam': self.ca_lam,
                })
                so_tao += 1

        message = f"Đã tạo/cập nhật {so_tao} đăng ký ca làm."
        if so_bo_qua:
            message += f" Bỏ qua {so_bo_qua} ngày đã có đăng ký."

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Đăng ký ca làm hàng loạt',
                'message': message,
                'type': 'success',
                'sticky': False,
                'next': {
                    'type': 'ir.actions.act_window',
                    'name': 'Đăng ký ca làm theo ngày',
                    'res_model': 'dang_ky_ca_lam_theo_ngay',
                    'view_mode': 'tree,form',
                    'domain': [('dot_dang_ky_id', '=', self.dot_dang_ky_id.id)],
                },
            },
        }
