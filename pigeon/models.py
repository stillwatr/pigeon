from __future__ import annotations

import datetime
import uuid

import pigeon.models

# ==================================================================================================


class TelegramEntity:
    """
    TODO
    """
    id: int

    def __init__(self, id: int | None = None) -> None:
        self.id = id

# ==================================================================================================


class ChatPermissions:
    """
    TODO
    """
    users_can_send_messages: bool
    users_can_send_polls: bool
    users_can_send_other_messages: bool
    users_can_add_web_page_previews: bool
    users_can_change_info: bool
    users_can_invite_users: bool
    users_can_pin_messages: bool
    users_can_manage_topics: bool
    users_can_send_audios: bool
    users_can_send_documents: bool
    users_can_send_photos: bool
    users_can_send_videos: bool
    users_can_send_video_notes: bool
    users_can_send_voice_notes: bool

    def __init__(
            self,
            users_can_send_messages: bool | None = None,
            users_can_send_polls: bool | None = None,
            users_can_send_other_messages: bool | None = None,
            users_can_add_web_page_previews: bool | None = None,
            users_can_change_info: bool | None = None,
            users_can_invite_users: bool | None = None,
            users_can_pin_messages: bool | None = None,
            users_can_manage_topics: bool | None = None,
            users_can_send_audios: bool | None = None,
            users_can_send_documents: bool | None = None,
            users_can_send_photos: bool | None = None,
            users_can_send_videos: bool | None = None,
            users_can_send_video_notes: bool | None = None,
            users_can_send_voice_notes: bool | None = None) -> None:
        self.users_can_send_messages = users_can_send_messages
        self.users_can_send_polls = users_can_send_polls
        self.users_can_send_other_messages = users_can_send_other_messages
        self.users_can_add_web_page_previews = users_can_add_web_page_previews
        self.users_can_change_info = users_can_change_info
        self.users_can_invite_users = users_can_invite_users
        self.users_can_pin_messages = users_can_pin_messages
        self.users_can_manage_topics = users_can_manage_topics
        self.users_can_send_audios = users_can_send_audios
        self.users_can_send_documents = users_can_send_documents
        self.users_can_send_photos = users_can_send_photos
        self.users_can_send_videos = users_can_send_videos
        self.users_can_send_video_notes = users_can_send_video_notes
        self.users_can_send_voice_notes = users_can_send_voice_notes

    def copy(self) -> ChatPermissions:
        """
        TODO
        """
        permissions = ChatPermissions()
        permissions.users_can_send_messages = self.users_can_send_messages
        permissions.users_can_send_polls = self.users_can_send_polls
        permissions.users_can_send_other_messages = self.users_can_send_other_messages
        permissions.users_can_add_web_page_previews = self.users_can_add_web_page_previews
        permissions.users_can_change_info = self.users_can_change_info
        permissions.users_can_invite_users = self.users_can_invite_users
        permissions.users_can_pin_messages = self.users_can_pin_messages
        permissions.users_can_manage_topics = self.users_can_manage_topics
        permissions.users_can_send_audios = self.users_can_send_audios
        permissions.users_can_send_documents = self.users_can_send_documents
        permissions.users_can_send_photos = self.users_can_send_photos
        permissions.users_can_send_videos = self.users_can_send_videos
        permissions.users_can_send_video_notes = self.users_can_send_video_notes
        permissions.users_can_send_voice_notes = self.users_can_send_voice_notes

        return permissions


