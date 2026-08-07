# from odoo import http


# class MiModulo4(http.Controller):
#     @http.route('/mi_modulo_4/mi_modulo_4', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mi_modulo_4/mi_modulo_4/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mi_modulo_4.listing', {
#             'root': '/mi_modulo_4/mi_modulo_4',
#             'objects': http.request.env['mi_modulo_4.mi_modulo_4'].search([]),
#         })

#     @http.route('/mi_modulo_4/mi_modulo_4/objects/<model("mi_modulo_4.mi_modulo_4"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mi_modulo_4.object', {
#             'object': obj
#         })

