# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class MedicalMedicament(models.Model):
    _inherit = 'medical.medicament'

    is_prescription = fields.Boolean(
        string='Prescription Required',
        compute='_compute_is_prescription',
        help='Indicates if a prescription is required for this medicament',
    )
    is_controlled = fields.Boolean(
        string='Controlled Substance',
        help='Check this if the medicament is a controlled substance',
    )

    @api.multi
    def _compute_is_prescription(self):
        prescription_categ_id = self.env.ref(
            'sale_medical_prescription.product_category_rx'
        )
        for rec_id in self:
            if rec_id.categ_id == prescription_categ_id:
                rec_id.is_prescription = True
                continue
            rec_id.is_prescription = rec_id.categ_id._is_descendant_of(
                prescription_categ_id
            )