class Chat(TelegramEntity):
    """
    TODO
    """
    name: str
    verified: bool
    restricted: bool
    restricted_reason: str

    def __init__(
            self,
            id: int | None = None,
            name: str | None = None,
            verified: bool | None = None,
            restricted: bool | None = None,
            restricted_reason: str | None = None,
            users_can_send_messages: bool | None = None,
            users_can_send_polls: bool | None = None,
            users_can_send_other_messages: bool | None = None,
            users_can_add_web_page_previews: bool | None = None,
            users_can_change_info: bool | None = None,
            users_can_invite_users: bool | None = None,
            users_can_pin_messages: bool | None = None,
            users_can_manage_topics: bool | None = None,
            users_can_send_audios: bool | None = None,
            users_can_send_documents: bool | None = None,
            users_can_send_photos: bool | None = None,
            users_can_send_videos: bool | None = None,
            users_can_send_video_notes: bool | None = None,
            users_can_send_voice_notes: bool | None = None) -> None:
        super().__init__(id)
        self.name = name
        self.verified = verified
        self.restricted = restricted
        self.restricted_reason = restricted_reason
        self.users_can_send_messages = users_can_send_messages
        self.users_can_send_polls = users_can_send_polls
        self.users_can_send_other_messages = users_can_send_other_messages
        self.users_can_add_web_page_previews = users_can_add_web_page_previews
        self.users_can_change_info = users_can_change_info
        self.users_can_invite_users = users_can_invite_users
        self.users_can_pin_messages = users_can_pin_messages
        self.users_can_manage_topics = users_can_manage_topics
        self.users_can_send_audios = users_can_send_audios
        self.users_can_send_documents = users_can_send_documents
        self.users_can_send_photos = users_can_send_photos
        self.users_can_send_videos = users_can_send_videos
        self.users_can_send_video_notes = users_can_send_video_notes
        self.users_can_send_voice_notes = users_can_send_voice_notes


class User(Chat):
    """
    TODO
    """
    first_name: str
    last_name: str
    user_name: str
    phone: str
    lang_code: str
    deleted: bool
    is_bot: bool

    def __init__(
            self,
            id: int | None = None,
            first_name: str | None = None,
            last_name: str | None = None,
            user_name: str | None = None,
            phone: str | None = None,
            lang_code: str | None = None,
            verified: bool | None = None,
            deleted: bool | None = None,
            is_bot: bool | None = None,
            restricted: bool | None = None,
            restricted_reason: str | None = None) -> None:
        super().__init__(id, user_name, verified, restricted, restricted_reason)
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.phone = phone
        self.lang_code = lang_code
        self.deleted = deleted
        self.is_bot = is_bot

    def __str__(self) -> str:
        """
        TODO
        """
        return "User(" \
               f"id: {self.id}; " \
               f"first_name: {self.first_name}; " \
               f"last_name: {self.last_name}; " \
               f"user_name: {self.user_name}; " \
               f"phone: {self.phone}; " \
               f"lang_code: {self.lang_code}; " \
               f"verified: {self.verified}; " \
               f"restricted: {self.restricted}; " \
               f"restricted_reason: {self.restricted_reason}; " \
               f"deleted: {self.deleted}; "\
               f"is_bot: {self.is_bot})"

    def __repr__(self) -> str:
        """
        TODO
        """
        return f"User(id: {self.id})"


class Group(Chat):
    """
    TODO
    """
    creation_date: datetime.datetime
    deactivated: bool

    def __init__(
            self,
            id: int | None = None,
            name: str | None = None,
            creation_date: datetime.datetime | None = None,
            deactivated: bool | None = None,
            verified: bool | None = None,
            restricted: bool | None = None,
            restricted_reason: str | None = None) -> None:
        super().__init__(id, name, verified, restricted, restricted_reason)
        self.creation_date = creation_date
        self.deactivated = deactivated

    def __str__(self) -> str:
        """
        TODO
        """
        return "Group(" \
               f"id: {self.id}; " \
               f"name: {self.name}; " \
               f"creation_date: {self.creation_date}; " \
               f"deactivated: {self.deactivated}; " \
               f"verified: {self.verified}; " \
               f"restricted: {self.restricted}; " \
               f"restricted_reason: {self.restricted_reason})"

    def __repr__(self) -> str:
        """
        TODO
        """
        return f"Group(id: {self.id})"


