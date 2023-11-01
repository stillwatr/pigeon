from __future__ import annotations

import datetime

# ==================================================================================================


class TelegramObject:
    """
    TODO
    """
    id: int

    def __init__(self, id: int = None) -> None:
        self.id = id

# ==================================================================================================


class Chat(TelegramObject):
    """
    TODO
    """
    name: str
    verified: bool
    restricted: bool
    restricted_reason: str

    def __init__(
            self,
            id: int = None,
            name: str = None,
            verified: bool = None,
            restricted: bool = None,
            restricted_reason: str = None) -> None:
        super().__init__(id)
        self.name = name
        self.verified = verified
        self.restricted = restricted
        self.restricted_reason = restricted_reason


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
            id: int = None,
            first_name: str = None,
            last_name: str = None,
            user_name: str = None,
            phone: str = None,
            lang_code: str = None,
            verified: bool = None,
            deleted: bool = None,
            is_bot: bool = None,
            restricted: bool = None,
            restricted_reason: str = None) -> None:
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
            id: int = None,
            name: str = None,
            creation_date: datetime.datetime = None,
            deactivated: bool = None,
            verified: bool = None,
            restricted: bool = None,
            restricted_reason: str = None) -> None:
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
            id: int = None,
            name: str = None,
            creation_date: datetime.dateime = None,
            verified: bool = None,
            restricted: bool = None,
            restricted_reason: str = None) -> None:
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


class Message(TelegramObject):
    """
    TODO
    """
    chat_id: int
    from_chat: Chat
    post_date: datetime.datetime
    edit_date: datetime.datetime
    status_message_type: str
    text: str
    photo_id: int
    photo: Photo
    video_id: int
    video: Video
    reactions: list[tuple]  # TODO: Introduce model for reactions?
    num_views: int
    num_forwards: int
    num_replies: int
    group_id: str
    reply_to_msg_id: str
    forward_from_chat: Chat

    def __init__(
            self,
            id: int = None,
            chat_id: int = None,
            from_chat: Chat = None,
            post_date: datetime.datetime = None,
            edit_date: datetime.datetime = None,
            status_message_type: str = None,
            text: str = None,
            photo_id: int = None,
            photo: Photo = None,
            video_id: int = None,
            video: Video = None,
            reactions: list[tuple] = None,
            num_views: int = None,
            num_forwards: int = None,
            num_replies: int = None,
            group_id: str = None,
            reply_to_msg_id: str = None,
            forward_from_chat: Chat = None) -> None:
        """
        TODO
        """
        super().__init__(id)
        self.chat_id = chat_id
        self.from_chat = from_chat
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
        self.forward_from_chat = forward_from_chat

    def __str__(self) -> str:
        """
        TODO
        """
        return "Message(" \
               f"id: {self.id}; " \
               f"chat_id: {self.chat_id}; " \
               f"from_chat: {repr(self.from_chat)}; " \
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
               f"forward_from_chat: {repr(self.forward_from_chat)})"

    def __repr__(self) -> str:
        """
        TODO
        """
        return f"Message(id: {self.id})"

# ==================================================================================================


class Photo(TelegramObject):
    """
    TODO
    """
    size: int
    width: int
    height: int
    hash: int

    def __init__(
            self,
            id: int = None,
            size: int = None,
            width: int = None,
            height: int = None,
            hash: int = None) -> None:
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


class Video(TelegramObject):
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
            id: int = None,
            mime_type: str = None,
            size: int = None,
            duration: int = None,
            width: int = None,
            height: int = None,
            thumb_hash: int = None) -> None:
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
    url: str
    callback_data: str | object

    def __init__(self, label: str, callback_data: str | object = None, url: str = None) -> None:
        """
        TODO
        """
        self.label = label
        self.url = url
        self.callback_data = callback_data
