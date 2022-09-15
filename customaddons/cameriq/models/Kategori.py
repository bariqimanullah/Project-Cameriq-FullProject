from odoo import api, fields, models

class Kategori(models.Model):
    _name = 'cameriq.kategori'
    _rec_name = 'nama_kategori'
    _description = 'New Description'

    nama_kategori = fields.Char(string='Nama Kategori', required=True)
    jumlah_item = fields.Integer(compute='_compute_jumlah_item', string='Jumlah Item')
    barang_ids = fields.One2many(comodel_name='cameriq.barang', inverse_name='kategori_id', string='Daftar Barang')
    merk_ids = fields.One2many(comodel_name='cameriq.merk', inverse_name='kategori_id', string='Daftar Merk')
    jumlah_merk = fields.Integer(compute='_compute_jumlah_merk', string='Jumlah Merk')
    
    @api.depends('merk_ids')
    def _compute_jumlah_merk(self):
        for rec in self:
            list_merk = self.env['cameriq.merk'].search([('kategori_id','=',rec.id)]).mapped('nama_merk')
            rec.jumlah_merk = len(list_merk)

    @api.depends('barang_ids')
    def _compute_jumlah_item(self):
        for rec in self:
            list_barang = self.env['cameriq.barang'].search([('kategori_id','=',rec.id)]).mapped('nama_barang')
            rec.jumlah_item = len(list_barang)

class Merk(models.Model):
    _name = 'cameriq.merk'
    _rec_name = 'nama_merk'
    _description = 'New Description'

    nama_merk = fields.Char(string='Nama Merk')
    kategori_id = fields.Many2one(comodel_name='cameriq.kategori', string='Kategori', ondelete = 'cascade')
    