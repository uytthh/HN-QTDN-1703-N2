from odoo import models, fields

class AILichSuChat(models.Model):
    _name = 'ai.lich_su_chat'
    _description = 'Lịch sử chat AI'

    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    thoi_gian = fields.Datetime(default=fields.Datetime.now)

    cau_hoi = fields.Text()
    tra_loi = fields.Text()

    context_data = fields.Text()
    thanh_cong = fields.Boolean(default=True)
    loi = fields.Text()
