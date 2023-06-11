from __future__ import annotations

import datetime

# ==================================================================================================

class TelegramObject:
    """
    TODO
    """
    id: str

    def __init__(self, id: str = None) -> None:
        self.id = id

class Message(TelegramObject):
    """
    TODO
    """
    chat_id: int
    author_peer_type: str
    author_peer_id: str
    post_date: datetime.datetime
    edit_date: datetime.datetime
    text: str
    photo_id: str
    _photo: Photo = None
    video_id: str
    _video: Video = None
    _reactions: list[tuple]  # TODO
    num_views: int
    num_forwards: int
    num_replies: int
    group_id: str
    reply_to_msg_id: str
    forward_from_peer_type: str
    forward_from_peer_id: str

    def __init__(self, id: str = None, chat_id: int = None, author_peer_type: str = None,
                 author_peer_id: str = None, post_date: datetime.datetime = None,
                 edit_date: datetime.datetime = None, text: str = None, photo_id: str = None,
                 photo: Photo = None, video_id: str = None, video: Video = None,
                 reactions: list[tuple] = None, num_views: int = None, num_forwards: int = None,
                 num_replies: int = None, group_id: str = None, reply_to_msg_id: str = None,
                 forward_from_peer_type: str = None, forward_from_peer_id: str = None) -> None:
        """
        TODO
        """
        super().__init__(id)
        self.chat_id = chat_id
        self.author_peer_type = author_peer_type
        self.author_peer_id = author_peer_id
        self.post_date = post_date
        self.edit_date = edit_date
        self.text = text
        self.photo_id = photo_id
        self._photo = photo
        self.video_id = video_id
        self._video = video
        self._reactions = reactions
        self.num_views = num_views
        self.num_forwards = num_forwards
        self.num_replies = num_replies
        self.group_id = group_id
        self.reply_to_msg_id = reply_to_msg_id
        self.forward_from_peer_type = forward_from_peer_type
        self.forward_from_peer_id = forward_from_peer_id

    def __str__(self) -> str:
        """
        TODO
        """
        return f"Message(id: {self.id}; chat_id: {self.chat_id}; " \
               f"author_peer_type: {self.author_peer_type}; " \
               f"author_peer_id: {self.author_peer_id}; post_date: {self.post_date}; " \
               f"edit_date: {self.edit_date}; text: {repr(self.text)}; " \
               f"photo_id: {self.photo_id}; video_id: {repr(self.video_id)}; " \
               f"reactions: {self._reactions}; num_views: {self.num_views}; " \
               f"num_forwards: {self.num_forwards}; num_replies: {self.num_replies}; " \
               f"group_id: {self.group_id}; reply_to_msg_id: {self.reply_to_msg_id}; " \
               f"forward_from_peer_type: {self.forward_from_peer_type}; " \
               f"forward_from_peer_id: {self.forward_from_peer_id})"

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
    chat_id: int
    ref_id: int
    message_id: int
    author_peer_type: str
    author_peer_id: int
    post_date: datetime.datetime
    size: int
    width: int
    height: int
    md5: str
    _telethon_media_obj: any

    def __init__(self, id: str = None, chat_id: int = None, ref_id: int = None,
                 message_id: str = None, author_peer_type: str = None, author_peer_id: str = None,
                 post_date: datetime.datetime = None, size: int = None, width: int = None,
                 height: int = None, md5: int = None) -> None:
        """
        TODO
        """
        super().__init__(id)
        self.chat_id = chat_id
        self.ref_id = ref_id
        self.message_id = message_id
        self.author_peer_type = author_peer_type
        self.author_peer_id = author_peer_id
        self.post_date = post_date
        self.size = size
        self.width = width
        self.height = height
        self.md5 = md5
        self._telethon_media_obj = None

    def __str__(self) -> str:
        """
        TODO
        """
        return f"Photo(id: {self.id}; chat_id: {self.chat_id}; ref_id: {self.ref_id}; " \
               f"message_id: {self.message_id}; author_peer_type: {self.author_peer_type}; " \
               f"author_peer_id: {self.author_peer_id}; post_date: {self.post_date}; " \
               f"size: {self.size}; width: {self.width}; height: {self.height}; md5: {self.md5})"

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
    chat_id: int
    ref_id: int
    message_id: int
    author_peer_type: str
    author_peer_id: int
    post_date: datetime.datetime
    mime_type: str
    size: int
    duration: int
    width: int
    height: int
    thumb_md5: str
    _telethon_media_obj: any

    def __init__(self, id: str = None, chat_id: int = None, author_peer_type: str = None,
                 author_peer_id: str = None, post_date: datetime.datetime = None,
                 mime_type: str = None, size: int = None, duration: int = None, width: int = None,
                 height: int = None, thumb_md5: int = None) -> None:
        """
        TODO
        """
        super().__init__(id)
        self.chat_id = chat_id
        self.author_peer_type = author_peer_type
        self.author_peer_id = author_peer_id
        self.post_date = post_date
        self.mime_type = mime_type
        self.size = size
        self.duration = duration
        self.width = width
        self.height = height
        self.thumb_md5 = thumb_md5
        self._telethon_media_obj = None

    def __str__(self) -> str:
        """
        TODO
        """
        return f"Video(id: {self.id}; chat_id: {self.chat_id}; ref_id: {self.ref_id}; " \
               f"message_id: {self.message_id}; author_peer_type: {self.author_peer_type}; " \
               f"author_peer_id: {self.author_peer_id}; mime_type: {self.mime_type}; " \
               f"size: {self.size}; duration: {self.duration}; width: {self.width}; " \
               f"height: {self.height}; thumb_md5: {self.thumb_md5})"

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