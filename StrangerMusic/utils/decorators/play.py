from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup,Message
from pyrogram.enums import ChatMemberStatus

from StrangerMusic.utils.database.mongodatabase import add_private_chat
from StrangerMusic.utils.inline.start import pvt_bot
from config import PLAYLIST_IMG_URL, PRIVATE_BOT_MODE, adminlist,PRIVATE_BOT_MODE_MEM, OWNER_ID
from strings import get_string
from StrangerMusic import YouTube, app
from StrangerMusic.misc import SUDOERS
from StrangerMusic.utils.database import (get_cmode, get_lang,
                                       get_playmode, get_playtype,
                                       is_active_chat,
                                       is_commanddelete_on,
                                       is_served_private_chat)
from StrangerMusic.utils.database.memorydatabase import is_maintenance
from StrangerMusic.utils.inline.playlist import botplaylist_markup


def PlayWrapper(command):
    async def wrapper(client, message:Message):
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    "Bot is under maintenance. Please wait for some time... \n Untill use our other bots and enjoy music \n @fallen_MusicBot \n@Sykkunobot"
                )
        mem_count = await app.get_chat_members_count(message.chat.id)
        if PRIVATE_BOT_MODE == str(True):
            if mem_count > PRIVATE_BOT_MODE_MEM:
                await add_private_chat(message.chat.id)
            elif not await is_served_private_chat(message.chat.id):
                try:
                    await app.resolve_peer(OWNER_ID[0])
                    OWNER = OWNER_ID[0]
                except :
                    OWNER = None
                btn = pvt_bot(OWNER)
                await message.reply_text(
                    "**Private Music Bot**\n\nOnly for authorized chats from the owner. Ask my owner to allow your chat first.",
                    reply_markup=InlineKeyboardMarkup(btn)
                )
                return await app.leave_chat(message.chat.id)
            
        if await is_commanddelete_on(message.chat.id):
            try:
                await message.delete()
            except:
                pass
        language = await get_lang(message.chat.id)
        _ = get_string(language)
        audio_telegram = (
            (
                message.reply_to_message.audio
                or message.reply_to_message.voice
            )
            if message.reply_to_message
            else None
        )
        video_telegram = (
            (
                message.reply_to_message.video
                or message.reply_to_message.document
            )
            if message.reply_to_message
            else None
        )
        url = await YouTube.url(message)
        if (
            audio_telegram is None
            and video_telegram is None
            and url is None
        ):
            if len(message.command) < 2:
                if "stream" in message.command:
                    return await message.reply_text(_["str_1"])
                buttons = botplaylist_markup(_)
                return await message.reply_photo(
                    photo=PLAYLIST_IMG_URL,
                    caption=_["playlist_1"],
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="How to Fix this? ",
                            callback_data="AnonymousAdmin",
                        ),
                    ]
                ]
            )
            return await message.reply_text(
                _["general_4"], reply_markup=upl
            )
        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None:
                return await message.reply_text(_["setting_12"])
            try:
                chat = await app.get_chat(chat_id)
            except:
                return await message.reply_text(_["cplay_4"])
            channel = chat.title
        else:
            chat_id = message.chat.id
            channel = None
        playmode = await get_playmode(message.chat.id)
        playty = await get_playtype(message.chat.id)
        if playty != "Everyone":
            if message.from_user.id not in SUDOERS:
                admins = adminlist.get(message.chat.id)
                if not admins:
                    return await message.reply_text(_["admin_18"])
                else:
                    if message.from_user.id not in admins:
                        return await message.reply_text(_["play_4"])
        if message.command[0][0] == "v":
            video = True
        else:
            if "-v" in message.text:
                video = True
            else:
                video = True if message.command[0][1] == "v" else None
        if message.command[0][-1] == "e":
            if not await is_active_chat(chat_id):
                return await message.reply_text(_["play_18"])
            fplay = True
        else:
            fplay = None
        return await command(
            client,
            message,
            _,
            chat_id,
            video,
            channel,
            playmode,
            url,
            fplay,
        )

    return wrapper
