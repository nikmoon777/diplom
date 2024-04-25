from aiogram.types import Message, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

import pyrogram_client
from commands.errors import CommandError
from commands.utils import is_number_phone, is_username, normalize_username, NUMBER_PHONE_LENGTH_RU
from core.api.entities.ban_info import BanInfo
from core.api.entities.user import User
from core.api.errors.errors import ApiError
from core.api.request import TgAccess, ApiRequest, Requests
from templates.template import template_get

access = TgAccess('oiehf8h9w38hwp8fhsbriguvbsviusbrv98wh9p8owijfoiwhefiuwhef932wfi')
request = ApiRequest(access)


async def HELP(message: Message) -> None:
    args = message.text.split()
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Описание форматирования', callback_data=f'helpmore')
    if len(args) < 2:
        await message.reply(template_get('help'), reply_markup=keyboard_builder.as_markup())
    else:
        try:
            await message.reply(template_get(args[1]))
        except KeyError:
            await message.reply('Команда не была найдена')


async def user_banned(user_data: str, from_uid: int) -> bool:
    try:
        if user_data.isdigit():
            exists = request.check_user(from_uid, int(user_data))
        elif is_number_phone(user_data, NUMBER_PHONE_LENGTH_RU):
            exists = request.check_user(from_uid, phone=user_data)
        elif is_username(user_data):
            exists = request.check_user(from_uid, screen_name=normalize_username(user_data))
        else:
            raise CommandError()
        return exists
    except ApiError:
        pass
    except BaseException:
        raise CommandError('Incorrect command args\n' + template_get('check'))


async def check_user(message: Message) -> None:
    args = message.text.split()[1:]
    if len(args):
        user_search_param = args[0]
        if user_search_param.lower() == 'я':
            user_search_param = str(message.from_user.id)
    else:
        if not message.reply_to_message:
            raise CommandError(template_get('check'))
        user_search_param = str(message.reply_to_message.from_user.id)
    if is_username(user_search_param):
        pyrogram_user = await pyrogram_client.get_user(user_search_param)
        user_search_param = str(pyrogram_user.id)
    exists = await user_banned(user_search_param, message.from_user.id)

    if exists:
        file = FSInputFile('./assets/check_user__exists_in_base.jpg')
        ban_info = request.get_ban_info(int(user_search_param))
        if ban_info.owner_id is not None:
            user_owner_ban = await pyrogram_client.get_user(ban_info.owner_id['tgId'])
            ban_own_msg = f'\nЗабанил(-a): @{user_owner_ban.username}'
        else:
            ban_own_msg = f'\nЗабанил(-а): Неизвестно'
    else:
        file = FSInputFile('./assets/check_user__not_found_in_base.jpg')
        ban_own_msg = ''

    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Показать пруфы', callback_data=f'check {user_search_param}')
    keyboard_builder.button(text='Подробнее', callback_data=f'about {user_search_param}')
    await message.answer_photo(file, 'Пользователь проверен' + ban_own_msg, reply_markup=keyboard_builder.as_markup())


async def get_my_id(message: Message) -> None:
    await message.reply(str(message.from_user.id))


async def get_id(message: Message) -> None:
    try:
        await message.reply(str(message.reply_to_message.from_user.id))
    except BaseException:
        raise CommandError('get_id')


async def ban_user(message: Message) -> None:
    text = message.text if message.text else message.caption
    try:
        if message.reply_to_message:
            fwd = message.reply_to_message
            tg_username = fwd.from_user.username
            tg_id = fwd.from_user.id
            cause_ban = ' '.join(text.split()[1:])
        else:
            tg_id = tg_username = None
            if '\n' in text:
                args_user, cause_ban = text.split('\n')
            else:
                args_user, cause_ban = text, ''

            for arg in args_user.split()[1:]:
                if arg.isdigit():
                    tg_id = int(arg)
                elif is_username(arg):
                    tg_username = normalize_username(arg)
                elif is_number_phone(arg, NUMBER_PHONE_LENGTH_RU):
                    await message.reply('Номер телефона больше не поддерживается')

            if not tg_username and not tg_id:
                raise RuntimeError()
            elif tg_id:
                user = await pyrogram_client.get_user(tg_id)
                tg_username = user.username
            else:
                user = await pyrogram_client.get_user(tg_username)
                tg_id = user.id
    except BaseException as ex:
        print(ex.args)
        raise CommandError('ban_user')

    user = request.get_user(message.from_user.id, tg_id)
    if user[0] in Requests.RESPONSE_OK_RANGE:
        user = user[1]
    else:
        await message.reply('Пользователь был добавлен в базу')
        new_user = User(None, 'USER', tg_id, tg_username, None, None)
        request.add_user(message.from_user.id, new_user)
        user = request.get_user(message.from_user.id, new_user.tg_id)[1]

    photos = []
    if message.photo is not None:
        photos.append(message.photo[-1].file_id)

    owner_ban_user: User = request.get_user(message.from_user.id, message.from_user.id)[1]
    ban_info = BanInfo(None, user.uuid, owner_ban_user.uuid, cause_ban.strip(), {'images': photos})
    if request.ban_user(message.from_user.id, user.tg_id, ban_info) in Requests.RESPONSE_OK_RANGE:
        await message.reply('OK')
    else:
        await message.reply('ERROR')


