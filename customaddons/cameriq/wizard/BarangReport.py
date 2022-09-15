from odoo import fields, models, api

class BarangReport(models.TransientModel):
    _name = 'cameriq.barangreport'
    _description = 'Description'

    kategori_id = fields.Many2one(comodel_name='cameriq.kategori', string='Kategori', required=True)
    tgl_report = fields.Datetime('Tanggal Transaksi', default = fields.Datetime.now())

    def action_barang_report(self):
        kategori_id = self.kategori_id
        tgl_report = self.tgl_report
        if kategori_id:
            barang = self.env['cameriq.barang'].search_read([('kategori_id', '=', kategori_id.id)])
        data = {
            'form': self.read()[0],
            'barangxx': barang,
        }
        return self.env.ref('cameriq.wizard_barangreport_pdf').report_action(self, data=data)