# from odoo import http


# class MiModulo5(http.Controller):
#     @http.route('/mi_modulo_5/mi_modulo_5', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mi_modulo_5/mi_modulo_5/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mi_modulo_5.listing', {
#             'root': '/mi_modulo_5/mi_modulo_5',
#             'objects': http.request.env['mi_modulo_5.mi_modulo_5'].search([]),
#         })

#     @http.route('/mi_modulo_5/mi_modulo_5/objects/<model("mi_modulo_5.mi_modulo_5"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mi_modulo_5.object', {
#             'object': obj
#         })

