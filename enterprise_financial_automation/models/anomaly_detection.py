from odoo import models, fields, api


class FinancialAnomaly(models.Model):
    _name = 'efa.anomaly'
    _description = 'Financial Anomaly Detection'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Anomaly', required=True)
    anomaly_type = fields.Selection([
        ('duplicate_entry', 'Duplicate Journal Entry'),
        ('unusual_amount', 'Unusual Amount'),
        ('round_number', 'Round Number Suspicion'),
        ('weekend_posting', 'Weekend Posting'),
        ('unusual_account', 'Unusual Account Combination'),
        ('manual_override', 'Manual Override Detected'),
    ], string='Type', required=True)
    amount = fields.Float(string='Amount')
    account = fields.Char(string='Account')
    detected_date = fields.Datetime(string='Detected', default=fields.Datetime.now)
    ai_confidence = fields.Float(string='AI Confidence %', default=0.0)
    state = fields.Selection([
        ('new', 'New'),
        ('investigating', 'Investigating'),
        ('confirmed', 'Confirmed Fraud'),
        ('false_positive', 'False Positive'),
        ('resolved', 'Resolved'),
    ], default='new', tracking=True)
    assigned_to = fields.Many2one('res.users', string='Investigator')
    description = fields.Text(string='Details')
    journal_ref = fields.Char(string='Journal Reference')

    def action_investigate(self):
        for rec in self:
            rec.state = 'investigating'

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_false_positive(self):
        for rec in self:
            rec.state = 'false_positive'

    def action_resolve(self):
        for rec in self:
            rec.state = 'resolved'

    @api.model
    def _cron_scan_anomalies(self):
        """AI-powered anomaly scan placeholder — integrates with GL data."""
        return True
