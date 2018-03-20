odoo.define('website_event_snippet.s_events_editor', function (require) {
    'use strict';

    var core = require('web.core');
    var s_options = require('web_editor.snippets.options');
    var s_animation = require('web_editor.snippets.animation');
    var Model = require('web.Model');

    var _t = core._t;

    // js_get_events
    s_options.registry.js_get_events = s_options.Class.extend({
        drop_and_build_snippet: function () {
            if (!this.$target.data('snippet-view')) {
                this.$target.data("snippet-view", new s_animation.registry.js_get_events(this.$target));
            }
        },

        clean_for_save: function () {
            this.$target.empty();
        },
    });

    // js_get_events limit
    s_options.registry.js_get_events_limit = s_options.Class.extend({
        start: function () {
            var self = this;
            setTimeout(function () {
                var ul = self.$overlay.find(".snippet-option-js_get_events_limit > ul");
                if (self.$target.attr("data-events_limit")) {
                    var limit = self.$target.attr("data-events_limit");
                    ul.find('li[data-events_limit="' + limit + '"]').addClass("active");
                } else {
                    ul.find('li[data-events_limit="4"]').addClass("active");
                }
            }, 100);
        },

        events_limit: function (type, value, $li) {
            var self = this;
            if (type != "click") {return;}
            console.log('limit');
            value = parseInt(value);
            this.$target.attr("data-events_limit",value)
                                    .data("events_limit",value)
                                    .data('snippet-view').redrow(true);
            setTimeout(function () {
                $li.parent().find("li").removeClass("active");
                $li.addClass("active");
            }, 100);
        },
    });

    //Event Cover Image Enable/Disable Snippet Option.
    s_options.registry.js_get_events_cover = s_options.Class.extend({
        start: function () {
            var self = this;
            setTimeout(function () {
                var ul = self.$overlay.find(".snippet-option-js_get_events_cover > ul");
                if (self.$target.attr("data-events_cover")) {
                    var cover = self.$target.attr("data-events_cover");
                    ul.find('li[data-events_cover="' + cover + '"]').addClass("active");
                } else {
                    ul.find('li[data-events_cover="1"]').addClass("active");
                }
            }, 100);
        },

        events_cover: function (type, value, $li) {
            var self = this;
            if (type != "click") {return;}
            value = parseInt(value);
            this.$target.attr("data-events_cover",value)
                                    .data("events_cover",value)
                                    .data('snippet-view').redrow(true);
            setTimeout(function () {
                $li.parent().find("li").removeClass("active");
                $li.addClass("active");
            }, 100);
        },
    });
});
