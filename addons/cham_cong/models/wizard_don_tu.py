# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class DonTuTuChoiWizard(models.TransientModel):
    """Wizard nhập lý do khi từ chối đơn từ.

    Trước đây nút "Từ chối" gọi thẳng tới model 'don_tu.tu_choi.wizard'
    nhưng model này chưa từng được định nghĩa -> bấm vào sẽ báo lỗi.
    """
    _name = 'don_tu.tu_choi.wizard'
    _description = 'Wizard từ chối đơn từ'

    don_tu_id = fields.Many2one('don_tu', string="Đơn từ", required=True)
    ten_don = fields.Char(related='don_tu_id.ten_don', string="Đơn")
    ly_do_tu_choi = fields.Text(string="Lý do từ chối", required=True)

    def action_xac_nhan(self):
        self.ensure_one()
        if not self.ly_do_tu_choi or not self.ly_do_tu_choi.strip():
            raise UserError("Vui lòng nhập lý do từ chối!")
        self.don_tu_id.action_tu_choi_voi_ly_do(self.ly_do_tu_choi)
        return {'type': 'ir.actions.act_window_close'}
