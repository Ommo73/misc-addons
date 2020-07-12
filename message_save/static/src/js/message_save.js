odoo.define('message_save.save', function (require) {
"use strict";

var ThreadWidget = require('mail.widget.Thread');
var Message = require('mail.model.Message');


ThreadWidget.include({
    events: _.extend(ThreadWidget.prototype.events, {
            'click .message_save': '_onClickSaveMessage',
        }),

    _onClickSaveMessage: function (e) {
        var self = this;
        self.icon = $(e.currentTarget)
        if (self.icon.hasClass('fa-bookmark-o')) {
            var messageID = $(e.currentTarget).data('message-id');
            var context = this.getSession().user_context;
            return this._rpc({
                    model: 'mail.message',
                    method: 'save_partner_message',
                    args: [[], messageID],
                    context: context,
            })
            .then(function (result){
                    self.icon.removeClass('fa-bookmark-o');
                    self.icon.addClass('fa-bookmark');
                });
        };
    },
});

Message.include({
    init: function (parent, data, emojis) {
        this._super.apply(this, arguments);
        this._isSaved = data.saved;
    },

    isSaved: function (){
        return this._isSaved;
    },
});
});
