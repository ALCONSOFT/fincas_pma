# -*- coding: utf-8 -*-
# from odoo import http


# class FincasPma(http.Controller):
#     @http.route('/fincas_pma/fincas_pma/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fincas_pma/fincas_pma/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fincas_pma.listing', {
#             'root': '/fincas_pma/fincas_pma',
#             'objects': http.request.env['fincas_pma.fincas_pma'].search([]),
#         })

#     @http.route('/fincas_pma/fincas_pma/objects/<model("fincas_pma.fincas_pma"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fincas_pma.object', {
#             'object': obj
#         })
