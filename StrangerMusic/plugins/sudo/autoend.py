

from pyrogram import filters
from pyrogram.types import Message
from strings import get_command
from StrangerMusic import app
from StrangerMusic.misc import SUDOERS
from StrangerMusic.utils.database import autoend_off, autoend_on

# Commands
AUTOEND_COMMAND = get_command("AUTOEND_COMMAND")


@app.on_message(filters.command(AUTOEND_COMMAND) & SUDOERS)
async def auto_end_stream(client, message:Message):
    usage = "**Usage:**\n\n/autoend [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await autoend_on()
        await message.reply_text(
            "Auto End Stream Enabled.\n\nBot will leave voice chat automatically after 3 mins if no one is listening with a warning message.."
        )
    elif state == "disable":
        await autoend_off()
        await message.reply_text("Auto End Stream Disabled.")
    else:
        await message.reply_text(usage)
