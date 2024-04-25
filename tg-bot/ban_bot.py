from os import getenv

from pyrogram import Client, filters
from pyrogram.types import Message

from core.api.request import TgAccess, ApiRequest, Requests

app = Client(name='ban_bot', api_id=int(getenv('TG_SCAM_BAN_BOT_API_ID')), api_hash=getenv('TG_SCAM_BAN_BOT_API_HASH'))
access = TgAccess('oiehf8h9w38hwp8fhsbriguvbsviusbrv98wh9p8owijfoiwhefiuwhef932wfi')
request = ApiRequest(access)


@app.on_message(filters.group)
async def message(client: Client, message: Message):
    if message.from_user and message.text == '/banchat':
        me = await client.get_chat_member(message.chat.id, client.me.id)
        if not me.privileges.can_restrict_members:
            await message.reply('Я не могу удалять пользователей в этом чате!')
            return
        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status in [user.status.ADMINISTRATOR, user.status.OWNER]:
            async for member in client.get_chat_members(message.chat.id):
                if request.check_user(message.from_user.id, member.user.id):
                    await message.chat.ban_member(member.user.id)
            await message.delete()
        else:
            await message.reply('Не удалось')


app.run()
