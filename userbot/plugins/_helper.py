  
from telethon import functions

from userbot import ALIVE_NAME, CMD_LIST
from userbot.utils import admin_cmd

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "Ιтz мє ¢ℓαєу"


@command(pattern="^.help ?(.*)")
async def cmd_list(event):
    if not event.text[0].isalpha() and event.text[0] not in (
        "/",
        "#",
        "@",
        "!",
        "-",
        "_",
    ):
        tgbotusername = Var.TG_BOT_USER_NAME_BF_HER
        input_str = event.pattern_match.group(1)
        if tgbotusername is None or input_str == "text":
            string = ""
            for i in CMD_LIST:
                string += "⚡️" + i + "\n"
                for iter_list in CMD_LIST[i]:
                    string += "    `" + str(iter_list) + "`"
                    string += "\n"
                string += "\n"
            if len(string) > 4095:
                with io.BytesIO(str.encode(string)) as out_file:
                    out_file.name = "cmd.txt"
                    await bot.send_file(
                        event.chat_id,
                        out_file,
                        force_document=True,
                        allow_cache=False,
                        caption="**ℂ𝕆𝕄𝕄𝔸ℕ𝔻𝕊**",
                        reply_to=reply_to_id,
                    )
                    await event.delete()
            else:
                await event.edit(string)
        elif input_str:
            if input_str in CMD_LIST:
                string = "Commands found in {}:".format(input_str)
                for i in CMD_LIST[input_str]:
                    string += "    " + i
                    string += "\n"
                await event.edit(string)
            else:
                await event.edit(input_str + " is not a valid plugin!")
        else:
            help_string = f"""👩‍💻υѕєявσт-нєℓρєя.. ρяσνι∂є∂ ƒσя - **{DEFAULTUSER}**\n
`Userbot Helper to reveal all the commands`\n🔖𝗗𝗼 .help plugin_name ƒσя 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦"""
            results = await bot.inline_query(  
                tgbotusername, help_string
            )
            await results[0].click(
                event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
            )
            await event.delete()

