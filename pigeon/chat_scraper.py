from __future__ import annotations

import math
import telethon
import typing

import pigeon.models
import pigeon.utils

# ==================================================================================================


class TelegramChatScraper:
    """
    TODO
    """

    def __init__(self, telethon_api_id: int, telethon_api_hash: str, telethon_session: str) -> None:
        """
        TODO
        """
        self.client: telethon.TelegramClient = telethon.TelegramClient(
            api_id=telethon_api_id,
            api_hash=telethon_api_hash,
            session=telethon_session
        )
        self.chats: list[pigeon.models.Chat] = []

    async def start(self) -> TelegramChatScraper:
        """
        TODO
        """
        # Try to start the client.
        try:
            await self.client.start()
        except Exception as e:
            raise RuntimeError("Could not start the Telethon client.", e)

        # Get the chats the user is a member of. This is necessary to later access groups
        # and chats by id, see https://docs.telethon.dev/en/stable/concepts/entities.html.
        try:
            self.chats = await self.get_chats()
        except Exception as e:
            raise RuntimeError("Could not get chats.", e)

        return self

    async def get_chats(self) -> list[pigeon.models.Chat]:
        """
        TODO
        """
        chats: list[pigeon.models.Chat] = []

        for dialog in await self.client.get_dialogs():
            if dialog.is_user:
                chats.append(TelegramChatScraper.entity_to_user(dialog.entity))
            elif dialog.is_group:
                chats.append(TelegramChatScraper.entity_to_group(dialog.entity))
            elif dialog.is_channel:
                chats.append(TelegramChatScraper.entity_to_channel(dialog.entity))

        return chats

    async def get_users(self, chat_id: str) -> list[pigeon.models.User]:
        """
        TODO
        """
        assert chat_id is not None, "no chat id given"

        # Start the client if necessary.
        if not self.client.is_connected():
            await self.start()

        # Scrape the users of the specified chat.
        users: list[pigeon.models.User] = []
        async for participant in self.client.iter_participants(chat_id):
            if not isinstance(participant, telethon.types.User):
                continue
            users.append(TelegramChatScraper.entity_to_user(participant))

        return users

    async def get_messages(
            self,
            chat_id: int,
            compute_media_hashes: bool = False) -> list[pigeon.models.Message]:
        """
        TODO
        """
        assert chat_id is not None, "no chat id given"

        # Start the client if necessary.
        if not self.client.is_connected():
            await self.start()

        # Scrape the messages of the specified chat.
        # NOTE: Passing `reverse=True` to iter_messages() sorts the messages from old to new.
        messages: list[pigeon.models.Message] = []
        async for msg in self.client.iter_messages(chat_id, reverse=True):
            if not isinstance(msg, telethon.types.Message):
                continue

            message = pigeon.models.Message()
            message.id = msg.id
            message.chat_id = chat_id
            message.from_chat_id, message.from_chat_type = self.get_from_chat(msg)
            message.post_date = msg.date
            message.edit_date = msg.edit_date
            message.text = msg.message
            message.photo = await self.get_photo(msg, compute_media_hashes)
            message.photo_id = message.photo.id if message.photo is not None else None
            message.video = await self.get_video(msg, compute_media_hashes)
            message.video_id = message.video.id if message.video is not None else None
            message.reactions = self.get_reactions(msg)
            message.num_views = msg.views if msg.views is not None else 0
            message.num_forwards = msg.forwards if msg.forwards is not None else 0
            message.num_replies = msg.replies.replies if msg.replies is not None else 0
            message.group_id = msg.grouped_id if msg.grouped_id is not None else None
            message.reply_to_msg_id = msg.reply_to.reply_to_msg_id if msg.reply_to else None
            message.fwd_from_chat_id, message.fwd_from_chat_type = self.get_fwd_from_chat(msg)

            messages.append(message)

        return messages

    # ==============================================================================================

    async def get_photos(
            self,
            chat_id: int,
            compute_hashes: bool = False) -> list[pigeon.models.Photo]:
        """
        TODO
        """
        assert chat_id is not None, "no chat id given"

        # Start the client if necessary.
        if not self.client.is_connected():
            await self.start()

        # Scrape the photos posted in the specified chat.
        # NOTE: Passing `reverse=True` to iter_messages() sorts the messages from old to new.
        photos: list[pigeon.models.Photo] = []
        async for msg in self.client.iter_messages(chat_id, reverse=True):
            if not isinstance(msg, telethon.types.Message):
                continue

            photo = await self.get_photo(msg, compute_hashes)
            if photo is not None:
                photos.append(photo)

        return photos

    async def get_photo(
            self,
            msg: telethon.types.Message,
            compute_hash: bool = False) -> pigeon.models.Photo | None:
        """
        TODO
        """
        assert msg is not None, "no message given"

        # The message does not contain a photo if it has no "media" attribute.
        if not hasattr(msg, "media"):
            return None

        # The message does not contain a photo if the media is not of type 'MessageMediaPhoto'.
        if not isinstance(msg.media, telethon.types.MessageMediaPhoto):
            return None

        p: telethon.types.Photo = msg.media.photo
        if p is None:
            return None

        photo = pigeon.models.Photo(id=p.id)

        # There may be different sizes of the same photo, stored in `p.sizes` and ordered by size
        # in ascending order. Use the photo with the largest size (= the last element in p.sizes).
        if p.sizes:
            largest_photo_size: telethon.types.TypePhotoSize = p.sizes[-1]
            photo.width = largest_photo_size.w
            photo.height = largest_photo_size.h

            if isinstance(largest_photo_size, telethon.types.PhotoSizeProgressive):
                photo.size = largest_photo_size.sizes[-1]
            else:
                photo.size = largest_photo_size.size

            if compute_hash:
                try:
                    photo_bytes = await msg.download_media(file=bytes, thumb=-1)
                    photo.hash = pigeon.utils.compute_image_hash(photo_bytes)
                except Exception as e:
                    print("Could not download thumbnail.", e)

        return photo

    # ==============================================================================================

    async def get_videos(
            self,
            chat_id: int,
            compute_thumb_hashes: bool = False) -> list[pigeon.models.Video]:
        """
        TODO
        """
        assert chat_id is not None, "no chat id given"

        # Start the client if necessary.
        if not self.client.is_connected():
            await self.start()

        # Scrape the videos posted in the specified chat.
        # NOTE: Passing `reverse=True` to iter_messages() sorts the messages from old to new.
        videos: list[pigeon.models.Video] = []
        async for msg in self.client.iter_messages(chat_id, reverse=True):
            if not isinstance(msg, telethon.types.Message):
                continue

            video = await self.get_video(msg, compute_thumb_hashes)
            if video is not None:
                videos.append(video)

        return videos

    async def get_video(
            self,
            msg: telethon.types.Message,
            compute_thumb_hash: bool = False) -> pigeon.models.Video | None:
        """
        TODO
        """
        assert msg is not None, "No message given."

        # The message does not contain a video if it has no "media" attribute.
        if not hasattr(msg, "media"):
            return None

        # The message does not contain a video if the media is not of type 'MessageMediaDocument'.
        if not isinstance(msg.media, telethon.types.MessageMediaDocument):
            return None

        doc: telethon.types.Document = msg.media.document
        if doc is None:
            return None

        # The message doesn't contain a video if the document's mime type does not contain "video".
        if "video" not in doc.mime_type:
            return None

        video = pigeon.models.Video()
        video.id = doc.id
        video.mime_type = doc.mime_type
        video.size = doc.size

        # Obtain the duration, width and height of the video.
        if doc.attributes is not None:
            for attr in doc.attributes:
                if isinstance(attr, telethon.types.DocumentAttributeVideo):
                    video.duration = math.ceil(attr.duration)
                    video.width = attr.w
                    video.height = attr.h

        # Compute the hash of the video's largest thumbnail.
        if compute_thumb_hash:
            if doc.thumbs is not None:
                for thumb in reversed(doc.thumbs):
                    if isinstance(thumb, telethon.types.PhotoSize):
                        try:
                            thumbnail_bytes = await msg.download_media(file=bytes, thumb=thumb)
                            video.thumb_hash = pigeon.utils.compute_image_hash(thumbnail_bytes)
                        except Exception as e:
                            print("Could not download thumbnail.", e)
                        break

        return video

    # ==============================================================================================

    def get_reactions(self, msg: telethon.types.Message) -> list[tuple] | None:
        """
        TODO
        """
        assert msg is not None, "No message given."

        if msg.reactions is None:
            return None

        if msg.reactions.results is None:
            return None

        reactions: list[tuple] = []
        for entry in msg.reactions.results:
            emoticon = entry.reaction.emoticon if entry.reaction is not None else None
            count = entry.count
            reactions.append((emoticon, count))

        return reactions

    def get_from_chat(self, msg: telethon.types.Message) -> typing.Tuple[int | None, str | None]:
        """
        TODO
        """
        assert msg is not None, "no message given"

        from_id = msg.from_id or msg.peer_id

        if isinstance(from_id, telethon.types.PeerChannel):
            return from_id.channel_id, "channel"

        if isinstance(from_id, telethon.types.PeerChat):
            return from_id.chat_id, "group"

        if isinstance(from_id, telethon.types.PeerUser):
            return from_id.user_id, "user"

        return None, None

    def get_fwd_from_chat(self, m: telethon.types.Message) -> typing.Tuple[str | None, str | None]:
        """
        TODO
        """
        assert m is not None, "no message given"

        if m.fwd_from is None:
            return None, None

        from_id = m.fwd_from.from_id

        # A forwarded chat can hide its identity, in which case from_id is None.
        if from_id is None:
            return m.fwd_from.from_name, None

        if isinstance(from_id, telethon.types.PeerChannel):
            return str(from_id.channel_id), "channel"

        if isinstance(from_id, telethon.types.PeerChat):
            return str(from_id.chat_id), "group"

        if isinstance(from_id, telethon.types.PeerUser):
            return str(from_id.user_id), "user"

        return None, None

    # ==============================================================================================

    def entity_to_user(entity: telethon.types.User) -> pigeon.models.User:
        """
        TODO
        """
        return pigeon.models.User(
            entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            user_name=entity.username,
            phone=entity.phone,
            lang_code=entity.lang_code,
            verified=entity.verified,
            deleted=entity.deleted,
            is_bot=entity.bot,
            restricted=entity.restricted,
            restricted_reason=entity.restriction_reason
        )

    def entity_to_group(entity: telethon.types.Chat) -> pigeon.models.Group:
        """
        TODO
        """
        return pigeon.models.Group(
            id=entity.id,
            name=entity.title,
            creation_date=entity.date,
            deactivated=getattr(entity, "deactivated", False),
        )

    def entity_to_channel(entity: telethon.types.Channel) -> pigeon.models.Channel:
        """
        TODO
        """
        return pigeon.models.Channel(
            id=entity.id,
            name=entity.title,
            creation_date=entity.date,
            verified=entity.verified,
            restricted=entity.restricted,
            restricted_reason=entity.restriction_reason
        )
