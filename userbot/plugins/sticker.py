"""Make / Download Telegram Sticker Packs without installing Third Party applications
Available Commands:
.keng [Optional Emoji]
.packinfo
.getstcr"""
import asyncio
import datetime
import math
import os
import zipfile
from collections import defaultdict
from io import BytesIO

from PIL import Image
from telethon.errors import MessageNotModifiedError
from telethon.errors.rpcerrorlist import StickersetInvalidError
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import (
    DocumentAttributeSticker,
    InputStickerSetID,
    InputStickerSetShortName,
    MessageMediaPhoto,
)

from userbot import ALIVE_NAME
from userbot.utils import admin_cmd

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "GODHACKERZ USER"
FILLED_UP_DADDY = "Invalid pack selected."


@borg.on(admin_cmd(pattern="keng ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if not event.is_reply:
        await moods.edit("Reply to a photo to add to your personal sticker pack MASTER.")
        return
    reply_message = await event.get_reply_message()
    sticker_emoji = "🔥"
    input_str = event.pattern_match.group(1)
    if input_str:
        sticker_emoji = input_str
    moods = await reply(event, "`HeHe , Me Gonna Steal`")
    user = await bot.get_me()
    if not user.username:
        user.username = user.id
    pack = 1
    userid = event.from_id
    # packname = f"GODHACKERZ PACK"
    # packshortname = f"GODHACKERZ_{userid}_ns"  # format: Uni_Borg_userid
    if userid == 1207066133:
        packname = f"@GODHACKERZ Packs 🎭"
        packshortname = "GodhackerzPack"
    else:
        packname = f"{user.username}'s {pack}"
        packshortname = f"GODHACKERZ_{userid}_Pack"
    await moods.edit("`Wew ! I Love That Sticker MASTER ! Mind If i Kang It ?`")

    is_a_s = is_it_animated_sticker(reply_message)
    file_ext_ns_ion = "@Godhackerzuserbot.png"
    file = await borg.download_file(reply_message.media)
    uploaded_sticker = None
    if is_a_s:
        file_ext_ns_ion = "AnimatedSticker.tgs"
        uploaded_sticker = await borg.upload_file(file, file_name=file_ext_ns_ion)
        if userid == 1207066133:
            packname = f"MASTER Ka Pack"
            packshortname = "Godhackerzuserbotisgreat"
        else:
            packname = f"{user.username}'s {pack}"
            packshortname = f"Godhackerzuserbot_{userid}"  # format: Uni_Borg_userid
    elif not is_message_image(reply_message):
        await moods.edit("Invalid message type")
        return
    else:
        with BytesIO(file) as mem_file, BytesIO() as sticker:
            resize_image(mem_file, sticker)
            sticker.seek(0)
            uploaded_sticker = await borg.upload_file(
                sticker, file_name=file_ext_ns_ion
            )

    await moods.edit("ADDING To Your Pack MASTER ! Please Wait! MASTER")

    async with borg.conversation("@Stickers") as bot_conv:
        now = datetime.datetime.now()
        dt = now + datetime.timedelta(minutes=1)
        if not await stickerset_exists(bot_conv, packshortname):
            await moods.edit("`Creating a new pack!`")
            await silently_send_message(bot_conv, "/cancel")
            if is_a_s:
                response = await silently_send_message(bot_conv, "/newanimated")
            else:
                response = await silently_send_message(bot_conv, "/newpack")
            if "Yay!" not in response.text:
                await moods.edit(f"**Error**! @Stickers replied: {response.text}")
                return
            response = await silently_send_message(bot_conv, packname)
            if not response.text.startswith("Alright!"):
                await moods.edit(f"**Error**! @Stickers replied: {response.text}")
                return
            w = await bot_conv.send_file(
                file=uploaded_sticker, allow_cache=False, force_document=True
            )
            response = await bot_conv.get_response()
            if "Sorry" in response.text:
                await moods.edit(f"**Error**! @Stickers replied: {response.text}")
                return
            await silently_send_message(bot_conv, sticker_emoji)
            await silently_send_message(bot_conv, "/publish")
            response = await silently_send_message(bot_conv, f"<{packname}>")
            await silently_send_message(bot_conv, "/skip")
            response = await silently_send_message(bot_conv, packshortname)
            if response.text == "Sorry, this short name is already taken.":
                await moods.edit(f"**Error**! @Stickers replied: {response.text}")
                return
        else:
            await silently_send_message(bot_conv, "/cancel")
            await silently_send_message(bot_conv, "/addsticker")
            await silently_send_message(bot_conv, packshortname)
            await bot_conv.send_file(
                file=uploaded_sticker, allow_cache=False, force_document=True
            )
            response = await bot_conv.get_response()
            if response.text == FILLED_UP_DADDY:
                while response.text == FILLED_UP_DADDY:
                    pack += 1
                    prevv = int(pack) - 1
                    packname = f"{user.username}'s {pack}"
                    packshortname = f"Vol_{pack}_with_{user.username}"
                    # if userid == 1207066133:
                    # packname = f"{user.username}'s {pack}"
                    # packshortname = "Vol._{pack}_FRIDAY_ke_locker_me"
                    # else:
                    # packname = f"Vol._{pack}_FRIDAY{userid}"
                    # packshortname = f"Vol._{pack}_Friday_{userid}_ns"
                    if not await stickerset_exists(bot_conv, packshortname):
                        await moods.edit(
                            "**Pack No. **"
                            + str(prevv)
                            + "** full! Making a new Pack, Vol. **"
                            + str(pack)
                        )
                        if is_a_s:
                            response = await silently_send_message(
                                bot_conv, "/newanimated"
                            )
                        else:
                            response = await silently_send_message(bot_conv, "/newpack")
                        if "Yay!" not in response.text:
                            await moods.edit(
                                f"**Error**! @Stickers replied: {response.text}"
                            )
                            return
                        response = await silently_send_message(bot_conv, packname)
                        if not response.text.startswith("Alright!"):
                            await moods.edit(
                                f"**Error**! @Stickers replied: {response.text}"
                            )
                            return
                        w = await bot_conv.send_file(
                            file=uploaded_sticker,
                            allow_cache=False,
                            force_document=True,
                        )
                        response = await bot_conv.get_response()
                        if "Sorry" in response.text:
                            await moods.edit(
                                f"**Error**! @Stickers replied: {response.text}"
                            )
                            return
                        await silently_send_message(bot_conv, sticker_emoji)
                        await silently_send_message(bot_conv, "/publish")
                        response = await silently_send_message(
                            bot_conv, f"<{packname}>"
                        )
                        await silently_send_message(bot_conv, "/skip")
                        response = await silently_send_message(bot_conv, packshortname)
                        if response.text == "Sorry, this short name is already taken.":
                            await moods.edit(
                                f"**Error**! @Stickers replied: {response.text}"
                            )
                            return
                    else:
                        await moods.edit(
                            "Pack No. "
                            + str(prevv)
                            + " full! Switching to Vol. "
                            + str(pack)
                        )
                        await silently_send_message(bot_conv, "/addsticker")
                        await silently_send_message(bot_conv, packshortname)
                        await bot_conv.send_file(
                            file=uploaded_sticker,
                            allow_cache=False,
                            force_document=True,
                        )
                        response = await bot_conv.get_response()
                        if "Sorry" in response.text:
                            await moods.edit(
                                f"**Error**! @Stickers replied: {response.text}"
                            )
                            return
                        await silently_send_message(bot_conv, sticker_emoji)
                        await silently_send_message(bot_conv, "/done")
            else:
                if "Sorry" in response.text:
                    await moods.edit(f"**Error**! @Stickers replied: {response.text}")
                    return
                await silently_send_message(bot_conv, response)
                await silently_send_message(bot_conv, sticker_emoji)
                await silently_send_message(bot_conv, "/done")
    await moods.edit(
        f"**Sticker Has Been Kanged SucessFully And Can Be Found** [Here](t.me/addstickers/{packshortname})Master"
    )


@borg.on(admin_cmd(pattern="packinfo"))
async def _(event):
    moods = await reply("`HeHe , Master Me Gonna Leech Pack Info`")
    if event.fwd_from:
        return
    if not event.is_reply:
        await moods.edit("Reply to any sticker to get it's pack info Master .")
        return
    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        await moods.edit("Reply to any sticker to get it's pack info.")
        return
    stickerset_attr_s = rep_msg.document.attributes
    stickerset_attr = find_instance(stickerset_attr_s, DocumentAttributeSticker)
    if not stickerset_attr.stickerset:
        await moods.edit("sticker does not belong to a pack.")
        return
    get_stickerset = await borg(
        GetStickerSetRequest(
            InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash,
            )
        )
    )
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)
    await moods.edit(
        f"**Sticker Title:** `{get_stickerset.set.title}\n`"
        f"**Sticker Short Name:** `{get_stickerset.set.short_name}`\n"
        f"**Official:** `{get_stickerset.set.official}`\n"
        f"**Archived:** `{get_stickerset.set.archived}`\n"
        f"**Stickers In Pack:** `{len(get_stickerset.packs)}`\n"
        f"**Emojis In Pack:** {' '.join(pack_emojis)}"
    )


