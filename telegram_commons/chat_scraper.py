from __future__ import annotations

import hashlib
import telethon

from telethon.types import TypePhotoSize, PhotoSize, PhotoSizeProgressive

from telegram_commons.models import Message, Photo, Video
import telegram_commons.utils as utils

# ==================================================================================================

# TODO: If dir 'sessions' does not exist, an exception is thrown.
# DEFAULT_TELETHON_SESSION: str = "sessions/telegram-chat-scraper"
DEFAULT_TELETHON_SESSION: str = "telegram-chat-scraper"


class TelegramChatScraper:
    """
    TODO
    """

    def __init__(self, telethon_api_id: int, telethon_api_hash: str) -> None:
        """
        TODO
        """
        self.client: telethon.TelegramClient = telethon.TelegramClient(
            session  = DEFAULT_TELETHON_SESSION,
            api_id   = telethon_api_id,
            api_hash = telethon_api_hash
        )

    async def start(self):
        """
        TODO
        """
        # Start the Telethon client.
        try:
            await self.client.start()
        except Exception as e:
            raise RuntimeError(f"Could not start Telethon client.", e)

        # Get the groups and channels of which the user is a member. This is necessary to later
        # access a group/chat by id, see https://docs.telethon.dev/en/stable/concepts/entities.html.
        try:
            await self.client.get_dialogs()
        except Exception as e:
            raise RuntimeError(f"Could not get groups and channels of the user.", e)

    async def get_messages(self, chat_id: str, compute_media_md5: bool = False) -> list[Message]:
        """
        TODO
        """
        assert chat_id is not None, "No chat id given."

        if not self.client.is_connected():
            await self.start()

        messages: list[Message] = []

        # Iterate through the messages of the specified chat. Store the information about a message
        # in a `models.Message` object and add the object to the result list.
        # NOTE: Passing `reverse=True` to iter_messages() sorts the messages from old to new.
        async for msg in self.client.iter_messages(chat_id, reverse=True):
            # Ignore all non-messages.
            if not isinstance(msg, telethon.types.Message):
                continue

            message = Message()
            message.id = msg.id
            message.chat_id = chat_id
            message.author_peer_type, message.author_peer_id = await self._get_from_peer(chat_id, msg)
            message.post_date = msg.date
            message.edit_date = msg.edit_date
            message.text = msg.message
            message._photo = await self._get_photo(msg, compute_media_md5)
            message.photo_id = message._photo.id if message._photo.id is not None else None
            message._video = await self._get_video(msg, compute_media_md5)
            message.video_id = message._video.id if message._video.id is not None else None
            message._reactions = self._get_reactions(msg)
            message.num_views = msg.views if msg.views is not None else 0
            message.num_forwards = msg.forwards if msg.forwards is not None else 0
            message.num_replies = msg.replies.replies if msg.replies is not None else 0
            message.group_id = msg.grouped_id

            # Check if the message is a reply to another message in the same chat.
            if msg.reply_to is not None:
                message.reply_to_msg_id = msg.reply_to.reply_to_msg_id

            # Check if the message was forwarded from another chat.
            if msg.fwd_from is not None:
                message.forward_from_peer_type, message.forward_from_peer_id = \
                    await self._get_from_peer(chat_id, msg.fwd_from)

            messages.append(message)

        return messages

    async def get_photos(self, chat_id: str, compute_md5: bool = False) -> list[Photo]:
        """
        TODO
        """
        assert chat_id is not None, "No chat id given."

        if not self.client.is_connected():
            await self.start()

        photos: list[Photo] = []

        # Iterate through the messages of the specified chat. If the current message contains a
        # photo, store the information about the photo in a `models.Photo` object and add the
        # object to the result list.
        # NOTE: Passing `reverse=True` to iter_messages() sorts the messages from old to new.
        async for msg in self.client.iter_messages(chat_id, reverse=True):
            photo: Photo = await self._get_photo(chat_id, msg, compute_md5)
            if photo is not None:
                photos.append(photo)

        return photos

    async def get_videos(self, chat_id: str, compute_md5: bool = False) -> list[Video]:
        """
        TODO
        """
        assert chat_id is not None, "No chat id given."

        if not self.client.is_connected():
            await self.start()

        videos: list[Video] = []

        # Iterate through the messages of the specified chat. If the current message contains a
        # video, store the information about the video in a `models.Video` object and add the
        # object to the result list.
        # NOTE: Passing `reverse=True` to iter_messages() sorts the messages from old to new.
        async for msg in self.client.iter_messages(chat_id, reverse=True):
            video: Video = await self._get_video(chat_id, msg, compute_md5)
            if video is not None:
                videos.append(video)

        return videos


    # async def download_video(self, video: Video, file: str = None):
    #     """
    #     TODO
    #     """
    #     file = file if file is not None else bytes
    #     return await self.client.download_media(video._telethon_media_obj, file=file)

    # async def download_video_thumb(self, video: Video, file: str = None):
    #     """
    #     TODO
    #     """
    #     file = file if file is not None else bytes
    #     return await self.client.download_media(video._telethon_media_obj, file=file, thumb=-1)

    # async def download_photo(self, photo: Photo, file: str = None):
    #     """
    #     TODO
    #     """
    #     file = file if file is not None else bytes
    #     return await self.client.download_media(photo._telethon_media_obj, file=file)

    # ==============================================================================================

    async def _get_from_peer(self, chat_id: str, msg: telethon.types.Message) -> tuple[str, str]:
        """
        TODO
        """
        if msg is None:
            return None, None

        if msg.from_id is None:
            # The message was sent by the channel itself.
            # Determine if the chat is a user, channel or group.
            entity = await self.client.get_entity(chat_id)
            if isinstance(entity, telethon.types.User):
                return "user", chat_id
            if isinstance(entity, telethon.types.Channel):
                if entity.megagroup or entity.gigagroup:
                    return "group", chat_id
                return "channel", chat_id
            if isinstance(entity, telethon.types.Chat):
                return "group", chat_id
            return None, None

        if isinstance(msg.from_id, telethon.types.PeerUser):
            return "user", msg.from_id.user_id

        if isinstance(msg.from_id, telethon.types.PeerChannel):
            return "channel", msg.from_id.channel_id

        if isinstance(msg.from_id, telethon.types.PeerChat):
            return "group", msg.from_id.chat_id

        return None, None


    def _get_reactions(self, msg: telethon.types.Message) -> list[tuple]:
        """
        TODO
        """
        if msg is None:
            return

        if msg.reactions is None:
            return

        if msg.reactions.results is None:
            return

        reactions = []
        for entry in msg.reactions.results:
            emoticon = entry.reaction.emoticon if entry.reaction is not None else None
            count = entry.count
            reactions.append((emoticon, count))

        return reactions

    async def _get_photo(self, chat_id: str, msg: telethon.types.Message, compute_md5: bool = False) -> Photo:
        """
        TODO
        """
        if msg is None:
            return

        # The message does not contain a photo if it has no "media" attribute.
        if not hasattr(msg, "media"):
            return

        # The message does not contain a photo if the media is not of type 'MessageMediaPhoto'.
        if not isinstance(msg.media, telethon.types.MessageMediaPhoto):
            return

        p: telethon.types.Photo = msg.media.photo
        if p is None:
            return

        photo: Photo = Photo()
        photo.id = utils.unique_id()
        photo.chat_id = chat_id
        photo.ref_id = p.id
        photo.message_id = msg.id
        photo.author_peer_type, photo.author_peer_id = await self._get_from_peer(chat_id, msg)
        photo.post_date = msg.date
        photo._telethon_media_obj = msg.media

        # There may be different sizes of the same photo, stored in `p.sizes` and ordered by size
        # in ascending order. Use the photo with the largest size (= the last element in p.sizes).
        if p.sizes:
            largest_photo_size: TypePhotoSize = p.sizes[-1]
            photo.width = largest_photo_size.w
            photo.height = largest_photo_size.h

            if isinstance(largest_photo_size, PhotoSizeProgressive):
                photo.size = largest_photo_size.sizes[-1]
            else:
                photo.size = largest_photo_size.size

            if compute_md5:
                try:
                    photo_bytes = await msg.download_media(file=bytes, thumb=-1)
                    photo.md5 = hashlib.md5(photo_bytes).hexdigest()
                except Exception as e:
                    print("Could not download thumb", e)
                    pass

        return photo


    async def _get_video(self,
                         chat_id: str,
                         msg: telethon.types.Message,
                         compute_md5: bool = False) -> Video:
        """
        TODO
        """
        if msg is None:
            return

        # The message does not contain a video if it has no "media" attribute.
        if not hasattr(msg, "media"):
            return

        # The message does not contain a video if the media is not of type 'MessageMediaDocument'.
        if not isinstance(msg.media, telethon.types.MessageMediaDocument):
            return

        doc: telethon.types.Document = msg.media.document
        if doc is None:
            return

        # The message doesn't contain a video if the document's mime type does not contain "video".
        if "video" not in doc.mime_type:
            return

        video: Video = Video()
        video.id = utils.unique_id()
        video.chat_id = chat_id
        video.ref_id = doc.id
        video.message_id = msg.id
        video.author_peer_type, video.author_peer_id = await self._get_from_peer(chat_id, msg)
        video.post_date = msg.date
        video.mime_type = doc.mime_type
        video.size = doc.size
        video._telethon_media_obj = msg.media

        # Obtain the duration, width and height of the video.
        if doc.attributes is not None:
            for attr in doc.attributes:
                if isinstance(attr, telethon.types.DocumentAttributeVideo):
                    video.duration = attr.duration
                    video.width = attr.w
                    video.height = attr.h
                    break

        # Obtain the MD5 hash of the video's largest thumbnail.
        if compute_md5:
            if doc.thumbs is not None:
                for thumb in reversed(doc.thumbs):
                    if isinstance(thumb, telethon.types.PhotoSize):
                        try:
                            thumb_bytes = await msg.download_media(file=bytes, thumb=thumb)
                            video.thumb_md5 = hashlib.md5(thumb_bytes).hexdigest()
                        except Exception as e:
                            # log.warn("Could not download thumb.")
                            pass
                        break

        return video
