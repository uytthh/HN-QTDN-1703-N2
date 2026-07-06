from odoo import models, fields
import requests

class AIAssistant(models.TransientModel):
    _name = 'ai.assistant'
    _description = 'AI Assistant'

    cau_hoi = fields.Text()
    tra_loi = fields.Text(readonly=True)

    loai_context = fields.Selection([
        ('all', 'Toàn hệ thống'),
        ('hr', 'Nhân sự'),
        ('finance', 'Tài chính')
    ], default='all')

    def action_hoi_ai(self):
        config = self.env['ai.cau_hinh_api'].search([('active', '=', True)], limit=1)

        if not config:
            self.tra_loi = "Chưa có cấu hình API"
            return

        headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": config.model_name,
            "messages": [
                {"role": "user", "content": self.cau_hoi}
            ]
        }

        try:
            res = requests.post(config.api_url, json=payload, headers=headers)

            if res.status_code == 200:
                data = res.json()
                answer = data['choices'][0]['message']['content']

                self.tra_loi = answer

                self.env['ai.lich_su_chat'].create({
                    'cau_hoi': self.cau_hoi,
                    'tra_loi': answer,
                    'user_id': self.env.user.id,
                    'thanh_cong': True
                })
            else:
                self.tra_loi = res.text

        except Exception as e:
            self.tra_loi = str(e)