@borg.on(admin_cmd(pattern="getsticker ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        # https://gist.github.com/udf/e4e3dbb2e831c8b580d8fddd312714f7
        if not reply_message.sticker:
            return
        sticker = reply_message.sticker
        sticker_attrib = find_instance(sticker.attributes, DocumentAttributeSticker)
        if not sticker_attrib.stickerset:
            await event.reply("This sticker is not part of a pack")
            return
        is_a_s = is_it_animated_sticker(reply_message)
        file_ext_ns_ion = "webp"
        file_caption = "https://t.me/RoseSupport/33801"
        if is_a_s:
            file_ext_ns_ion = "tgs"
            file_caption = "Forward the ZIP file to @AnimatedStickersRoBot to get lottIE JSON containing the vector information."
        sticker_set = await borg(GetStickerSetRequest(sticker_attrib.stickerset))
        pack_file = os.path.join(
            Config.TMP_DOWNLOAD_DIRECTORY, sticker_set.set.short_name, "pack.txt"
        )
        if os.path.isfile(pack_file):
            os.remove(pack_file)
        # Sticker emojis are retrieved as a mapping of
        # <emoji>: <list of document ids that have this emoji>
        # So we need to build a mapping of <document id>: <list of emoji>
        # Thanks, Durov
        emojis = defaultdict(str)
        for pack in sticker_set.packs:
            for document_id in pack.documents:
                emojis[document_id] += pack.emoticon

        async def download(sticker, emojis, path, file):
            await borg.download_media(sticker, file=os.path.join(path, file))
            with open(pack_file, "a") as f:
                f.write(f"{{'image_file': '{file}','emojis':{emojis[sticker.id]}}},")

        pending_tasks = [
            asyncio.ensure_future(
                download(
                    document,
                    emojis,
                    Config.TMP_DOWNLOAD_DIRECTORY + sticker_set.set.short_name,
                    f"{i:03d}.{file_ext_ns_ion}",
                )
            )
            for i, document in enumerate(sticker_set.documents)
        ]
        await moods.edit(
            f"Downloading {sticker_set.set.count} sticker(s) to .{Config.TMP_DOWNLOAD_DIRECTORY}{sticker_set.set.short_name}..."
        )
        num_tasks = len(pending_tasks)
        while 1:
            done, pending_tasks = await asyncio.wait(
                pending_tasks, timeout=2.5, return_when=asyncio.FIRST_COMPLETED
            )
            try:
                await moods.edit(
                    f"Downloaded {num_tasks - len(pending_tasks)}/{sticker_set.set.count}"
                )
            except MessageNotModifiedError:
                pass
            if not pending_tasks:
                break
        await moods.edit("Downloading to my local completed")
        # https://gist.github.com/udf/e4e3dbb2e831c8b580d8fddd312714f7
        directory_name = Config.TMP_DOWNLOAD_DIRECTORY + sticker_set.set.short_name
        zipf = zipfile.ZipFile(directory_name + ".zip", "w", zipfile.ZIP_DEFLATED)
        zipdir(directory_name, zipf)
        zipf.close()
        await borg.send_file(
            event.chat_id,
            directory_name + ".zip",
            caption=file_caption,
            force_document=True,
            allow_cache=False,
            reply_to=event.message.id,
            progress_callback=progress,
        )
        try:
            os.remove(directory_name + ".zip")
            os.remove(directory_name)
        except:
            pass
        await moods.edit("task Completed")
        await asyncio.sleep(3)
        await event.delete()
    else:
        await moods.edit("TODO: Not Implemented")


# Helpers


def is_it_animated_sticker(message):
    try:
        if message.media and message.media.document:
            mime_type = message.media.document.mime_type
            if "tgsticker" in mime_type:
                return True
            else:
                return False
        else:
            return False
    except:
        return False


def is_message_image(message):
    if message.media:
        if isinstance(message.media, MessageMediaPhoto):
            return True
        if message.media.document:
            if message.media.document.mime_type.split("/")[0] == "image":
                return True
        return False
    return False


async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response


async def stickerset_exists(conv, setname):
    try:
        await borg(GetStickerSetRequest(InputStickerSetShortName(setname)))
        response = await silently_send_message(conv, "/addsticker")
        if response.text == "Invalid pack selected.":
            await silently_send_message(conv, "/cancel")
            return False
        await silently_send_message(conv, "/cancel")
        return True
    except StickersetInvalidError:
        return False


def resize_image(image, save_locaton):
    """Copyright Rhyse Simpson:
    https://github.com/skittles9823/SkittBot/blob/master/tg_bot/modules/stickers.py
    """
    im = Image.open(image)
    maxsize = (512, 512)
    if (im.width and im.height) < 512:
        size1 = im.width
        size2 = im.height
        if im.width > im.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        im = im.resize(sizenew)
    else:
        im.thumbnail(maxsize)
    im.save(save_locaton, "PNG")


def progress(current, total):
    logger.info(
        "Uploaded: {} of {}\nCompleted {}".format(
            current, total, (current / total) * 100
        )
    )


def find_instance(items, class_or_tuple):
    for item in items:
        if isinstance(item, class_or_tuple):
            return item
    return None


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
            os.remove(os.path.join(root, file))
