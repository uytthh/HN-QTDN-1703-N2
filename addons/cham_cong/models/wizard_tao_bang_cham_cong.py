# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class TaoBangChamCongHangLoatWizard(models.TransientModel):
    """Tự động tạo các dòng Bảng chấm công (chưa có giờ vào/ra) cho tất cả
    nhân viên đã đăng ký ca làm trong một khoảng ngày, để HR/nhân viên chỉ
    cần vào điền giờ vào - giờ ra thực tế thay vì tự tạo từng dòng.
    """
    _name = 'bang_cham_cong.hang_loat.wizard'
    _description = 'Tạo bảng chấm công hàng loạt'

    dot_dang_ky_id = fields.Many2one('dot_dang_ky', string="Đợt đăng ký")
    ngay_bat_dau = fields.Date(string="Từ ngày", required=True)
    ngay_ket_thuc = fields.Date(string="Đến ngày", required=True)
    nhan_vien_ids = fields.Many2many(
        'nhan_vien', string="Chỉ áp dụng cho nhân viên (để trống = tất cả)")

    @api.onchange('dot_dang_ky_id')
    def _onchange_dot_dang_ky_id(self):
        for record in self:
            if record.dot_dang_ky_id:
                record.ngay_bat_dau = record.dot_dang_ky_id.ngay_bat_dau
                record.ngay_ket_thuc = record.dot_dang_ky_id.ngay_ket_thuc

    def action_tao_bang_cham_cong(self):
        self.ensure_one()
        if self.ngay_bat_dau > self.ngay_ket_thuc:
            raise UserError("'Từ ngày' phải trước hoặc bằng 'Đến ngày'!")

        DangKy = self.env['dang_ky_ca_lam_theo_ngay']
        BangCC = self.env['bang_cham_cong']

        domain = [
            ('ngay_lam', '>=', self.ngay_bat_dau),
            ('ngay_lam', '<=', self.ngay_ket_thuc),
        ]
        if self.dot_dang_ky_id:
            domain.append(('dot_dang_ky_id', '=', self.dot_dang_ky_id.id))
        if self.nhan_vien_ids:
            domain.append(('nhan_vien_id', 'in', self.nhan_vien_ids.ids))

        dang_ky_list = DangKy.search(domain)

        so_tao = 0
        so_bo_qua = 0
        for dk in dang_ky_list:
            da_co = BangCC.search([
                ('nhan_vien_id', '=', dk.nhan_vien_id.id),
                ('ngay_cham_cong', '=', dk.ngay_lam),
            ], limit=1)
            if da_co:
                so_bo_qua += 1
                continue
            BangCC.create({
                'nhan_vien_id': dk.nhan_vien_id.id,
                'ngay_cham_cong': dk.ngay_lam,
            })
            so_tao += 1

        message = f"Đã tạo {so_tao} bảng chấm công mới."
        if so_bo_qua:
            message += f" Bỏ qua {so_bo_qua} ngày đã có bảng chấm công."

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Tạo bảng chấm công hàng loạt',
                'message': message,
                'type': 'success',
                'sticky': False,
                'next': {
                    'type': 'ir.actions.act_window',
                    'name': 'Bảng chấm công',
                    'res_model': 'bang_cham_cong',
                    'view_mode': 'tree,calendar,form',
                    'domain': [
                        ('ngay_cham_cong', '>=', self.ngay_bat_dau),
                        ('ngay_cham_cong', '<=', self.ngay_ket_thuc),
                    ],
                },
            },
        }
