from odoo import api, fields, models


class UpdateBiaya(models.TransientModel):
    _name = 'cameriq.updatebiaya'
        
    barang_id = fields.Many2one(comodel_name='cameriq.barang', string='Nama Barang', required=True)
    biaya_sewa = fields.Integer(string='Biaya Sewa')

    @api.onchange('barang_id')
    def _onchange_field(self):
        for record in self:
            record.biaya_sewa = record.barang_id.biaya_sewa
    
    def button_updatebiaya(self):
        for rec in self:
            self.env['cameriq.barang'].search([('id','=',rec.barang_id.id)]).write({'biaya_sewa': rec.biaya_sewa})
