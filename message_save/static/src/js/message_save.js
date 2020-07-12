odoo.define('message_save.save', function (require) {
"use strict";

var ThreadWidget = require('mail.widget.Thread');

ThreadWidget.include({
    events: _.extend(ThreadWidget.prototype.events, {
            'click .message_save': '_onClickSaveMessage',
        }),

    _onClickSaveMessage: function (e) {
        var messageID = $(e.currentTarget).data('message-id');
        var context = this.getSession().user_context;
        return this._rpc({
                model: 'mail.message',
                method: 'save_partner_message',
                args: [[], messageID],
                context: context,
        });
    },
});
});
