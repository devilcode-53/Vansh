import asyncio
import uvloop

# Correct: set uvloop as default policy before pyrogram import
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER


class Aviax(Client):
    def init(self):
        LOGGER(name).info("Starting Bot...")
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
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

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
                "Bot failed to access the log group/channel. Make sure it’s added there."
            )
            exit()
        except Exception as ex:
            LOGGER(name).error(
                f"Bot failed to access the log group/channel.\nReason: {type(ex).name}."
            )
            exit()

        a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(name).error(
                "Please promote your bot as an admin in your log group/channel."
            )
            exit()
        LOGGER(name).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()
