# -*- coding: utf-8 -*-
# from odoo import http


# class OzenelReports(http.Controller):
#     @http.route('/ozenel_reports/ozenel_reports', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ozenel_reports/ozenel_reports/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ozenel_reports.listing', {
#             'root': '/ozenel_reports/ozenel_reports',
#             'objects': http.request.env['ozenel_reports.ozenel_reports'].search([]),
#         })

#     @http.route('/ozenel_reports/ozenel_reports/objects/<model("ozenel_reports.ozenel_reports"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ozenel_reports.object', {
#             'object': obj
#         })

