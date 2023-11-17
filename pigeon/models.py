from __future__ import annotations

import datetime

# ==================================================================================================


class TelegramObject:
    """
    TODO
    """
    id: int

    def __init__(self, id: int | None = None) -> None:
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
            id: int | None = None,
            name: str | None = None,
            verified: bool | None = None,
            restricted: bool | None = None,
            restricted_reason: str | None = None) -> None:
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


class Message(TelegramObject):
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
    url: str
    callback_data: str | object

    def __init__(
            self,
            label: str,
            callback_data: str | object = None,
            url: str | None = None) -> None:
        """
        TODO
        """
        self.label = label
        self.url = url
        self.callback_data = callback_data
