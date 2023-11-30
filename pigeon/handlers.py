from typing import Any, Tuple

import telegram as tg
import telegram.ext as tg_ext

import pigeon.logging as logging
import pigeon.models as models

# ==================================================================================================


class BotAddedToChatHandler(tg_ext.ChatMemberHandler):
    """
    TODO
    """

    def __init__(self, bot, callback: tg_ext._utils.types.HandlerCallback):
        """
        TODO
        """
        super().__init__(callback)
        self.bot = bot

    def check_update(self, update: object) -> bool:
        """
        TODO
        """

        if not isinstance(update, tg.Update):
            return False

        my_chat_member = update.my_chat_member
        if not my_chat_member:
            return False

        # Ignore the update if no new user was added to the chat.
        new_chat_member = my_chat_member.new_chat_member
        if not isinstance(new_chat_member, tg.ChatMemberAdministrator):
            return False

        # Ignore the update if no information about the added user is given.
        user = new_chat_member.user
        if not isinstance(user, tg.User):
            return False

        # Ignore the update if the added user is not a bot.
        if not user.is_bot:
            return False

        # Ignore the update if the added user is not this bot.
        if user.id is None or user.id != self.bot.app.bot.id:
            return False

        return True

    def collect_additional_context(
            self,
            context: tg_ext.CallbackContext,
            update: tg.Update,
            app: tg_ext.Application,
            check_result: Any) -> None:
        """
        TODO
        """
        assert context
        assert update

        my_chat_member = update.my_chat_member
        if not my_chat_member:
            return

        chat = my_chat_member.chat
        if not chat:
            return

        # TODO: Pass the whole chat object here. Map the chat to a custom chat object.
        context.update({"chat_id": chat.id, "chat_title": chat.title})


class CommandHandler(tg_ext.MessageHandler):
    """
    TODO
    """

    def __init__(self, callback: tg_ext._utils.types.HandlerCallback):
        """
        TODO
        """
        super().__init__(tg_ext.filters.COMMAND, callback)

    def collect_additional_context(
            self,
            context: tg_ext.CallbackContext,
            update: tg.Update,
            app: tg_ext.Application,
            check_result: Any) -> None:
        assert update

        if update.channel_post:
            # The update originates from a CHANNEL, meaning the message is in the following format:
            # Message(
            #   channel_chat_created=False,
            #   chat=Chat(id=-1002058788806, title='...', type=<ChatType.CHANNEL>),
            #   date=datetime.datetime(2023, 11, 26, 13, 48, 54, tzinfo=datetime.timezone.utc),
            #   delete_chat_photo=False,
            #   entities=(MessageEntity(length=4, offset=0, type=<MessageEntityType.BOT_COMMAND>),),
            #   group_chat_created=False,
            #   message_id=16,
            #   sender_chat=Chat(id=-1002058788806, title='...', type=<ChatType.CHANNEL>),
            #   supergroup_chat_created=False,
            #   text='...'
            # )
            text = update.channel_post.text
            if not text:
                return

            chat = update.channel_post.chat
            if not chat:
                return

            from_chat = update.channel_post.sender_chat
            if not from_chat:
                return

            context.update({
                "cmd": text.split()[0][1:],
                "args": text.split()[1:],
                "chat_id": chat.id,
                "from_chat_id": from_chat.id
            })
            return

        if update.message:
            # The update originates from a GROUP, meaning the message is in the following format:
            # Message(
            #   channel_chat_created=False,
            #   chat=Chat(id=-1001810897453, title='...', type=<ChatType.SUPERGROUP>),
            #   date=datetime.datetime(2023, 11, 26, 14, 39, 57, tzinfo=datetime.timezone.utc),
            #   delete_chat_photo=False,
            #   entities=(MessageEntity(length=4, offset=0, type=<MessageEntityType.BOT_COMMAND>),),
            #   from_user=User(id=1139069550, is_bot=False, language_code='de', username='...'),
            #   group_chat_created=False,
            #   message_id=2704,
            #   supergroup_chat_created=False,
            #   text='...'
            # )
            text = update.message.text
            if not text:
                return

            chat = update.message.chat
            if not chat:
                return

            from_user = update.message.from_user
            if not from_user:
                return

            context.update({
                "cmd": text.split()[0][1:],
                "args": text.split()[1:],
                "chat_id": chat.id,
                "from_chat_id": from_user.id
            })


class MessageHandler(tg_ext.MessageHandler):
    """
    TODO
    """

    def __init__(self, callback: tg_ext._utils.types.HandlerCallback):
        """
        TODO
        """
        super().__init__(~tg_ext.filters.COMMAND, callback)


class CallbackQueryHandler(tg_ext.CallbackQueryHandler):
    """
    TODO
    """

    def __init__(self, callback: tg_ext._utils.types.HandlerCallback):
        """
        TODO
        """
        super().__init__(callback)
