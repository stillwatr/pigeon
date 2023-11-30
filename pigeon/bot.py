import asyncio
import telegram as tg
import telegram.ext as tg_ext
import typing
import yaml

import pigeon.handlers as handlers
import pigeon.models as models
import pigeon.utils as utils
import pigeon.logging as logging

import pigeon.telegram_bot_entity_mapper as mapper

# ==================================================================================================


def action_name(name):
    def decorator(cls):
        cls.name = name
        return cls
    return decorator


def get_action(name: str) -> type[models.BotAction]:
    """
    TODO
    """
    subclass: type[models.BotAction]
    for subclass in models.BotAction.__subclasses__():
        if subclass.name == name:
            return subclass

# ==================================================================================================


class TelegramBot:
    """
    TODO
    """

    def __init__(self, token: str):
        """
        TODO
        """
        self.app: tg_ext.Application = tg_ext.ApplicationBuilder().token(token).build()
        self.app.add_handler(handlers.BotAddedToChatHandler(self, self._handle_bot_added_to_chat))
        self.app.add_handler(handlers.CommandHandler(self._handle_command))
        self.app.add_handler(handlers.MessageHandler(self._handle_message))
        self.app.add_handler(handlers.CallbackQueryHandler(self._handle_callback_query))

        self.entity_mapper = mapper.TelegramBotEntityMapper()

        self.log = logging.Log(__file__)
        self.log.set_level(logging.LogLevel.INFO)
        console_log_handler = logging.ConsoleLogHandler()
        console_log_handler.setLevel(logging.LogLevel.DEBUG)
        self.log.add_handler(console_log_handler)
        # telegram_log_handler = logging.TelegramLogHandler(self, 1139069550)  # TODO
        # telegram_log_handler.setLevel(logging.LogLevel.FOCUS)
        # self.log.add_handler(telegram_log_handler)

    def start(self):
        """
        TODO
        """
        self.app.run_polling()

    # ==============================================================================================

    async def get_name(self) -> int:
        """
        TODO
        """
        bot = await self.app.bot.get_me()
        return bot.username

    # ==============================================================================================
    # Handler methods.

    async def _handle_bot_added_to_chat(self, update: tg.Update, context: tg_ext.CallbackContext):
        """
        TODO
        """
        assert update, "no update given"
        assert context, "no context given"

        # FIXME: Implement a permission system.
        if update.my_chat_member.from_user.id != 1139069550:  # stillwatr
            return

        chat_id = getattr(context, "chat_id", None)
        if not isinstance(chat_id, int):
            # FIXME: Exception handling.
            return

        chat_title = getattr(context, "chat_title", None)
        if not isinstance(chat_title, str):
            # FIXME: Exception handling.
            return

        await self.on_bot_added_to_chat(chat_id, chat_title)

    async def on_bot_added_to_chat(self, chat_id: int, chat_title: str) -> None:
        """
        TODO
        """
        pass

    # ----------------------------------------------------------------------------------------------

    async def _handle_command(self, update: tg.Update, context: tg_ext.CallbackContext):
        """
        TODO
        """
        assert update, "no update given"

        # FIXME: Implement a permission system.
        if update.message.from_user.id != 1139069550:  # stillwatr
            return

        # If the message was posted in a channel, the message is stored in
        # update.channel_post, otherwise it is stored in update.message.
        entity = update.channel_post or update.message
        if not isinstance(entity, tg.Message):
            # FIXME: Exception handling.
            return

        try:
            command = self.entity_mapper.map_command(entity)
        except Exception as e:
            # FIXME: Exception handling.
            self.log.info(e)
            return

        await self.on_command(command)

    async def on_command(self, command: models.Command):
        """
        TODO
        """
        pass

    # ----------------------------------------------------------------------------------------------

    async def _handle_message(self, update: tg.Update, context: tg_ext.CallbackContext):
        """
        TODO
        """
        assert update, "no update given"

        # If the message was posted in a channel, the message is stored in
        # update.channel_post, otherwise it is stored in update.message.
        entity = update.channel_post or update.message
        if not isinstance(entity, tg.Message):
            # FIXME: Exception handling.
            return

        try:
            message = self.entity_mapper.map_message(entity)
        except Exception:
            # FIXME: Exception handling.
            return

        # If the message contains a photo, compute a hash of the photo.
        if message.photo:
            try:
                message.photo.hash = await self.compute_photo_hash(entity)
            except Exception:
                # FIXME: Exception handling.
                pass

        # If the message contains a video, compute a hash of the thumbnail of the video.
        if message.video:
            try:
                message.video.thumb_hash = await self.compute_video_thumb_hash(entity)
            except Exception:
                # FIXME: Exception handling.
                pass

        await self.on_message(message)

    async def on_message(self, message: models.Message):
        """
        TODO
        """
        pass

    # ----------------------------------------------------------------------------------------------
    # Methods related to callbacks.

    async def _handle_callback_query(self, update: tg.Update, context: tg_ext.CallbackContext):
        """
        TODO
        """
        assert update, "no update given"

        callback_query = update.callback_query
        if not isinstance(callback_query, tg.CallbackQuery):
            # FIXME: Exception handling.
            return

        # FIXME: Implement a permission system.
        if update.callback_query.from_user.id != 1139069550:  # stillwatr
            await callback_query.answer()
            return

        callback_id = callback_query.data
        if callback_id is None:
            # FIXME: Exception handling.
            await callback_query.answer()
            return

        message = callback_query.message
        if not isinstance(message, tg.Message):
            # FIXME: Exception handling.
            await callback_query.answer()
            return

        await self.on_callback_query(message.chat_id, callback_id)
        # TODO: Answer the callback query in the handlers? To specify inividual response texts?
        await callback_query.answer()

    async def on_callback_query(self, chat_id: int, callback_id: str) -> None:
        """
        TODO
        """
        pass

    # ==============================================================================================
    # TODO: Maybe move the following two methods into an util file.

    async def compute_photo_hash(self, message: tg.Message) -> int:
        """
        TODO
        """
        if not isinstance(message, tg.Message):
            raise ValueError("no message given")

        if not isinstance(message.photo, tuple):
            raise ValueError("no photo given")

        if len(message.photo) == 0:
            raise ValueError("no photo given")

        photo: tg.PhotoSize = message.photo[-1]
        if not isinstance(photo, tg.PhotoSize):
            raise ValueError("no photo given")

        file = await self.app.bot.get_file(photo.file_id)
        file_bytes = await file.download_as_bytearray()

        return utils.compute_image_hash(file_bytes)

    async def compute_video_thumb_hash(self, message: tg.Message) -> int:
        """
        TODO
        """
        if not isinstance(message, tg.Message):
            raise ValueError("no message given")

        if not isinstance(message.video, tg.Video):
            raise ValueError("no video given")

        # Compute the hash of the thumbnail.
        if not message.video.thumbnail:
            raise ValueError("no thumbnail given")

        file = await self.app.bot.get_file(message.video.thumbnail.file_id)
        file_bytes = await file.download_as_bytearray()

        return utils.compute_image_hash(file_bytes)

    # ==============================================================================================
    # Send messages methods.

    async def send_message(
            self,
            to_chat_id: int,
            text: str,
            in_response_to: str | None = None,
            inline_buttons: list[list[models.InlineMessageButton]] | None = None) -> models.Message:
        """
        TODO
        """
        # reply_markup = self.get_inline_keyboard_markup(inline_buttons)
        msg = await self.app.bot.send_message(
            to_chat_id,
            text,
            parse_mode=tg.constants.ParseMode.HTML,
            reply_to_message_id=in_response_to
            # reply_markup=reply_markup
        )
        return self.entity_mapper.map_message(msg)

    async def send_message_from_template(
            self,
            template_path: str,
            to_chat_id: int,
            in_response_to: str | None = None,
            **kwargs) -> models.Message:
        assert template_path is not None, "no template_path given"
        assert to_chat_id is not None, "no to_chat_id given"

        # Read the template file and replace the contained placeholders.
        with open(template_path, "r") as stream:
            template_str = stream.read().format_map(dict(kwargs))

        # Parse the template.
        template = yaml.safe_load(template_str)

        message = template.get("message")
        if message is None:
            raise ValueError("the template does not contain a 'message' section")

        text = message.get("text")
        video = message.get("video")
        keyboard = self.parse_keyboard_template(message)

        if video:
            self.log.info(f"Sending video: {to_chat_id}, {video}")
            msg = await self.app.bot.send_video(
                chat_id=to_chat_id,
                video=video,
                caption=text,
                parse_mode=tg.constants.ParseMode.HTML,
                reply_to_message_id=in_response_to,
                reply_markup=keyboard
            )
        else:
            msg = await self.app.bot.send_message(
                to_chat_id,
                text=text,
                parse_mode=tg.constants.ParseMode.HTML,
                reply_to_message_id=in_response_to,
                reply_markup=keyboard
            )

        return self.entity_mapper.map_message(msg)

    # TODO: Move this to a parser class.
    def parse_keyboard_template(self, message_template):
        """
        TODO
        """
        if message_template is None:
            return None

        keyboard_template = message_template.get("keyboard")
        if keyboard_template is None:
            return None

        keyboard = []
        for row in keyboard_template:
            keyboard_row = []
            for button in row:
                button_type = button.get("type")
                button_label = button.get("label")

                if button_type == "url":
                    keyboard_row.append(tg.InlineKeyboardButton(
                        text=button_label,
                        url=button.get("url")
                    ))
                elif button_type == "callback":
                    keyboard_row.append(tg.InlineKeyboardButton(
                        text=button_label,
                        callback_data=button.get("callback_id")
                    ))

            keyboard.append(keyboard_row)

        return tg.InlineKeyboardMarkup(keyboard)

    async def send_photo(
            self,
            to_chat_id: str,
            photo: typing.Any,
            caption: str | None = None,
            in_response_to: str | None = None,
            inline_buttons: list[list[models.InlineMessageButton]] | None = None) -> models.Message:
        """
        TODO
        """
        # reply_markup = self.get_inline_keyboard_markup(inline_buttons)
        msg = await self.app.bot.send_photo(
            to_chat_id,
            photo,
            caption=caption,
            parse_mode=tg.constants.ParseMode.HTML,
            reply_to_message_id=in_response_to,
            # reply_markup=reply_markup
        )

        return self.entity_mapper.map_message(msg)

    async def send_video(
            self,
            to_chat_id: str,
            video: typing.Any,
            caption: str | None = None,
            in_response_to: str | None = None,
            inline_buttons: list[list[models.InlineMessageButton]] | None = None) -> models.Message:
        """
        TODO
        """
        # reply_markup = self.get_inline_keyboard_markup(inline_buttons)
        msg = await self.app.bot.send_video(
            to_chat_id=to_chat_id,
            video=video,
            caption=caption,
            parse_mode=tg.constants.ParseMode.HTML,
            reply_to_message_id=in_response_to,
            # reply_markup=reply_markup
        )

        return self.entity_mapper.map_message(msg)

    # ==============================================================================================
    # Chat permissions.

    async def get_chat_permissions(self, chat_id: int) -> models.ChatPermissions:
        """
        TODO
        """
        assert chat_id is not None, "no chat id given"

        chat: tg.Chat = await self.app.bot.get_chat(chat_id)
        return models.ChatPermissions(
            users_can_send_messages=chat.permissions.can_send_messages,
            users_can_send_polls=chat.permissions.can_send_polls,
            users_can_send_other_messages=chat.permissions.can_send_other_messages,
            users_can_add_web_page_previews=chat.permissions.can_add_web_page_previews,
            users_can_change_info=chat.permissions.can_change_info,
            users_can_invite_users=chat.permissions.can_invite_users,
            users_can_pin_messages=chat.permissions.can_pin_messages,
            users_can_manage_topics=chat.permissions.can_manage_topics,
            users_can_send_audios=chat.permissions.can_send_audios,
            users_can_send_documents=chat.permissions.can_send_documents,
            users_can_send_photos=chat.permissions.can_send_photos,
            users_can_send_videos=chat.permissions.can_send_videos,
            users_can_send_video_notes=chat.permissions.can_send_video_notes,
            users_can_send_voice_notes=chat.permissions.can_send_voice_notes
        )

    async def set_chat_permissions(self, chat_id: int, permissions: models.ChatPermissions) -> None:
        """
        TODO
        """
        assert chat_id is not None, "no chat id given"
        assert permissions is not None, "no permissions given"

        await self.app.bot.set_chat_permissions(chat_id, tg.ChatPermissions(
            can_send_messages=permissions.users_can_send_messages,
            can_send_polls=permissions.users_can_send_polls,
            can_send_other_messages=permissions.users_can_send_other_messages,
            can_add_web_page_previews=permissions.users_can_add_web_page_previews,
            can_change_info=permissions.users_can_change_info,
            can_invite_users=permissions.users_can_invite_users,
            can_pin_messages=permissions.users_can_pin_messages,
            can_manage_topics=permissions.users_can_manage_topics,
            can_send_audios=permissions.users_can_send_audios,
            can_send_documents=permissions.users_can_send_documents,
            can_send_photos=permissions.users_can_send_photos,
            can_send_videos=permissions.users_can_send_videos,
            can_send_video_notes=permissions.users_can_send_video_notes,
            can_send_voice_notes=permissions.users_can_send_voice_notes
        ), use_independent_chat_permissions=True)

    # ==============================================================================================
    # Forward messages methods.

    async def forward_message(self, message: models.Message, to_chat_id: str) -> None:
        """
        TODO
        """
        msg = await self.app.bot.forward_message(to_chat_id, message.chat_id, message.id)
        return msg.message_id

    # ==============================================================================================
    # Methods to delete messages.

    async def delete_messages(self, messages: list[models.Message]) -> None:
        """
        TODO
        """
        await asyncio.gather(*[self.delete_message_by_id(m.chat_id, m.id) for m in messages])

    async def delete_message(self, message: models.Message) -> None:
        """
        TODO
        """
        await self.delete_message_by_id(message.chat_id, message.id)

    async def delete_messages_by_ids(self, chat_id: int, message_ids: list[int]) -> None:
        """
        TODO
        """
        await asyncio.gather(*[self.delete_message_by_id(chat_id, id) for id in message_ids])

    async def delete_message_by_id(self, chat_id: int, message_id: int) -> None:
        """
        TODO
        """
        await self.app.bot.delete_message(chat_id, message_id)

    # ==============================================================================================
    # Scheduler methods.

    def run_once(self, seconds_from_now: int, callback) -> None:
        """
        TODO
        """
        self.app.job_queue.run_once(callback, seconds_from_now)

    # ==============================================================================================
    # Helper methods.

    # ync def convert_message(self, source: tg.Message, compute_media_hash: bool) -> models.Message:
    #     """
    #     TODO
    #     """
    #     if source is None:
    #         return
    #     if not isinstance(source, tg.Message):
    #         return

    #     message = models.Message()
    #     message.id = source.message_id
    #     message.chat_id = source.chat_id
    #     message.post_date = source.date
    #     message.edit_date = source.edit_date
    #     message.text = source.text
    #     message.num_views = 0  # TODO
    #     message.num_forwards = 0  # TODO
    #     message.num_replies = 0  # TODO
    #     message.group_id = 0  # TODO
    #     message._reactions = []  # TODO

    #     # Determine the author.
    #     if source.sender_chat:
    #         if source.sender_chat.type == "group":
    #             message.author_peer_type = "group"
    #         elif source.sender_chat.type == "supergroup":
    #             message.author_peer_type = "group"
    #         elif source.sender_chat.type == "channel":
    #             message.author_peer_type = "channel"
    #         else:
    #             message.author_peer_type = "user"
    #         message.author_peer_id = source.sender_chat.id
    #     elif source.from_user:
    #         message.author_peer_type = "user"
    #         message.author_peer_id = source.from_user.id

    #     # If the message contains a photo, extract it.
    #     message._photo = await self.get_photo(source, compute_hash=compute_media_hash)
    #     message.photo_id = message._photo.id if message._photo is not None else None

    #     # If the message contains a video, extract it.
    #     message._video = await self.get_video(source, compute_thumb_hash=compute_media_hash)
    #     message.video_id = message._video.id if message._video is not None else None

    #     # If the message is a reply to another message, determine the id of that message.
    #     if source.reply_to_message:
    #         message.reply_to_msg_id = source.reply_to_message.message_id

    #     # If the message was forwarded, determine from which peer it was forwarded .
    #     if source.forward_from_chat:
    #         if source.forward_from_chat.type == "group":
    #             message.forward_from_peer_type = "group"
    #         elif source.forward_from_chat.type == "supergroup":
    #             message.forward_from_peer_type = "group"
    #         elif source.forward_from_chat.type == "channel":
    #             message.forward_from_peer_type = "channel"
    #         else:
    #             message.forward_from_peer_type = "user"
    #         message.forward_from_peer_id = source.forward_from_chat.id
    #     elif source.forward_from:
    #         message.forward_from_peer_type = "user"
    #         message.forward_from_peer_id = source.forward_from.id
    #     elif source.forward_sender_name:
    #         message.forward_from_peer_type = "user"

    #     # Check if the message is a status message.
    #     if source.new_chat_members:
    #         message.status_message_type = "new_chat_members"
    #         message.text = source.new_chat_members
    #     if source.left_chat_member:
    #         message.status_message_type = "left_chat_member"
    #         message.text = source.left_chat_member
    #     if source.new_chat_title:
    #         message.status_message_type = "new_chat_title"
    #         message.text = source.new_chat_title
    #     if source.new_chat_photo:
    #         message.status_message_type = "new_chat_photo"
    #         message.text = source.new_chat_photo
    #     if source.delete_chat_photo:
    #         message.status_message_type = "delete_chat_photo"
    #         message.text = source.delete_chat_photo
    #     if source.group_chat_created:
    #         message.status_message_type = "chat_created"
    #         message.text = source.group_chat_created
    #     if source.supergroup_chat_created:
    #         message.status_message_type = "chat_created"
    #         message.text = source.supergroup_chat_created
    #     if source.channel_chat_created:
    #         message.status_message_type = "chat_created"
    #         message.text = source.channel_chat_created
    #     if source.message_auto_delete_timer_changed:
    #         message.status_message_type = "message_auto_delete_timer_changed"
    #         message.text = source.message_auto_delete_timer_changed
    #     if source.migrate_from_chat_id:
    #         message.status_message_type = "migrate_from_chat_id"
    #         message.text = source.migrate_from_chat_id
    #     if source.migrate_to_chat_id:
    #         message.status_message_type = "migrate_to_chat_id"
    #         message.text = source.migrate_to_chat_id
    #     if source.pinned_message:
    #         message.status_message_type = "pinned_message"
    #         message.text = source.pinned_message
    #     if source.connected_website:
    #         message.status_message_type = "connected_website"
    #         message.text = source.connected_website
    #     if source.proximity_alert_triggered:
    #         message.status_message_type = "proximity_alert_triggered"
    #         message.text = source.proximity_alert_triggered
    #     if source.video_chat_scheduled:
    #         message.status_message_type = "video_chat_scheduled"
    #         message.text = source.video_chat_scheduled
    #     if source.video_chat_started:
    #         message.status_message_type = "video_chat_started"
    #         message.text = source.video_chat_started
    #     if source.video_chat_ended:
    #         message.status_message_type = "video_chat_ended"
    #         message.text = source.video_chat_ended
    #     if source.video_chat_participants_invited:
    #         message.status_message_type = "video_chat_participants_invited"
    #         message.text = source.video_chat_participants_invited
    #     if source.web_app_data:
    #         message.status_message_type = "web_app_data"
    #         message.text = source.web_app_data
    #     if source.forum_topic_created:
    #         message.status_message_type = "forum_topic_created"
    #         message.text = source.forum_topic_created
    #     if source.forum_topic_closed:
    #         message.status_message_type = "forum_topic_closed"
    #         message.text = source.forum_topic_closed
    #     if source.forum_topic_reopened:
    #         message.status_message_type = "forum_topic_reopened"
    #         message.text = source.forum_topic_reopened
    #     if source.forum_topic_edited:
    #         message.status_message_type = "forum_topic_edited"
    #         message.text = source.forum_topic_edited
    #     if source.general_forum_topic_hidden:
    #         message.status_message_type = "general_forum_topic_hidden"
    #         message.text = source.general_forum_topic_hidden
    #     if source.general_forum_topic_unhidden:
    #         message.status_message_type = "general_forum_topic_unhidden"
    #         message.text = source.general_forum_topic_unhidden
    #     if source.write_access_allowed:
    #         message.status_message_type = "write_access_allowed"
    #         message.text = source.write_access_allowed
    #     if source.user_shared:
    #         message.status_message_type = "user_shared"
    #         message.text = source.user_shared
    #     if source.chat_shared:
    #         message.status_message_type = "chat_shared"
    #         message.text = source.chat_shared

    #     return message

    # def get_inline_keyboard_markup(
    #         self,
    #         inline_buttons: list[list[models.InlineMessageButton]]) -> tg.InlineKeyboardMarkup:
    #     """
    #     TODO
    #     """
    #     if inline_buttons is None:
    #         return

    #     keyboard = []

    #     for inline_button_row in inline_buttons:
    #         keyboard_row = []
    #         for inline_button in inline_button_row:
    #             keyboard_row.append(
    #                 tg.InlineKeyboardButton(
    #                     text=inline_button.label,
    #                     url=inline_button.url,
    #                     callback_data=inline_button.callback_data
    #                 )
    #             )
    #         keyboard.append(keyboard_row)

    #     return tg.InlineKeyboardMarkup(keyboard)
