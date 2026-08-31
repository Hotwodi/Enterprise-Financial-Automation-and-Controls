from odoo import models, fields, api


class ReconciliationRule(models.Model):
    _name = 'efa.reconciliation.rule'
    _description = 'Smart Reconciliation Rule'
    _inherit = ['mail.thread']

    name = fields.Char(string='Rule Name', required=True)
    rule_type = fields.Selection([
        ('exact_match', 'Exact Amount Match'),
        ('fuzzy_match', 'Fuzzy Amount Match (±tolerance)'),
        ('reference_match', 'Reference Number Match'),
        ('date_range', 'Date Range Match'),
        ('composite', 'Composite Match'),
    ], string='Match Type', default='exact_match')
    tolerance = fields.Float(string='Tolerance Amount', default=0.01)
    auto_match = fields.Boolean(string='Auto-Match', default=True)
    active = fields.Boolean(string='Active', default=True)
    matched_count = fields.Integer(string='Matched Items', default=0)
    unmatched_count = fields.Integer(string='Unmatched Items', default=0)
    last_run = fields.Datetime(string='Last Run')

    def action_run_reconciliation(self):
        for rec in self:
            rec.last_run = fields.Datetime.now()

    @api.model
    def _cron_auto_reconcile(self):
        rules = self.search([('active', '=', True), ('auto_match', '=', True)])
        for rule in rules:
            rule.action_run_reconciliation()
