from odoo import fields, models, api


class TransaksiReport(models.TransientModel):
    _name = 'cameriq.transaksireport'
    _description = 'Description'

    client_id = fields.Many2one(comodel_name='res.partner', string='Client', required=False)
    from_date = fields.Date(string='Dari Tanggal', required=False)
    to_date = fields.Date(string='Ke tanggal', required=False)

    def action_transaksi_report(self):
        filter = []
        client_id = self.client_id
        from_date = self.from_date
        to_date = self.to_date
        if client_id:
            filter += [('client_id', '=', client_id.id)]
        if from_date:
            filter += [('tgl_transaksi', '>=', from_date)]
        if to_date:
            filter += [('tgl_transaksi', '<=', to_date)]
        transaksi = self.env['cameriq.transaksi'].search_read(filter)
        data = {
            'form': self.read()[0],
            'client': {'name':(client_id.name), 'address':(client_id.street), 'phone':(client_id.phone), 'email':(client_id.email)},
            'transaksixx': transaksi,
        }
        return self.env.ref('cameriq.wizard_transaksireport_pdf').report_action(self, data=data)