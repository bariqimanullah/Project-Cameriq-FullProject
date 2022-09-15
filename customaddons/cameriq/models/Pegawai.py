from odoo import api, fields, models


class Pegawai(models.Model):
    _name = 'cameriq.pegawai'
    _rec_name = 'nama_pegawai'
    _description = 'New Description'

    nama_pegawai = fields.Char(string='Nama Pegawai', required=True)
    no_telp = fields.Char(string='No. Telepon', required=True)
    no_id = fields.Char(string='NIK', required=True)
    jenis_kelamin = fields.Selection(string='Jenis Kelamin', selection=[
        ('lakilaki', 'Laki-Laki'), 
        ('perempuan', 'Perempuan'),
        ], required=True)
    tgl_lahir = fields.Date(string='Tanggal Lahir', required=True)
    image_pegawai = fields.Binary(string='Image')
    
