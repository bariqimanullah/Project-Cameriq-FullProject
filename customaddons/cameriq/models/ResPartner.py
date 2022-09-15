from email.policy import default
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    jenis_id = fields.Selection([
        ('ktp', 'KTP'),
        ('sim', 'SIM')
    ], string='Jenis ID Pengenal', default='ktp', required=True)
    no_id = fields.Char(string='No ID Pengenal', default=0, required=True)
    tgl_registrasi = fields.Datetime(string='Tanggal Registrasi', default = fields.Datetime.now(), required=True)
    is_membership = fields.Boolean(string='Membership')
    id_member = fields.Char(string='Id Membership', required=False, domain="[('is_membership', '=', True)]", compute='_compute_kode_transaksi')

    @api.depends('is_membership')
    def _compute_kode_transaksi(self):
        for rec in self:
            if rec.is_membership != False:
                res_data = self.env['res.partner'].search([('name','=',rec.name)])
                name = res_data.name
                zip = res_data.zip
                kode = name.replace(" ", "").lower()+str(zip)
                rec.id_member = kode
            else:
                rec.id_member = 0