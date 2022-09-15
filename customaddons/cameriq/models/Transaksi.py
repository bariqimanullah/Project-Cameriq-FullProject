from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import ValidationError, UserError

class Transaksi(models.Model):
    _name = 'cameriq.transaksi'
    _rec_name = 'client_name'
    _description = 'New Description'
    
    client_id = fields.Many2one('res.partner', string='Client', required=True, ondelete = 'cascade')
    client_name = fields.Char(string='Nama', related='client_id.name')
    client_address = fields.Char(string='Alamat', related='client_id.street')
    client_phone = fields.Char(string='No. Telepon', related='client_id.phone')
    client_mobile = fields.Char(string='No. HP', related='client_id.mobile')
    client_email = fields.Char(string='Email', related='client_id.email')
    client_image = fields.Binary(string='Image', related='client_id.image_1920')
    client_jenisid = fields.Selection(string='Jenis ID Pengenal', related='client_id.jenis_id')
    client_no_id = fields.Char(string='No. ID Pengenal', related='client_id.no_id')

    kode_transaksi = fields.Char(string='Kode Transaksi', compute='_compute_kode_transaksi')
    tgl_transaksi = fields.Datetime('Tanggal Transaksi', default = fields.Datetime.now(), readonly=True, required=True)
    tgl_sewa = fields.Date(string='Tanggal Sewa', required=True)
    tgl_akhirsewa = fields.Date(string='Tanggal Akhir Sewa', required=True)
    lama_sewa = fields.Integer(string='Lama Sewa (Hari)', compute='_compute_lama_sewa')

    detailbarang_ids = fields.One2many(comodel_name='cameriq.detailbarang', 
                                      inverse_name='transaksi_id', 
                                      string='Detail Barang')
    total_bayar = fields.Integer(string='Total', compute='_compute_total')

    _sql_constraints = [
        ('date_check', "CHECK ((tgl_sewa <= tgl_akhirsewa))", "Terdapat kesalahan format tanggal sewa. Silakan cek kembali!")
    ]

    @api.constrains('jumlah')
    def check_quantity(self):
        for rec in self:
            if rec.lama_sewa <= 0:
                raise ValidationError("Minimal sewa selama 1 hari.")

    state = fields.Selection(string='Status',
        selection=[('draft', 'Draft'),
                   ('onprocess', 'On Process'),
                   ('done', 'Done'),
                   ('canceled', 'Canceled'),
                   ],
        required=True, readonly=True, default='draft')

    @api.depends('client_name')
    def _compute_kode_transaksi(self):
        for rec in self:
            if rec.client_name:
                name = rec.client_name
                kode = name.replace(" ", "").lower()
                rec.kode_transaksi = kode
            else:
                rec.kode_transaksi = 0

    @api.depends('tgl_sewa','tgl_akhirsewa')
    def _compute_lama_sewa(self):
        for rec in self:
            date_format = '%Y-%m-%d'
            if rec.tgl_sewa and rec.tgl_akhirsewa != False:
                d1 = datetime.strptime(str(rec.tgl_sewa), date_format)
                d2 = datetime.strptime(str(rec.tgl_akhirsewa), date_format)
                daysDiff = str((d2-d1).days +1)
                rec.lama_sewa = int(daysDiff)
            else:
                rec.lama_sewa = 0

    @api.depends('detailbarang_ids')
    def _compute_total(self):
        for rec in self:
            subtotal = self.env['cameriq.detailbarang'].search([('transaksi_id','=',rec.id)]).mapped('subtotal')
            total = sum(subtotal) * rec.lama_sewa
            rec.total_bayar = total

    def unlink(self):
        if self.filtered(lambda line: line.state != 'draft'):
            raise UserError("Tidak dapat menghapus jika status BUKAN DRAFT")
        else:
            if self.detailbarang_ids:
                    item=[]
                    for rec in self:
                        item = self.env['cameriq.detailbarang'].search([('transaksi_id','=',rec.id)])
                    for ob in item:
                        ob.barang_id.jumlah_barang += ob.jumlah
        record = super(Transaksi, self).unlink()

    def write(self,vals):
        for rec in self:
            item = self.env['cameriq.detailbarang'].search([('transaksi_id','=',rec.id)])
            for data in item:
                data.barang_id.jumlah_barang += data.jumlah
        record = super(Transaksi,self).write(vals)
        for rec in self:
            new_item = self.env['cameriq.detailbarang'].search([('transaksi_id','=',rec.id)])
            for newdata in new_item:
                if newdata in item:
                    newdata.barang_id.jumlah_barang -= newdata.jumlah
                else:
                    pass
        return record

    def action_onprocess(self):
        self.write({'state': 'onprocess'})

    def action_done(self):
        if self.detailbarang_ids:
                    item=[]
                    for rec in self:
                        item = self.env['cameriq.detailbarang'].search([('transaksi_id','=',rec.id)])
                    for ob in item:
                        ob.barang_id.jumlah_barang += ob.jumlah
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'canceled'})

    def action_draft(self):
        self.write({'state': 'draft'})


class DetailBarang(models.Model):
    _name = 'cameriq.detailbarang'
    _description = 'New Description'

    transaksi_id = fields.Many2one(comodel_name='cameriq.transaksi', string='Transaksi', ondelete = 'cascade')
    kategori_id = fields.Many2one(comodel_name='cameriq.kategori', string='Kategori', ondelete = 'cascade')
    barang_id = fields.Many2one('cameriq.barang', string='Item', ondelete = 'cascade')
    biaya_sewa = fields.Integer(string='Biaya Sewa', related='barang_id.biaya_sewa')
    jumlah = fields.Integer(string='Jumlah')
    subtotal = fields.Integer(string='Subtotal', compute='_compute_subtotal')
    
    @api.depends('jumlah','biaya_sewa')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.jumlah * rec.biaya_sewa

    @api.model
    def create(self, vals):
        record = super(DetailBarang, self).create(vals)
        if record.jumlah:
            self.env['cameriq.barang'].search([('id', '=', record.barang_id.id)]).write({'jumlah_barang': record.barang_id.jumlah_barang - record.jumlah})
        return record

    @api.constrains('jumlah')
    def check_quantity(self):
        for rec in self:
            if rec.jumlah < 1:
                raise ValidationError("Minimal sewa {} sebanyak 1 buah".format(rec.barang_id.nama_barang))
            elif rec.barang_id.jumlah_barang < rec.jumlah:
                raise ValidationError("Stok {} tidak mencukupi. (sisa stok:{})".format(rec.barang_id.nama_barang, rec.barang_id.jumlah_barang))