# -*- coding: utf-8 -*-

from odoo.http import request
from odoo.addons.mail.controllers.webclient import WebclientController
from odoo.addons.mail.tools.discuss import Store

class ActivityManagementWebclientController(WebclientController):

    @classmethod
    def _process_request_for_internal_user(self, store: Store, name, params):
        super()._process_request_for_internal_user(store, name, params)
        if name == "group_systray_get_activities":
            bus_last_id = request.env["bus.bus"].sudo()._bus_last_id()
            groups = request.env["res.users"]._get_group_activity_groups()
            store.add_global_values(
                groupActivityCounter=sum(group.get("total_count", 0) for group in groups),
                activity_counter_bus_id=bus_last_id,
                groupActivityGroups=groups,
            )
