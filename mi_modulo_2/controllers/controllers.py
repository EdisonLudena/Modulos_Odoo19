# from odoo import http


# class MiModulo2(http.Controller):
#     @http.route('/mi_modulo_2/mi_modulo_2', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mi_modulo_2/mi_modulo_2/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mi_modulo_2.listing', {
#             'root': '/mi_modulo_2/mi_modulo_2',
#             'objects': http.request.env['mi_modulo_2.mi_modulo_2'].search([]),
#         })

#     @http.route('/mi_modulo_2/mi_modulo_2/objects/<model("mi_modulo_2.mi_modulo_2"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mi_modulo_2.object', {
#             'object': obj
#         })

