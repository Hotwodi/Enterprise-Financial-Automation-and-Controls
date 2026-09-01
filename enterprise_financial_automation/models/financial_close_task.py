from odoo import models, fields, api, _
from odoo.exceptions import UserError


class FinancialCloseTask(models.Model):
    _name = 'efa.close.task'
    _description = 'Financial Close Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, id'

    name = fields.Char(string='Task Name', required=True, tracking=True)
    sequence = fields.Integer(default=10)
    period = fields.Char(string='Close Period', required=True, help='e.g. 2025-01')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    assigned_to = fields.Many2one('res.users', string='Assigned To', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('review', 'Under Review'),
        ('done', 'Completed'),
        ('blocked', 'Blocked'),
    ], string='Status', default='draft', tracking=True)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'High'),
        ('2', 'Critical'),
    ], default='0')
    due_date = fields.Date(string='Due Date')
    completed_date = fields.Date(string='Completed Date')
    notes = fields.Html(string='Notes')
    ai_risk_score = fields.Float(string='AI Risk Score', default=0.0, help='AI-generated risk score 0-100')

    def action_start(self):
        for rec in self:
            rec.state = 'in_progress'

    def action_review(self):
        for rec in self:
            rec.state = 'review'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
            rec.completed_date = fields.Date.today()

    def action_block(self):
        for rec in self:
            rec.state = 'blocked'

    @api.model
    def _cron_ai_risk_assessment(self):
        tasks = self.search([('state', 'in', ['draft', 'in_progress', 'review'])])
        for task in tasks:
            score = 0.0
            if task.priority == '2':
                score += 40
            elif task.priority == '1':
                score += 20
            if task.due_date:
                days_left = (task.due_date - fields.Date.today()).days
                if days_left < 0:
                    score += 40
                elif days_left <= 3:
                    score += 25
                elif days_left <= 7:
                    score += 10
            if task.state == 'blocked':
                score += 30
            task.ai_risk_score = min(score, 100.0)
