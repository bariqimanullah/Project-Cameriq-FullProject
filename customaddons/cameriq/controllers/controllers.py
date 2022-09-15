from odoo import http, models, fields
from odoo.http import request
import json

class Cameriq(http.Controller):
    @http.route('/cameriq/getbarang', auth='public', method=['GET'])
    def getBarang(self, **kw):
        barang = request.env['cameriq.barang'].search([])
        isi = []
        for b in barang:
            isi.append({
                'nama_barang' : b.nama_barang,
                'biaya_sewa' : b.biaya_sewa,
                'jumlah_barang' : b.jumlah_barang
            })
        return json.dumps(isi)