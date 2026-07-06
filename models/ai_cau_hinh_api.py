from odoo import models, fields

class AICauHinhAPI(models.Model):
    _name = 'ai.cau_hinh_api'
    _description = 'Cấu hình API AI'

    ten = fields.Char(string="Tên cấu hình", required=True)
    api_url = fields.Char(
        string="API URL",
        default="https://openrouter.ai/api/v1/chat/completions"
    )
    model_name = fields.Char(
        string="Model",
        default="openai/gpt-4o-mini"
    )
    api_key = fields.Text(string="API Key")
    active = fields.Boolean(default=True)
