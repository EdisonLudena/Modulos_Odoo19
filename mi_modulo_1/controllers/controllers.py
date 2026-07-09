# from odoo import http


# class MiModulo1(http.Controller):
#     @http.route('/mi_modulo_1/mi_modulo_1', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mi_modulo_1/mi_modulo_1/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mi_modulo_1.listing', {
#             'root': '/mi_modulo_1/mi_modulo_1',
#             'objects': http.request.env['mi_modulo_1.mi_modulo_1'].search([]),
#         })

#     @http.route('/mi_modulo_1/mi_modulo_1/objects/<model("mi_modulo_1.mi_modulo_1"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mi_modulo_1.object', {
#             'object': obj
#         })

