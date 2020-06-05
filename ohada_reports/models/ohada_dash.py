# Copyright 2020 Vildan Safin <https://www.it-projects.info/team/Enigma228322>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons.web.controllers.main import clean_action
import logging

_logger = logging.getLogger(__name__)


class OhadaDash(models.Model):
    _name = "ohada.dash"
    _inherit = "ohada.dashboard"
    _description = "OHADA dashboard"

    name = fields.Char(required=True)
    name_to_display = fields.Selection([('name', 'Name'),
                                        ('company', 'Company')],
                                        default='name')
    display_name = fields.Char(compute='_compute_display_name')
    active = fields.Boolean()
    show_on_dashboard = fields.Boolean()
    sequence = fields.Integer()
    color = fields.Integer('Color index')
    type = fields.Selection([('report', 'Report'),
                             ('info_button', 'Info button'),
                             ('note_button', 'Note button'),
                             ('other_button', 'Other button'),
                             ('mix', 'Mix')],
                            required=True)
    # required if type == ‘report’.
    report_id = fields.Many2one('ohada.financial.html.report', string='OHADA report')
    report_type = fields.Char(string='Report type', related='report_id.code')
    # required only if type == ‘report’.
    displayed_report_line = fields.Many2one('ohada.financial.html.report.line')
    chart_type = fields.Selection([('barChart', 'Bar chart'),
                                   ('lineChart', 'Line chart')])
    dash_size = fields.Selection([('small', 'Small'),
                                  ('middle', 'Middle'),
                                  ('large', 'Large')])
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda s: s.env.user.company_id
    )
    currency_id = fields.Char(related='company_id.currency_id.symbol', string='Currency symbol')
    reports = fields.Text(compute='_compute_reports')

    def _compute_reports(self):
        for dash in self:
            if dash.type == 'note_button':
                dash.reports = self.env['ohada.financial.html.report'].search([('type', '=', 'note'), ('secondary', '=', False)])
                report_data = []
                import wdb;wdb.set_trace()
                for report in dash.reports:
                    report_data.append({
                        'name': report.,
                        'id': report.id
                    })
                self.reports = json.dumps(report_data)

    def _compute_display_name(self):
        _logger.info("_compute_display_name was called!")
        for dash in self:
            if dash.name_to_display == 'name':
                dash.display_name = dash.name
            else:
                dash.display_name = 'Company' + str(dash.id)

    @api.multi
    def open_action(self):
        # report = self.report_id
        report = self.env['ohada.financial.html.report'].search([('code', '=', self.report_type)])
        action = self.env['ir.actions.client'].sudo().search([('name', '=', report.name)]).read()[0]
        action = clean_action(action)
        ctx = self.env.context.copy()
        if action:
            ctx.update({
                    'id': report.id,
                    'report_options': report.make_temp_options(),
                    'model': report._name
            })
        action['context'] = ctx
        return action
    
    # @api.multi
    # def open_action_by_id(self, params):
    #     import wdb;wdb.set_trace()
    #     report = self.env.ref('ohada_reports.'+ params['ref_id'])
    #     action = self.env['ir.actions.client'].sudo().search([('name', '=', report.name)]).read()[0]
    #     action = clean_action(action)
    #     ctx = self.env.context.copy()
    #     if action:
    #         ctx.update({
    #                 'id': report.id,
    #                 'report_options': report.make_temp_options(),
    #                 'model': report._name
    #         })
    #     action['context'] = ctx
    #     return action


class ReportOhadaFinancialReport(models.Model):
    _inherit = "ohada.financial.html.report"

    dashboard_report_id = fields.One2many('ohada.dash', 'report_id')


class OhadaFinancialReportLine(models.Model):
    _inherit = "ohada.financial.html.report.line"

    dashboard_displayed_report_line = fields.One2many('ohada.dash', 'displayed_report_line')
