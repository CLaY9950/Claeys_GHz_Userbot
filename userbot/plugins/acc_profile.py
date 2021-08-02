"""ρяσƒιℓє υρ∂αтιση ¢σммαη∂ѕ:
.pbio <Bio>
.pname <Name>
.ppic"""
import os
from telethon import events
from telethon.tl import functions
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="pbio (.*)"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    bio = event.pattern_match.group(1)
    try:
        await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            about=bio
        ))
        await event.edit("𝗦𝗨𝗖𝗖𝗘𝗦𝗦𝗙𝗨𝗟𝗟𝗬 ¢нαηgє∂ υя 𝐁𝐈𝐎 ¢ℓαєу! ¢нє¢к ☑ησω мαѕтєя!\n\n © 🇦​🇸​🇸​​​​​🇮​🇸​🇹​🇦​🇳​🇹 ᵒᶠ ᶜˡᵃᵉʸ"​)
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))


@borg.on(admin_cmd(pattern="pname ((.|\n)*)"))  # pylint:disable=E0602,W0703
async def _(event):
    if event.fwd_from:
        return
    names = event.pattern_match.group(1)
    first_name = names
    last_name = ""
    if  "\\n" in names:
        first_name, last_name = names.split("\\n", 1)
    try:
        await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            first_name=first_name,
            last_name=last_name
        ))
        await event.edit("My Master Name was changed successfully! © @Godhackerzuserbot")
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))


@borg.on(admin_cmd(pattern="ppic"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    await event.edit("∂σωиℓσα∂ιиg ρяσfιℓє ρι¢ тσ му ℓσ¢αℓ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):  # pylint:disable=E0602
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)  # pylint:disable=E0602
    photo = None
    try:
        photo = await borg.download_media(  # pylint:disable=E0602
            reply_message,
            Config.TMP_DOWNLOAD_DIRECTORY  # pylint:disable=E0602
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))
    else:
        if photo:
            await event.edit("now, Uploading to @Telegram ...")
            file = await borg.upload_file(photo)  # pylint:disable=E0602
            try:
                await borg(functions.photos.UploadProfilePhotoRequest(  # pylint:disable=E0602
                    file
                ))
            except Exception as e:  # pylint:disable=C0103,W0703
                await event.edit(str(e))
            else:
                await event.edit("υя ρяσfιℓє ρι¢ ωαѕ ѕυ¢¢єѕѕfυℓℓу ¢нαиgє∂ !\n\n © 🇦​🇸​🇸​🇮​🇸​🇹​🇦​🇳​🇹 ᵒᶠ ᶜˡᵃᵉʸ​​​")
    try:
        os.remove(photo)
    except Exception as e:  # pylint:disable=C0103,W0703
        logger.warn(str(e))  # pylint:disable=E0602
