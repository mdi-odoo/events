odoo.define('website_event_snippet.s_events_frontend', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    var core = require('web.core');
    var s_animation = require('web_editor.snippets.animation');
    var QWeb = core.qweb;

    ajax.loadXML("/website_event_snippet/static/src/xml/event_template.xml", core.qweb);

    s_animation.registry.js_get_events = s_animation.Class.extend({
        selector : ".js_get_events",

        start: function () {
            this.redrow();
        },

        stop: function () {
            this.clean();
        },

        redrow: function (debug) {
            this.clean(debug);
            this.build(debug);
        },

        clean: function (debug) {
            this.$target.empty();
        },

        build: function (debug) {
            var self     = this,
                limit    = self.$target.data("events_limit"),
                cover    = self.$target.data("events_cover"),
                template = self.$target.data("template");

            // prevent user's editing
            self.$target.attr("contenteditable","False");

            // if no data, then use defaults values
            if (!limit) limit = 4;
            if (cover == undefined) cover = 1;

            // create the domain
            var domain = [['website_published', '=', true], ['state', '=', 'confirm']];
            
            ajax.jsonRpc('/website_event_snippet/render', 'call', {
                'domain': domain,
                'limit': limit,
            }).then(function (events) {
                var html = QWeb.render("website_event_snippet.media_list_template", {cover: cover, events:events});
                $(html).appendTo(self.$target);
            }).fail(function (e) {
                return;
            });
        },
    });
});