# DEPRECATED
async def ban_user_old(message: Message) -> None:
    text = message.text if message.text else message.caption
    uuid = number_phone = None
    role = 'USER'
    try:
        if message.reply_to_message:
            fwd = message.reply_to_message
            user = User(uuid, role, fwd.from_user.id, fwd.from_user.username, number_phone)
            ban_cause = ' '.join(text.split()[1:])
        else:
            tg_id = screen_name = None
            user_ban = text.split('\n')
            user_info = user_ban[0]
            ban_cause = user_ban[1] if len(user_ban) > 1 else ''
            args = user_info.split()[1:]
            for arg in args:
                if arg.isdigit():
                    tg_id = int(arg)
                elif is_number_phone(arg, NUMBER_PHONE_LENGTH_RU):
                    number_phone = arg
                else:
                    screen_name = normalize_username(arg)
            user = User(uuid, role, tg_id, screen_name, number_phone)
        photo_ids = []
        if message.photo is not None:
            photo_ids.append(message.photo[-1].file_id)
        ban_inf = BanInfo('', user.uuid, ban_cause.strip(), {'images': photo_ids})
    except BaseException:
        raise CommandError('ban_user')
    base_user = request.get_user(message.from_user.id, user.tg_id)
    if base_user[0] == Requests.RESPONSE_NOT_FOUND[0]:
        request.add_user(message.from_user.id, user)
    code = request.ban_user(message.from_user.id, user.tg_id, ban_inf)
    if code not in Requests.RESPONSE_OK_RANGE:
        await message.reply('Already')
    else:
        await message.reply('OK')


async def _pull_tg_id_from_message(message: Message) -> int:
    if message.reply_to_message:
        return message.reply_to_message.from_user.id
    else:
        try:
            data = message.text.split()[1]
            tg_id = 0
            if is_username(data):
                user = await pyrogram_client.get_user(data)
                tg_id = user.id
            return tg_id if tg_id else int(data)
        except BaseException:
            raise CommandError('Args error')


async def unban_user(message: Message) -> None:
    request.delete_ban_info(message.from_user.id, await _pull_tg_id_from_message(message))
    await message.reply('OK')


async def get_user(message: Message) -> None:
    user_info = request.get_user(message.from_user.id, await _pull_tg_id_from_message(message))
    if user_info[0] != Requests.RESPONSE_OK[0]:
        raise ApiError('User not found')
    user = user_info[1]
    await message.reply(f'User Info.\nsystem_id: {user.uuid}\ntg_id: {user.tg_id}\nrole: {user.role}\n'
                        f'username: {user.screen_name}\nphone: {user.number_phone}\ngamenick: {user.gamenick}')


async def delete_user(message: Message) -> None:
    request.delete_user(message.from_user.id, await _pull_tg_id_from_message(message))
    await message.reply('OK')


async def set_user(message: Message) -> None:
    user_info = list()
    try:
        tg_id = await _pull_tg_id_from_message(message)
        #                       first arg (tg_id) in dependency from reply_to_message not required
        args = message.text.split()[(1 if message.reply_to_message else 2):]
        for arg in args:
            key, value = arg.split(':')
            user_info.append((key, value))
    except BaseException:
        raise CommandError('Args error')
    user = request.get_user(message.from_user.id, tg_id)
    if user[0] != Requests.RESPONSE_OK[0]:
        raise CommandError('User not found')
    user = user[1]
    for key, value in user_info:
        if key == 'role':
            user.role = value
        elif key == 'username':
            user.screen_name = normalize_username(value)
        elif key == 'phone':
            user.number_phone = value
        elif key == 'gamenick':
            user.gamenick = value
    request.set_user(message.from_user.id, user)
    await message.reply('OK')


async def add_user(message: Message) -> None:
    text = message.text
    uuid = number_phone = None
    role = 'USER'
    try:
        if message.reply_to_message:
            fwd = message.reply_to_message
            user = User(uuid, role, fwd.from_user.id, fwd.from_user.username, number_phone)
        else:
            tg_id = screen_name = None
            args = text.split()[1:]
            for arg in args:
                if arg.isdigit():
                    tg_id = int(arg)
                elif is_number_phone(arg, NUMBER_PHONE_LENGTH_RU):
                    number_phone = arg
                else:
                    screen_name = normalize_username(arg)
            user = User(uuid, role, tg_id, screen_name, number_phone, None)
    except BaseException:
        raise CommandError('ban_user')
    status = request.add_user(message.from_user.id, user)
    if status not in Requests.RESPONSE_OK_RANGE:
        raise CommandError('User has not been added')
    await message.reply('OK')
