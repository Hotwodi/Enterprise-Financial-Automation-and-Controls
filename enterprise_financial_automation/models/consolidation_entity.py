from odoo import models, fields, api


class ConsolidationEntity(models.Model):
    _name = 'efa.consolidation.entity'
    _description = 'Consolidation Entity'
    _inherit = ['mail.thread']

    name = fields.Char(string='Entity Name', required=True)
    code = fields.Char(string='Entity Code', required=True)
    company_id = fields.Many2one('res.company', string='Company')
    currency_id = fields.Many2one('res.currency', string='Currency')
    ownership_pct = fields.Float(string='Ownership %', default=100.0)
    consolidation_method = fields.Selection([
        ('full', 'Full Consolidation'),
        ('proportional', 'Proportional'),
        ('equity', 'Equity Method'),
    ], default='full')
    period = fields.Char(string='Period')
    total_assets = fields.Float(string='Total Assets')
    total_revenue = fields.Float(string='Total Revenue')
    net_income = fields.Float(string='Net Income')
    intercompany_eliminations = fields.Float(string='Intercompany Eliminations')
    consolidated = fields.Boolean(string='Consolidated', default=False)

    @api.model
    def _cron_run_consolidation(self):
        entities = self.search([('consolidated', '=', False)])
        for ent in entities:
            ent.consolidated = True
