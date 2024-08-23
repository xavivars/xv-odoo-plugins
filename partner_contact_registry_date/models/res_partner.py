# Copyright (C) 2024 Xavi Ivars <xavi.ivars@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class ResPartner(models.Model):
    """Partner with birth date in date format."""

    _inherit = "res.partner"

    registry_date = fields.Date("Registry Date")
    seniority = fields.Integer(readonly=True, compute="_compute_seniority")
    position = fields.Text("Número de llista", readonly=True, compute="_compute_position")

    registry_type = fields.Selection(
        [
            ("regular", "Membre de ple dret"),
            ("honor", "Membre honorífic"),
            ("menor", "Membre menor d'edat"),
        ],
        string="Modalitat de registre",
        default="regular",
    )

    quota_type = fields.Selection(
        [
            ("full", "Quota íntegra"),
            ("remote", "Fora de la localitat"),
            ("discounted", "Tornant d'excedència" )
        ],
        string="Tipus de quota",
        default="full",
    )

    retired = fields.Boolean("Jubilat")
    exempt = fields.Boolean("En excedència")


    @api.depends("seniority", "age")
    def _compute_position(self):
        all_partners = self.env["res.partner"].search(['registry_date', '=like', '%' ], "seniority asc, age asc" )
        for record in self:
            record.position = 0
            i = 1
            for partner in all_partners:
                if partner.id == record.id:
                    record.position = i
                i += 1


    @api.depends("registry_date")
    def _compute_seniority(self):
        for record in self:
            seniority = 0
            if record.registry_date:
                seniority = relativedelta(fields.Date.today(), record.registry_date).years
            record.seniority = seniority
