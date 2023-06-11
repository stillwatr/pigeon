from typing import Optional, Union

import telegram as tg
import telegram.ext as tg_ext

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

    def check_update(self, update: object) -> Optional[Union[bool, dict[str, list[any]]]]:
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
            self, cxt: tg_ext.CallbackContext, update: tg.Update, app: tg_ext.Application,
            check_result: Optional[Union[bool, dict[str, object]]]) -> None:
        """
        TODO
        """
        if not isinstance(update, tg.Update):
            return

        my_chat_member = update.my_chat_member
        if not my_chat_member:
            return

        chat = my_chat_member.chat
        if not chat:
            return

        chat_id = chat.id
        if not chat_id:
            return

        cxt.update({ "chat_id": chat_id, "chat_title": chat.title })