class Channel(Chat):
    """
    TODO
    """
    creation_date: datetime.datetime

    def __init__(
            self,
            id: int | None = None,
            name: str | None = None,
            creation_date: datetime.datetime | None = None,
            verified: bool | None = None,
            restricted: bool | None = None,
            restricted_reason: str | None = None) -> None:
        super().__init__(id, name, verified, restricted, restricted_reason)
        self.name = name
        self.creation_date = creation_date

    def __str__(self) -> str:
        """
        TODO
        """
        return "Channel(" \
               f"id: {self.id}; " \
               f"name: {self.name}; " \
               f"creation_date: {self.creation_date}; " \
               f"verified: {self.verified}; " \
               f"restricted: {self.restricted}; " \
               f"restricted_reason: {self.restricted_reason})"

    def __repr__(self) -> str:
        """
        TODO
        """
        return f"Channel(id: {self.id})"

# ==================================================================================================


class Message(TelegramEntity):
    """
    TODO
    """
    chat_id: int
    from_chat_id: int
    from_chat_type: str
    post_date: datetime.datetime
    edit_date: datetime.datetime
    status_message_type: str
    text: str
    photo_id: int
    photo: Photo
    video_id: int
    video: Video
    num_views: int
    num_forwards: int
    num_replies: int
    group_id: int
    reply_to_msg_id: int
    fwd_from_chat_id: str
    fwd_from_chat_type: str

    def __init__(
            self,
            id: int | None = None,
            chat_id: int | None = None,
            from_chat_id: int | None = None,
            from_chat_type: str | None = None,
            post_date: datetime.datetime | None = None,
            edit_date: datetime.datetime | None = None,
            status_message_type: str | None = None,
            text: str | None = None,
            photo_id: int | None = None,
            photo: Photo | None = None,
            video_id: int | None = None,
            video: Video | None = None,
            reactions: list[tuple] | None = None,
            num_views: int | None = None,
            num_forwards: int | None = None,
            num_replies: int | None = None,
            group_id: int | None = None,
            reply_to_msg_id: int | None = None,
            fwd_from_chat_id: str | None = None,
            fwd_from_chat_type: str | None = None) -> None:
        """
        TODO
        """
        super().__init__(id)
        self.chat_id = chat_id
        self.from_chat_id = from_chat_id
        self.from_chat_type = from_chat_type
        self.post_date = post_date
        self.edit_date = edit_date
        self.status_message_type = status_message_type
        self.text = text
        self.photo_id = photo_id
        self.photo = photo
        self.video_id = video_id
        self.video = video
        self.reactions = reactions
        self.num_views = num_views
        self.num_forwards = num_forwards
        self.num_replies = num_replies
        self.group_id = group_id
        self.reply_to_msg_id = reply_to_msg_id
        self.fwd_from_chat_id = fwd_from_chat_id
        self.fwd_from_chat_type = fwd_from_chat_type

    def __str__(self) -> str:
        """
        TODO
        """
        return "Message(" \
               f"id: {self.id}; " \
               f"chat_id: {self.chat_id}; " \
               f"from_chat_id: {self.from_chat_id}; " \
               f"from_chat_type: {self.from_chat_type}; " \
               f"post_date: {self.post_date}; " \
               f"edit_date: {self.edit_date}; " \
               f"status_message_type: {self.status_message_type}; " \
               f"text: {repr(self.text)}; " \
               f"photo_id: {self.photo_id}; " \
               f"video_id: {repr(self.video_id)}; " \
               f"reactions: {self.reactions}; " \
               f"num_views: {self.num_views}; " \
               f"num_forwards: {self.num_forwards}; " \
               f"num_replies: {self.num_replies}; " \
               f"group_id: {self.group_id}; " \
               f"reply_to_msg_id: {self.reply_to_msg_id}; " \
               f"fwd_from_chat_id: {self.fwd_from_chat_id}; " \
               f"fwd_from_chat_type: {self.fwd_from_chat_type})"

    def __repr__(self) -> str:
        """
        TODO
        """
        return f"Message(id: {self.id})"

# ==================================================================================================


