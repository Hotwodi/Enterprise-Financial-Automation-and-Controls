from odoo import models, fields, api, _


class InternalControl(models.Model):
    _name = 'efa.internal.control'
    _description = 'Internal Control'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Control Name', required=True, tracking=True)
    code = fields.Char(string='Control ID', required=True)
    description = fields.Text(string='Description')
    control_type = fields.Selection([
        ('preventive', 'Preventive'),
        ('detective', 'Detective'),
        ('corrective', 'Corrective'),
    ], string='Type', default='preventive')
    frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual'),
    ], string='Frequency', default='monthly')
    owner_id = fields.Many2one('res.users', string='Control Owner')
    state = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('failed', 'Failed'),
    ], string='Status', default='active', tracking=True)
    compliance_score = fields.Float(string='Compliance Score', default=100.0, help='0-100')
    last_tested = fields.Date(string='Last Tested')
    sod_conflict = fields.Boolean(string='SoD Conflict Detected', default=False)
    sod_notes = fields.Text(string='SoD Conflict Notes')

    @api.model
    def _cron_run_control_tests(self):
        controls = self.search([('state', '=', 'active')])
        for ctrl in controls:
            ctrl.last_tested = fields.Date.today()
            if ctrl.sod_conflict:
                ctrl.compliance_score = max(0, ctrl.compliance_score - 25)
            if ctrl.compliance_score < 50:
                ctrl.state = 'failed'


class SoDConflict(models.Model):
    _name = 'efa.sod.conflict'
    _description = 'Segregation of Duties Conflict'

    name = fields.Char(string='Conflict Name', required=True)
    user_id = fields.Many2one('res.users', string='User')
    role_a = fields.Char(string='Role A')
    role_b = fields.Char(string='Role B')
    severity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], default='medium')
    state = fields.Selection([
        ('open', 'Open'),
        ('mitigated', 'Mitigated'),
        ('resolved', 'Resolved'),
    ], default='open')
    detected_date = fields.Date(string='Detected', default=fields.Date.today)
    control_id = fields.Many2one('efa.internal.control', string='Related Control')
