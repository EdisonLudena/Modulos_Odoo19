/** @odoo-module **/

import { Store } from "@mail/core/common/store_service";
import { patch } from "@web/core/utils/patch";
import { fields } from "@mail/core/common/record";

patch(Store.prototype, {
    setup() {
        super.setup(...arguments);
        this.groupActivityCounter = 0;
        this.groupActivityGroups = fields.Attr([]);
    },

    async initialize() {
        await Promise.all([
            this.fetchStoreData("group_systray_get_activities"),
            super.initialize(...arguments),
        ]);
    },
});
