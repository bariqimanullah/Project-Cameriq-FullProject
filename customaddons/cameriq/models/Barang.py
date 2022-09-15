from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Barang(models.Model):
    _name = 'cameriq.barang'
    _rec_name = 'nama_barang'
    _description = 'New Description'

    nama_barang = fields.Char(string='Nama Barang', required=True)
    kode_barang = fields.Char(string='Kode Barang', required=True)
    kategori_id = fields.Many2one(comodel_name='cameriq.kategori', string='Kategori Barang', ondelete = 'cascade', required=True)
    merk_id = fields.Many2one(comodel_name='cameriq.merk', string='Merk', ondelete = 'cascade', required=True)
    jumlah_barang = fields.Integer(string='Jumlah Ketersediaan Barang', required=True)
    biaya_sewa = fields.Integer(string='Biaya Sewa (Rp.)')

    _sql_constraints = [
	    ('kode_barang_unique','unique (kode_barang)','Kode barang telah digunakan.')
    ]

    @api.constrains('jumlah_barang','biaya_sewa')
    def check_harga(self):
        for rec in self:
            if rec.jumlah_barang < 0:
                raise ValidationError("Format jumlah yang dimasukkan salah. Silakan cek kembali!")
            elif rec.biaya_sewa < 0:
                raise ValidationError("Format biaya sewa yang dimasukkan salah. Silakan cek kembali!")