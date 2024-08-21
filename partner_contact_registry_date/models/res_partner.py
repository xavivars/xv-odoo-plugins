# Copyright (C) 2024 Xavi Ivars <xavi.ivars@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class ResPartner(models.Model):
    """Partner with birth date in date format."""

    _inherit = "res.partner"

    registry_date = fields.Date("Registry Date")
    seniority = fields.Integer(readonly=True, compute="_compute_seniority")

    @api.depends("registry_date")
    def _compute_seniority(self):
        for record in self:
            seniority = 0
            if record.registry_date:
                seniority = relativedelta(fields.Date.today(), record.registry_date).years
            record.seniority = seniority
