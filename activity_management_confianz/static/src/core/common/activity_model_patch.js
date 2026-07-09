/** @odoo-module **/

import { Activity } from "@mail/core/common/activity_model";
import { patch } from "@web/core/utils/patch";
import { fields } from "@mail/core/common/record";

patch(Activity.prototype, {
    setup() {
        super.setup(...arguments);
        this.team_id = fields.Attr(false);
    },
});
