from os import getenv

from pyrogram import Client

client = Client(name='bot', api_id=int(getenv('TG_SCAM_BAN_BOT_API_ID')), api_hash=getenv('TG_SCAM_BAN_BOT_API_HASH'),
                bot_token=getenv('TG_SCAM_BOT'))


def pyronect(f):
    async def wrap(*args, **kwargs):
        try:
            await client.connect()
            result = await f(*args, *kwargs)
            return result
        except RuntimeError:
            pass
        finally:
            await client.disconnect()
    return wrap


async def get_user(user_id: str | int):
    return await client.get_users(user_id)


async def get_chat_users(chat_id: int):
    ids = []
    async for member in client.get_chat_members(chat_id):
        ids.append(member.chat.id)
    return ids


async def get_me():
    return await client.get_me()
