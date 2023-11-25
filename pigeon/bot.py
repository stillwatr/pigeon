import telegram as tg
import telegram.ext as tg_ext
import tg_file_id.file_unique_id as tg_file_unique_id

import pigeon.handlers as handlers
import pigeon.log as log
import pigeon.models as models
import pigeon.utils as utils

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
        # self.app.add_handler(handlers.CommandHandler(self._handle_command))
        self.app.add_handler(handlers.MessageHandler(self._handle_message))
        # self.app.add_handler(tg_ext.CallbackQueryHandler(self._handle_callback_query))

        # self.log = logging.getLogger(__file__)
        # self.log.setLevel(logging.DEBUG)
        # ch = logging.StreamHandler()
        # ch.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s : %(message)s"))
        # self.log.addHandler(ch)

    def start(self):
        """
        TODO
        """
        self.app.run_polling()

    # ==============================================================================================
    # Handler methods.

    async def _handle_bot_added_to_chat(self, update: tg.Update, context: tg_ext.CallbackContext):
        """
        TODO
        """
        assert context, "no context given"
        await self.on_bot_added_to_chat(context.chat_id)

    async def on_bot_added_to_chat(self, chat_id: int):
        """
        TODO
        """
        pass

    # ----------------------------------------------------------------------------------------------

    async def _handle_command(self, update: tg.Update, context: tg_ext.CallbackContext):
        """
        TODO
        """
        assert context, "no context given"

        await self.on_command(
            cmd=context.cmd,
            args=context.args,
            chat_id=context.chat_id,
            from_chat_id=context.from_chat_id
        )

    async def on_command(self, cmd: str, args: list[str], chat_id: int, from_chat_id: int):
        """
        TODO
        """
        pass

    # ----------------------------------------------------------------------------------------------

    async def _handle_message(self, update: tg.Update, context: tg_ext.CallbackContext):
        """
        TODO
        """
        assert update, "no context given"

        log.error(update)

        # If the message was posted in a channel, the message is stored in update.channel_post,
        # otherwise it is stored in update.message.
        msg = update.channel_post or update.message
        if not msg:
            return

        message = models.Message()
        message.id = msg.message_id
        message.chat_id = msg.chat.id if msg.chat else None
        message.from_chat_id = self.get_from_chat_id(msg)
        message.from_chat_type = self.get_from_chat_type(msg)
        message.post_date = msg.date
        # msg.edit_date = message.edit_date  # TODO
        message.text = msg.text
        message.photo = await self.get_photo(msg, compute_hash=True)
        message.photo_id = message.photo.id if message.photo is not None else None
        message.video = await self.get_video(msg, compute_hash=True)
        message.video_id = message.video.id if message.video is not None else None
        message.group_id = msg.media_group_id
        message.reply_to_msg_id = msg.reply_to_message.message_id if msg.reply_to_message else None
        message.fwd_from_chat_id = self.get_fwd_from_chat_id(msg)
        message.fwd_from_chat_type = self.get_fwd_from_chat_type(msg)
        message.reply_to_msg_id = msg.reply_to_message.message_id if msg.reply_to_message else None

        log.error(message.photo)
        log.error(message.video)

        await self.on_message(message)

    async def on_message(self, msg: models.Message):
        """
        TODO
        """
        pass

    # ----------------------------------------------------------------------------------------------

    # async def _handle_callback_query(self, update: tg.Update, context: tg_ext.CallbackContext):
    #     """
    #     TODO
    #     """
    #     if not update:
    #         log.error("No update given.")
    #         return

    #     callback_query = update.callback_query
    #     if not callback_query:
    #         log.error("No callback query given.")
    #         return

    #     message = callback_query.message
    #     if not message:
    #         log.error("No message given.")
    #         return

    #     chat = message.chat
    #     if not chat:
    #         log.error("No chat given.")
    #         return

    #     from_user = callback_query.from_user
    #     if not from_user:
    #         log.error("No from user given.")
    #         return

    #     data = callback_query.data
    #     if not data:
    #         log.error("No data given.")
    #         return

    #     await self.on_callback_query(chat.id, message.id, from_user.id, data)

    #     await callback_query.answer()

    # async def on_callback_query(self, chat_id: int, message_id: int, user_id: int, data: any):
    #     """
    #     TODO
    #     """
    #     pass

    # ==============================================================================================
    # Send messages methods.

    # async def send_message(self,
    #                        chat_id: str,
    #                        text: str,
    #                        in_response_to: str = None,
    #                        inline_buttons: list[list[models.InlineMessageButton]] = None) -> None:
    #     """
    #     TODO
    #     """
    #     reply_markup = self.get_inline_keyboard_markup(inline_buttons)
    #     msg = await self.app.bot.send_message(chat_id,
    #                                           text,
    #                                           parse_mode=tg.constants.ParseMode.HTML,
    #                                           reply_to_message_id=in_response_to,
    #                                           reply_markup=reply_markup)
    #     return msg.message_id

    # async def send_photo(self,
    #                      chat_id: str,
    #                      photo,
    #                      caption: str = None,
    #                      in_response_to=None,
    #                      inline_buttons: list[list[models.InlineMessageButton]] = None) -> None:
    #     """
    #     TODO
    #     """
    #     reply_markup = self.get_inline_keyboard_markup(inline_buttons)
    #     msg = await self.app.bot.send_photo(chat_id,
    #                                         photo,
    #                                         caption=caption,
    #                                         parse_mode=tg.constants.ParseMode.HTML,
    #                                         reply_to_message_id=in_response_to,
    #                                         reply_markup=reply_markup)
    #     return msg.message_id

    # async def send_video(self,
    #                      chat_id: str,
    #                      video,
    #                      caption: str = None,
    #                      in_response_to=None,
    #                      inline_buttons: list[list[models.InlineMessageButton]] = None) -> None:
    #     """
    #     TODO
    #     """
    #     reply_markup = self.get_inline_keyboard_markup(inline_buttons)
    #     msg = await self.app.bot.send_video(chat_id,
    #                                         video,
    #                                         caption=caption,
    #                                         parse_mode=tg.constants.ParseMode.HTML,
    #                                         reply_to_message_id=in_response_to,
    #                                         reply_markup=reply_markup)
    #     return msg.message_id

    # # ============================================================================================
    # # Forward messages methods.

    # async def forward_message(self, message: models.Message, to_chat_id: str) -> None:
    #     """
    #     TODO
    #     """
    #     msg = await self.app.bot.forward_message(to_chat_id, message.chat_id, message.id)
    #     return msg.message_id

    # # ============================================================================================
    # # Delete messages methods.

    # async def delete_message(self, chat_id: str, message_id: str) -> None:
    #     """
    #     TODO
    #     """
    #     await self.app.bot.delete_message(chat_id, message_id)

    # ==============================================================================================
    # Scheduler methods.

    # def run_once(self, seconds_from_now: int, callback) -> None:
    #     """
    #     TODO
    #     """
    #     self.app.job_queue.run_once(callback, seconds_from_now)

    # ==============================================================================================
    # Logging methods.

    # async def debug(self, msg: str, send_to_chat_id: int = None) -> None:
    #     """
    #     TODO
    #     """
    #     self.log.debug(msg)
    #     if send_to_chat_id:
    #         await self.send_message(send_to_chat_id, msg)

    # async def error(self, msg: str, send_to_chat_id: int = None) -> None:
    #     """
    #     TODO
    #     """
    #     self.log.error(msg)
    #     if send_to_chat_id:
    #         await self.send_message(send_to_chat_id, msg)

    # ==============================================================================================
    # Helper methods.

    # async def convert_message(self, source: tg.Message, compute_media_hash: bool) -> models.Message:
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

    async def get_video(self, msg: tg.Message, compute_hash: bool = False) -> models.Video | None:
        """
        TODO
        """
        assert msg, "no message given"

        if not isinstance(msg, tg.Message):
            return

        if msg.video is None:
            return None

        if not isinstance(msg.video, tg.Video):
            return

        video = models.Video()
        video.id = tg_file_unique_id.FileUniqueId.from_unique_id(msg.video.file_unique_id).id
        video.mime_type = msg.video.mime_type
        video.duration = msg.video.duration
        video.size = msg.video.file_size
        video.width = msg.video.width
        video.height = msg.video.height

        # Compute the hash of the thumbnail.
        if compute_hash and msg.video.thumbnail:
            try:
                thumbnail = await self.app.bot.get_file(msg.video.thumbnail.file_id)
                thumbnail_bytes = await thumbnail.download_as_bytearray()
                video.thumb_hash = utils.compute_image_hash(thumbnail_bytes)
            except Exception as e:
                print("Could not compute image hash.", e)
                pass

        return video

    async def get_photo(self, msg: tg.Message, compute_hash: bool = False) -> models.Photo | None:
        """
        TODO
        """
        assert msg, "no message given"

        if not isinstance(msg, tg.Message):
            return None

        if msg.photo is None:
            return None

        if not isinstance(msg.photo, tuple):
            return None

        if len(msg.photo) == 0:
            return None

        p: tg.PhotoSize = msg.photo[-1]
        if not isinstance(p, tg.PhotoSize):
            return None

        photo = models.Photo()
        photo.id = tg_file_unique_id.FileUniqueId.from_unique_id(p.file_unique_id).id
        photo.height = p.height
        photo.width = p.width
        photo.size = p.file_size

        # Compute the hash of the photo.
        if compute_hash:
            try:
                file = await self.app.bot.get_file(p.file_id)
                photo_bytes = await file.download_as_bytearray()
                photo.hash = utils.compute_image_hash(photo_bytes)
            except Exception as e:
                print("Could not compute image hash.", e)
                pass

        return photo

    def get_from_chat_id(self, msg: tg.Message) -> int | None:
        """
        TODO
        """
        if msg.sender_chat:
            return msg.sender_chat.id
        if msg.from_user:
            return msg.from_user.id
        return None

    def get_from_chat_type(self, msg: tg.Message) -> str | None:
        """
        TODO
        """
        # TODO: Define it globally. Introduce an own enum or chat types.
        mapping: dict[str, str] = {
            tg.constants.ChatType.CHANNEL: "channel",
            tg.constants.ChatType.GROUP: "group",
            tg.constants.ChatType.SUPERGROUP: "group",
            tg.constants.ChatType.SENDER: "user"
        }

        if msg.sender_chat:
            return mapping.get(msg.sender_chat.type)
        if msg.from_user:
            return "user"
        return None

    def get_fwd_from_chat_id(self, msg: tg.Message) -> str | None:
        """
        TODO
        """
        # A user can hide his identity when forwarding one of his messages - in which case only
        # the user name is stored in msg.forward_sender_name.
        if msg.forward_sender_name:
            return msg.forward_sender_name
        if msg.forward_from:
            return str(msg.forward_from.id)
        if msg.forward_from_chat:
            return str(msg.forward_from_chat.id)
        if msg.forward_from_message_id:
            return str(msg.forward_from_message_id)
        return None

    def get_fwd_from_chat_type(self, msg: tg.Message) -> str | None:
        """
        TODO
        """
        # TODO: Define it globally. Introduce an own enum or chat types.
        mapping: dict[str, str] = {
            tg.constants.ChatType.CHANNEL: "channel",
            tg.constants.ChatType.GROUP: "group",
            tg.constants.ChatType.SUPERGROUP: "group",
            tg.constants.ChatType.SENDER: "user"
        }

        if msg.forward_from:
            return "user"
        if msg.forward_from_chat:
            return mapping.get(msg.forward_from_chat.type)
        return None
