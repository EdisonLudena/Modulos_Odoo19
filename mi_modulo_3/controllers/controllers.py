# from odoo import http


# class MiModulo3(http.Controller):
#     @http.route('/mi_modulo_3/mi_modulo_3', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mi_modulo_3/mi_modulo_3/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mi_modulo_3.listing', {
#             'root': '/mi_modulo_3/mi_modulo_3',
#             'objects': http.request.env['mi_modulo_3.mi_modulo_3'].search([]),
#         })

#     @http.route('/mi_modulo_3/mi_modulo_3/objects/<model("mi_modulo_3.mi_modulo_3"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mi_modulo_3.object', {
#             'object': obj
#         })

