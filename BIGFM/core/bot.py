# BIGFM/core/call/bot.py

import asyncio

# 🔧 Ensure a running event loop before installing uvloop (Heroku safe)
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# ✅ Install uvloop if available (optional performance boost)
try:
    import uvloop
    uvloop.install()
except ImportError:
    pass

from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER


class Aviax(Client):
    def init(self):
        LOGGER(name).info("🚀 Starting BIGFM Music Bot...")
        super().init(
            name="BIGFM",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        """Start the bot and verify access to the log group."""
        await super().start()

        self.id = self.me.id
        self.name = self.me.first_name + (f" {self.me.last_name}" if self.me.last_name else "")
        self.username = self.me.username or "Unknown"
        self.mention = self.me.mention

        # 🔹 Send startup message to log group
        try:
            await self.send_message(
                chat_id=config.LOG_GROUP_ID,
                text=(
                    f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\n"
                    f"ɪᴅ : <code>{self.id}</code>\n"
                    f"ɴᴀᴍᴇ : {self.name}\n"
                    f"ᴜsᴇʀɴᴀᴍᴇ : @{self.username}"
                ),
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(name).error(
                "❌ Bot cannot access LOG_GROUP_ID.\n"
                "Please ensure the bot is added to the log group/channel."
            )
            exit()
        except Exception as ex:
            LOGGER(name).error(
                f"❌ Unexpected error accessing log group: {type(ex).name}."
            )
            exit()

        # 🔹 Check admin permissions in log group
        try:
            member = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(name).error(
                    "⚠️ Please promote the bot as an admin in the log group/channel."
                )
                exit()
        except Exception as ex:
            LOGGER(name).error(f"❌ Failed to verify admin status: {ex}")
            exit()

        LOGGER(name).info(f"✅ BIGFM Music Bot Started as {self.name}")

    async def stop(self):
        """Gracefully stop the bot."""
        await super().stop()
        LOGGER(name).info("🛑 BIGFM Music Bot stopped successfully.")