class Command(Message):
    """
    TODO
    """
    command: str
    args: list[str]

    def __str__(self) -> str:
        """
        TODO
        """
        return "Command(" \
               f"id: {self.id}; " \
               f"chat_id: {self.chat_id}; " \
               f"from_chat_id: {self.from_chat_id}; " \
               f"from_chat_type: {self.from_chat_type}; " \
               f"post_date: {self.post_date}; " \
               f"command: {self.command}; " \
               f"args: {self.args})"

    def __repr__(self) -> str:
        """
        TODO
        """
        return f"Command(id: {self.id})"

# ==================================================================================================


class Photo(TelegramEntity):
    """
    TODO
    """
    size: int
    width: int
    height: int
    hash: int

    def __init__(
            self,
            id: int | None = None,
            size: int | None = None,
            width: int | None = None,
            height: int | None = None,
            hash: int | None = None) -> None:
        """
        TODO
        """
        super().__init__(id)
        self.size = size
        self.width = width
        self.height = height
        self.hash = hash

    def __str__(self) -> str:
        """
        TODO
        """
        return "Photo(" \
               f"id: {self.id}; " \
               f"size: {self.size}; " \
               f"width: {self.width}; " \
               f"height: {self.height}; " \
               f"hash: {self.hash})"

    def __repr__(self) -> str:
        """
        TODO
        """
        return f"Photo(id: {self.id})"

# ==================================================================================================


class Video(TelegramEntity):
    """
    TODO
    """
    mime_type: str
    size: int
    duration: int
    width: int
    height: int
    thumb_hash: int

    def __init__(
            self,
            id: int | None = None,
            mime_type: str | None = None,
            size: int | None = None,
            duration: int | None = None,
            width: int | None = None,
            height: int | None = None,
            thumb_hash: int | None = None) -> None:
        """
        TODO
        """
        super().__init__(id)
        self.mime_type = mime_type
        self.size = size
        self.duration = duration
        self.width = width
        self.height = height
        self.thumb_hash = thumb_hash

    def __str__(self) -> str:
        """
        TODO
        """
        return "Video(" \
               f"id: {self.id}; " \
               f"mime_type: {self.mime_type}; " \
               f"size: {self.size}; " \
               f"duration: {self.duration}; " \
               f"width: {self.width}; " \
               f"height: {self.height}; " \
               f"thumb_hash: {self.thumb_hash})"

    def __repr__(self) -> str:
        """
        TODO
        """
        return f"Video(id: {self.id})"

# ==================================================================================================


class InlineMessageButton():
    """
    TODO
    """
    label: str
    url: str | None
    callback_data: str | object | None

    def __init__(
            self,
            label: str,
            url: str | None = None,
            callback_data: str | object | None = None) -> None:
        """
        TODO
        """
        self.label = label
        self.url = url
        self.callback_data = callback_data


class BotAction:
    """
    TODO
    """
    name: str

    async def run(self, chat_id: int, params: dict = {}) -> None:
        """
        TODO
        """
        pass


class Callback:
    """
    TODO
    """
    id: str
    action_name: str
    chat_id: int
    params: dict
    authorization_type: str  # 'by_user_id'
    authorization_parties: list[str]

    def __init__(
            self,
            id: str | None = None,
            action: BotAction | None = None,
            chat_id: int | None = None,
            params: dict = {},
            authorization_type: str | None = None,
            authorization_parties: list[str] = []) -> None:
        """
        TODO
        """
        self.id = id if id is not None else uuid.uuid4()
        self.action_name = action.name if action is not None else None
        self.chat_id = chat_id
        self.params = params
        self.authorization_type = authorization_type
        self.authorization_parties = authorization_parties

    def __str__(self) -> str:
        """
        TODO
        """
        return "Callback(" \
               f"id: {self.id}; " \
               f"action_name: {self.action_name}; " \
               f"chat_id: {self.chat_id}; " \
               f"params: {self.params}; " \
               f"authorization_type: {self.authorization_type}; " \
               f"authorization_parties: {self.authorization_parties})"

    def __repr__(self) -> str:
        """
        TODO
        """
        return f"Callback(id: {self.id}, action: {self.action_name})"
