from odoo import api, fields, models


class UpdateStok(models.TransientModel):
    _name = 'cameriq.updatestok'
        
    barang_id = fields.Many2one(comodel_name='cameriq.barang', string='Nama Barang', required=True)
    jumlah_stok = fields.Integer(string='Jumlah Stok')

    @api.onchange('barang_id')
    def _onchange_field(self):
        for record in self:
            record.jumlah_stok = record.barang_id.jumlah_barang
    
    def button_updatestok(self):
        for rec in self:
            self.env['cameriq.barang'].search([('id','=',rec.barang_id.id)]).write({'jumlah_barang': rec.jumlah_stok})
