# from odoo import http


# class MiModulo1A(http.Controller):
#     @http.route('/mi_modulo_1__a/mi_modulo_1__a', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mi_modulo_1__a/mi_modulo_1__a/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mi_modulo_1__a.listing', {
#             'root': '/mi_modulo_1__a/mi_modulo_1__a',
#             'objects': http.request.env['mi_modulo_1__a.mi_modulo_1__a'].search([]),
#         })

#     @http.route('/mi_modulo_1__a/mi_modulo_1__a/objects/<model("mi_modulo_1__a.mi_modulo_1__a"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mi_modulo_1__a.object', {
#             'object': obj
#         })

