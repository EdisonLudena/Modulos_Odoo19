/** @odoo-module **/

import { Component } from "@odoo/owl";
import { ActivityMenu } from "@mail/core/web/activity_menu";
import { registry } from "@web/core/registry";

export class GroupActivityMenu extends ActivityMenu {
    static template = "activity_management_confianz.GroupActivityMenu";

    openActivityGroup(group, filter = "all", newWindow) {
        this.dropdown.close();
        const context = {
            force_search_count: 1,
            search_default_filter_activities_my: 0,
            group_activities_only: 1, // Flag to tell the mixin to only show team activities
            group_activity_target_model: group.model, // Explicit target for search restriction
        };

        if (filter === "all") {
            context["search_default_activities_overdue"] = 1;
            context["search_default_activities_today"] = 1;
        } else if (filter === "overdue") {
            context["search_default_activities_overdue"] = 1;
        } else if (filter === "today") {
            context["search_default_activities_today"] = 1;
        } else if (filter === "upcoming_all") {
            context["search_default_activities_upcoming_all"] = 1;
        }

        let domain = [];
        if (group.domain) {
            domain = group.domain;
        }
        const views = this.availableViews(group);

        this.executeActivityAction(group, domain, views, context, newWindow);
    }
}

registry
    .category("systray")
    .add("activity_management_confianz.group_activity_menu", { Component: GroupActivityMenu }, { sequence: 21 });
