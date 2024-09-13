# Copyright (C) 2024 Xavi Ivars <xavi.ivars@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class ResPartner(models.Model):
    """Partner with registry date."""

    _inherit = "res.partner"

    registry_date = fields.Date("Registry Date")
    seniority = fields.Integer(readonly=True, compute="_compute_seniority")
    position = fields.Integer("Número de llista", readonly=True, compute="_compute_position", store=True)

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
            ("student", "Estudiant"),
            ("discounted", "Tornant d'excedència" )
        ],
        string="Tipus de quota",
        default="full",
    )

    retired = fields.Boolean("Jubilat")
    exempt = fields.Boolean("En excedència")


    @api.depends("registry_date", "birthdate_date")
    def _compute_position(self):
        all_partner = self.env['res.partner'].search([])
        all_with_registry = all_partner.filtered(lambda r: r.registry_date is not None and r.registry_date != False)
        all_with_birthdate = all_with_registry.filtered(lambda r: r.birthdate_date is not None and r.birthdate_date != False)
        all_sorted = all_with_birthdate.sorted(lambda r: f"{r.registry_date}-{r.birthdate_date}")

        for record in self:
            record.position = 0
            i = 1
            for partner in all_sorted:
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
