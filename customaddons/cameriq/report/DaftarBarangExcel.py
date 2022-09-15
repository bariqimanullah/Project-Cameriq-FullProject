from odoo import fields, models

class BarangXlsx(models.AbstractModel):
    _name = 'report.cameriq.report_barang_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    tgl_lap = fields.Date.today()
    def generate_xlsx_report(self, workbook, data, barang):
        sheet = workbook.add_worksheet('Daftar Barang')
        bold = workbook.add_format({'bold': True})
        sheet.set_column(0, 0, 30)
        sheet.set_column(0, 1, 30)
        sheet.set_column(0, 2, 30)
        sheet.set_column(0, 3, 30)
        sheet.set_column(0, 4, 30)
        sheet.write(0, 0, str(self.tgl_lap))
        sheet.write(2, 0, 'Nama Barang', bold)
        sheet.write(2, 1, 'Kode Barang', bold)
        sheet.write(2, 2, 'Kategori', bold)
        sheet.write(2, 3, 'Jumlah Ketersediaan Barang', bold)
        sheet.write(2, 4, 'Biaya Sewa Harian', bold)
        row = 3
        col = 0
        for obj in barang:
            sheet.write(row, col, obj.nama_barang)
            sheet.write(row, col+1, obj.kode_barang)
            sheet.write(row, col+2, obj.kategori_id.nama_kategori)
            sheet.write(row, col+3, obj.jumlah_barang)
            sheet.write(row, col+4, obj.biaya_sewa)
            row += 1