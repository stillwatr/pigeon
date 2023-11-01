from __future__ import annotations

import math
import telethon

import pigeon.models as models
import pigeon.utils as utils

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
        self.chats: list[models.Chat] = []

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

    async def get_chats(self) -> list[models.Chat]:
        """
        TODO
        """
        chats: list[models.Chat] = []

        for dialog in await self.client.get_dialogs():
            if dialog.is_user:
                chats.append(self.entity_to_user(dialog.entity))
            elif dialog.is_group:
                chats.append(self.entity_to_group(dialog.entity))
            elif dialog.is_channel:
                chats.append(self.entity_to_channel(dialog.entity))

        return chats

    async def get_messages(
            self,
            chat_id: int,
            compute_media_hashes: bool = False) -> list[models.Message]:
        """
        TODO
        """
        assert chat_id is not None, "No chat id given."

        # Start the client if necessary.
        if not self.client.is_connected():
            await self.start()

        # Scrape the messages of the specified chat.
        # NOTE: Passing `reverse=True` to iter_messages() sorts the messages from old to new.
        messages: list[models.Message] = []
        async for msg in self.client.iter_messages(chat_id, reverse=True):
            # Ignore all non-messages.
            if not isinstance(msg, telethon.types.Message):
                continue

            message = models.Message()
            message.id = msg.id
            message.chat_id = chat_id
            message.from_chat = await self.get_from_chat(msg)
            message.post_date = msg.date
            message.edit_date = msg.edit_date
            message.text = msg.message
            # message.photo = await self.get_photo(msg, compute_media_hashes)
            # message.photo_id = message.photo.id if message.photo is not None else None
            # message.video = await self.get_video(msg, compute_media_hashes)
            # message.video_id = message.video.id if message.video is not None else None
            message.reactions = self.get_reactions(msg)
            message.num_views = msg.views if msg.views is not None else 0
            message.num_forwards = msg.forwards if msg.forwards is not None else 0
            message.num_replies = msg.replies.replies if msg.replies is not None else 0
            message.group_id = msg.grouped_id
            message.reply_to_msg_id = msg.reply_to.reply_to_msg_id if msg.reply_to else None
            message.forward_from_chat = await self.get_forward_from_chat(msg)

            messages.append(message)

        return messages

    # ==============================================================================================

    async def get_photos(
            self,
            chat_id: int,
            compute_hashes: bool = False) -> list[models.Photo]:
        """
        TODO
        """
        assert chat_id is not None, "No chat id given."

        # Start the client if necessary.
        if not self.client.is_connected():
            await self.start()

        # Scrape the photos posted in the specified chat.
        # NOTE: Passing `reverse=True` to iter_messages() sorts the messages from old to new.
        photos: list[models.Photo] = []
        async for msg in self.client.iter_messages(chat_id, reverse=True):
            photo: models.Photo = await self.get_photo(msg, compute_hashes)
            if photo is not None:
                photos.append(photo)

        return photos

    async def get_photo(
            self,
            msg: telethon.types.Message,
            compute_hash: bool = False) -> models.Photo:
        """
        TODO
        """
        assert msg is not None, "No message given."

        # The message does not contain a photo if it has no "media" attribute.
        if not hasattr(msg, "media"):
            return None

        # The message does not contain a photo if the media is not of type 'MessageMediaPhoto'.
        if not isinstance(msg.media, telethon.types.MessageMediaPhoto):
            return None

        p: telethon.types.Photo = msg.media.photo
        if p is None:
            return None

        photo = models.Photo(id=p.id)

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
                    photo.hash = utils.compute_image_hash(photo_bytes)
                except Exception as e:
                    print("Could not download thumbnail.", e)

        return photo

    # ==============================================================================================

    async def get_videos(
            self,
            chat_id: int,
            compute_thumb_hashes: bool = False) -> list[models.Video]:
        """
        TODO
        """
        assert chat_id is not None, "No chat id given."

        # Start the client if necessary.
        if not self.client.is_connected():
            await self.start()

        # Scrape the videos posted in the specified chat.
        # NOTE: Passing `reverse=True` to iter_messages() sorts the messages from old to new.
        videos: list[models.Video] = []
        async for msg in self.client.iter_messages(chat_id, reverse=True):
            video: models.Video = await self.get_video(msg, compute_thumb_hashes)
            if video is not None:
                videos.append(video)

        return videos

    async def get_video(
            self,
            msg: telethon.types.Message,
            compute_thumb_hash: bool = False) -> models.Video:
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

        video: models.Video = models.Video()
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
                            video.thumb_hash = utils.compute_image_hash(thumbnail_bytes)
                        except Exception as e:
                            print("Could not download thumbnail.", e)
                        break

        return video

    # ==============================================================================================

    def get_reactions(self, msg: telethon.types.Message) -> list[tuple]:
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

    # ==============================================================================================

    async def get_from_chat(self, msg: telethon.types.Message) -> models.Chat:
        """
        TODO
        """
        assert msg is not None, "No message given."

        from_id = msg.from_id
        if from_id is None:
            if isinstance(msg.peer_id, telethon.types.PeerChannel):
                from_id = msg.peer_id.channel_id
            elif isinstance(msg.peer_id, telethon.types.PeerChat):
                from_id = msg.peer_id.chat_id
            elif isinstance(msg.peer_id, telethon.types.PeerUser):
                from_id = msg.peer_id.user_id

        return models.Chat(id=from_id)

        # TODO: The following results in FloodwaitErrors.
        # try:
        #     entity = await self.client.get_entity(from_id)
        # except telethon.errors.rpcerrorlist.ChannelPrivateError:
        #     # The chat is private.
        #     return models.Chat(id=msg.from_id)

        # if isinstance(entity, telethon.types.User):
        #     return self.entity_to_user(entity)

        # if isinstance(entity, telethon.types.Chat) \
        #     or getattr(entity, "megagroup", False) \
        #         or getattr(entity, "gigagroup", False):
        #     return self.entity_to_group(entity)

        # if isinstance(entity, telethon.types.Channel):
        #     return self.entity_to_channel(entity)

        # return None

    # TODO: Merge with get_from_chat()
    async def get_forward_from_chat(self, msg: telethon.types.Message) -> models.Chat:
        """
        TODO
        """
        assert msg is not None, "No message given."

        if msg.fwd_from is None:
            return None

        # A forwarded chat can hide its identity, in which case from_id is None.
        from_id = msg.fwd_from.from_id
        if from_id is None:
            return models.Chat(name=msg.fwd_from.from_name)

        return models.Chat(id=from_id)

        # TODO: The following results in FloodWaitErrors.
        # Obtain the "from" entity (= user, channel or group).
        # try:
        #     entity = await self.client.get_entity(from_id)
        # except telethon.errors.rpcerrorlist.ChannelPrivateError:
        #     # The chat is private.
        #     return models.Chat(id=msg.fwd_from.from_id, name=msg.fwd_from.from_name)

        # if isinstance(entity, telethon.types.User):
        #     return self.entity_to_user(entity)

        # if isinstance(entity, telethon.types.Chat) \
        #     or getattr(entity, "megagroup", False) \
        #         or getattr(entity, "gigagroup", False):
        #     return self.entity_to_group(entity)

        # if isinstance(entity, telethon.types.Channel):
        #     return self.entity_to_channel(entity)

        # return None

    # ==============================================================================================

    # TODO: Can be static
    def entity_to_user(self, entity: telethon.types.User) -> models.User:
        """
        TODO
        """
        return models.User(
            id=entity.id,
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

    # TODO: Can be static
    def entity_to_group(self, entity: telethon.types.Chat) -> models.Group:
        """
        TODO
        """
        return models.Group(
            id=entity.id,
            name=entity.title,
            creation_date=entity.date,
            deactivated=getattr(entity, "deactivated", False),
        )

    # TODO: Can be static
    def entity_to_channel(self, entity: telethon.types.Channel) -> models.Channel:
        """
        TODO
        """
        return models.Channel(
            id=entity.id,
            name=entity.title,
            creation_date=entity.date,
            verified=entity.verified,
            restricted=entity.restricted,
            restricted_reason=entity.restriction_reason
        )
