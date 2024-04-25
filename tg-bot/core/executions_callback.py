from aiogram.types import CallbackQuery, InputMediaPhoto

from core.api.errors.errors import ApiError
from core.api.request import TgAccess, ApiRequest
from core.api.entities.user import User

access = TgAccess('oiehf8h9w38hwp8fhsbriguvbsviusbrv98wh9p8owijfoiwhefiuwhef932wfi')
request = ApiRequest(access)


async def get_proofs_check_user(callback_query: CallbackQuery, args: list):
    try:
        ban_inf = request.get_ban_info(int(args[0]))
        images = ban_inf.proofs['images']
        if len(images):
            await callback_query.message.edit_media(InputMediaPhoto(media=images[0], caption=ban_inf.cause))
        else:
            await callback_query.message.edit_caption(caption=ban_inf.cause)
    except ApiError:
        await callback_query.answer('Нет пруфов')


async def about_user(callback_query: CallbackQuery, args: list):
    user: User = request.get_user(callback_query.bot.id, int(args[0]))[1]
    try:
        await callback_query.message.reply(f'Подробная информация о пользователе.\nИдентификатор: {user.tg_id}\n'
                                           f'Игровое имя: {"Отсутствует" if user.gamenick is None else user.gamenick}')
    except:
        await callback_query.answer('Пользователь не найден в базе')
