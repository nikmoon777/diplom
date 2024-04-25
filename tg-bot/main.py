import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated

import pyrogram_client
from commands.command import CommandContainer, Command
from commands.errors import CommandError, CommandNotFound
from core.executions import check_user, user_banned, get_my_id, get_id, unban_user, get_user, \
    delete_user, set_user, add_user, HELP, ban_user
from core.executions_callback import get_proofs_check_user, about_user
from templates.template import template_get

START_HANDLER_TEMPLATE = 'start'

TOKEN = getenv('TG_SCAM_BOT')
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

cmd_box = CommandContainer()
cmd_box.add_command(Command(['/help', '/хелп'], HELP))
cmd_box.add_command(Command(['/myid', '/яид'], get_my_id))
cmd_box.add_command(Command(['/id', '/ид'], get_id))
cmd_box.add_command(Command(['/check', '/проверить', '/чек', 'чек'], check_user))
cmd_box.add_command(Command(['/ban', '/бан'], ban_user))
cmd_box.add_command(Command(['/banchat'], lambda x: None))
cmd_box.add_command(Command(['/unban', '/разбан'], unban_user))
cmd_box.add_command(Command(['/getuser', '/get', '/гетюзер', '/гет'], get_user))
cmd_box.add_command(Command(['/deluser', '/del', '/делюзер', '/дел'], delete_user))
cmd_box.add_command(Command(['/setuser', '/set', '/сетюзер', '/сет'], set_user))
cmd_box.add_command(Command(['/adduser', '/add', '/юзер', '/добавить'], add_user))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(template_get(START_HANDLER_TEMPLATE, message.from_user.full_name))


@dp.callback_query()
async def callback_query_handler(callback_query: CallbackQuery) -> None:
    data_args = callback_query.data.split()
    try:
        if data_args[0] == 'check':
            await get_proofs_check_user(callback_query, data_args[1:])
        elif data_args[0] == 'helpmore':
            await callback_query.message.edit_text(template_get('help_more'))
        elif data_args[0] == 'about':
            await about_user(callback_query, data_args[1:])
    except BaseException as ex:
        logging.log(logging.INFO, f'Error -> {ex.args[0]}')


@dp.message()
async def echo_handler(message: types.Message) -> None:
    try:
        if message.text is None and message.new_chat_members is not None:
            me = await bot.get_me()
            for chat_member in message.new_chat_members:
                if me.id == chat_member.id:
                    await message.answer(template_get('new_chat', '[обратитесь к администратору]'))
        if message.text is not None or message.caption is not None:
            await cmd_box.get_command(message.text.split()[0] if message.text else message.caption.split()[0])\
                .execute(message)
    except CommandNotFound:
        if message.text.startswith('/'):
            await message.reply('Команда не найдена')
    except CommandError as ex:
        await message.answer('Произошла ошибка при обработке команды: Неверные аргументы\n\n' + str(ex.args[0]))
    except RuntimeError as ex:
        logging.log(logging.INFO, f'Error -> {ex.args[0]}')
        await message.reply('Произошла ошибка при выполнении команды')


@dp.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def join_chat(event: ChatMemberUpdated) -> None:
    if await user_banned(str(event.new_chat_member.user.id), 1):
        await event.chat.ban(event.new_chat_member.user.id)


@dp.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def left_chat(event: ChatMemberUpdated) -> None:
    pass


async def start_pyrogram() -> None:
    await pyrogram_client.client.connect()
    await pyrogram_client.client.authorize()


async def main() -> None:
    asyncio.get_running_loop().create_task(start_pyrogram())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
