import telegram as tg
import tg_file_id.file_unique_id

import pigeon.models

# ==================================================================================================

CHAT_TYPE_MAPPING: dict[str, str] = {
    tg.constants.ChatType.CHANNEL: "channel",
    tg.constants.ChatType.GROUP: "group",
    tg.constants.ChatType.SUPERGROUP: "group",
    tg.constants.ChatType.SENDER: "user"
}

# ==================================================================================================


class TelegramBotEntityMapper:
    """
    TODO
    """

    def map_message(self, entity: tg.Message) -> pigeon.models.Message:
        """
        TODO
        """
        message = pigeon.models.Message()
        message.id = entity.message_id
        message.chat_id = entity.chat.id if entity.chat else None
        message.from_chat_id = self._get_from_chat_id(entity)
        message.from_chat_type = self._get_from_chat_type(entity)
        message.post_date = entity.date
        # msg.edit_date = message.edit_date  # TODO
        message.text = entity.text
        message.photo = self.map_photo(entity.photo[-1] if len(entity.photo) > 0 else None)
        message.photo_id = message.photo.id if message.photo is not None else None
        message.video = self.map_video(entity.video)
        message.video_id = message.video.id if message.video is not None else None
        message.group_id = entity.media_group_id
        reply_to_message = entity.reply_to_message
        message.reply_to_msg_id = reply_to_message.message_id if reply_to_message else None
        try:
            message.fwd_from_chat_id = self._get_fwd_from_chat_id(entity)
            message.fwd_from_chat_type = self._get_fwd_from_chat_type(entity)
        except Exception:
            # TODO
            pass

        # Check if the message is a status message.
        if entity.new_chat_members:
            message.status_message_type = "new_chat_members"
        if entity.left_chat_member:
            message.status_message_type = "left_chat_member"
        if entity.new_chat_title:
            message.status_message_type = "new_chat_title"
        if entity.new_chat_photo:
            message.status_message_type = "new_chat_photo"
        if entity.delete_chat_photo:
            message.status_message_type = "delete_chat_photo"
        if entity.group_chat_created:
            message.status_message_type = "chat_created"
        if entity.supergroup_chat_created:
            message.status_message_type = "chat_created"
        if entity.channel_chat_created:
            message.status_message_type = "chat_created"
        if entity.message_auto_delete_timer_changed:
            message.status_message_type = "message_auto_delete_timer_changed"
        if entity.migrate_from_chat_id:
            message.status_message_type = "migrate_from_chat_id"
        if entity.migrate_to_chat_id:
            message.status_message_type = "migrate_to_chat_id"
        if entity.pinned_message:
            message.status_message_type = "pinned_message"
        if entity.connected_website:
            message.status_message_type = "connected_website"
        if entity.proximity_alert_triggered:
            message.status_message_type = "proximity_alert_triggered"
        if entity.video_chat_scheduled:
            message.status_message_type = "video_chat_scheduled"
        if entity.video_chat_started:
            message.status_message_type = "video_chat_started"
        if entity.video_chat_ended:
            message.status_message_type = "video_chat_ended"
        if entity.video_chat_participants_invited:
            message.status_message_type = "video_chat_participants_invited"
        if entity.web_app_data:
            message.status_message_type = "web_app_data"
        if entity.forum_topic_created:
            message.status_message_type = "forum_topic_created"
        if entity.forum_topic_closed:
            message.status_message_type = "forum_topic_closed"
        if entity.forum_topic_reopened:
            message.status_message_type = "forum_topic_reopened"
        if entity.forum_topic_edited:
            message.status_message_type = "forum_topic_edited"
        if entity.general_forum_topic_hidden:
            message.status_message_type = "general_forum_topic_hidden"
        if entity.general_forum_topic_unhidden:
            message.status_message_type = "general_forum_topic_unhidden"
        if entity.write_access_allowed:
            message.status_message_type = "write_access_allowed"
        if entity.users_shared:
            message.status_message_type = "user_shared"
        if entity.chat_shared:
            message.status_message_type = "chat_shared"

        return message

    def map_command(self, entity: tg.Message) -> pigeon.models.Command:
        """
        TODO
        """
        command = pigeon.models.Command()
        command.id = entity.message_id
        command.chat_id = entity.chat.id if entity.chat else None
        command.from_chat_id = self._get_from_chat_id(entity)
        command.from_chat_type = self._get_from_chat_type(entity)
        command.post_date = entity.date
        # msg.edit_date = message.edit_date  # TODO
        command.text = entity.text
        command.command = entity.text.split()[0][1:] if entity.text is not None else None
        command.args = entity.text.split()[1:] if entity.text is not None else None
        command.photo = self.map_photo(entity.photo[-1] if len(entity.photo) > 0 else None)
        command.photo_id = command.photo.id if command.photo is not None else None
        command.video = self.map_video(entity.video)
        command.video_id = command.video.id if command.video is not None else None
        command.group_id = entity.media_group_id
        reply_to_message = entity.reply_to_message
        command.reply_to_msg_id = reply_to_message.message_id if reply_to_message else None
        try:
            command.fwd_from_chat_id = self._get_fwd_from_chat_id(entity)
            command.fwd_from_chat_type = self._get_fwd_from_chat_type(entity)
        except Exception:
            # TODO
            pass

        return command

    def map_video(self, entity: tg.Video) -> pigeon.models.Video:
        """
        TODO
        """
        if not isinstance(entity, tg.Video):
            return None

        video = pigeon.models.Video()
        video.id = tg_file_id.file_unique_id.FileUniqueId.from_unique_id(entity.file_unique_id).id
        video.mime_type = entity.mime_type
        video.duration = entity.duration
        video.size = entity.file_size
        video.width = entity.width
        video.height = entity.height

        return video

    def map_photo(self, entity: tg.PhotoSize) -> pigeon.models.Photo:
        """
        TODO
        """
        if not isinstance(entity, tg.PhotoSize):
            return None

        photo = pigeon.models.Photo()
        photo.id = tg_file_id.file_unique_id.FileUniqueId.from_unique_id(entity.file_unique_id).id
        photo.height = entity.height
        photo.width = entity.width
        photo.size = entity.file_size

        return photo

    # ==============================================================================================

    def _get_from_chat_id(self, msg: tg.Message) -> int | None:
        """
        TODO
        """
        if msg.sender_chat:
            return msg.sender_chat.id
        if msg.from_user:
            return msg.from_user.id
        return None

    def _get_from_chat_type(self, msg: tg.Message) -> str | None:
        """
        TODO
        """
        if msg and msg.sender_chat:
            return CHAT_TYPE_MAPPING.get(msg.sender_chat.type)
        if msg and msg.from_user:
            return "user"
        return None

    def _get_fwd_from_chat_id(self, msg: tg.Message) -> str | None:
        """
        TODO
        """
        # A user can hide his identity when forwarding one of his messages - in which case only
        # the user name is stored in msg.forward_sender_name.
        if msg and msg.forward_sender_name:
            return msg.forward_sender_name
        if msg and msg.forward_from:
            return str(msg.forward_from.id)
        if msg and msg.forward_from_chat:
            return str(msg.forward_from_chat.id)
        if msg and msg.forward_from_message_id:
            return str(msg.forward_from_message_id)
        return None

    def _get_fwd_from_chat_type(self, msg: tg.Message) -> str | None:
        """
        TODO
        """
        if msg and msg.forward_from_chat:
            return CHAT_TYPE_MAPPING.get(msg.forward_from_chat.type)
        if msg and msg.forward_from:
            return "user"
        return None
