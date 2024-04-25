import json

from requests import get, post, put, patch, delete

from core.api.entities.ban_info import BanInfo
from core.api.entities.user import User
from core.api.errors.errors import ApiError


class TgAccess:
    def __init__(self, secret):
        self._secret = secret

    def build(self, tg_id: int) -> str:
        return f'{self._secret}[{tg_id}]'


class Requests:
    ORIGIN = 'http://localhost:8080'

    GET_USER = '/users/search/byTg'
    GET_USER_BY_NAME = '/users/search/byName'
    GET_USER_BY_PHONE = '/users/search/byPhone'
    GET_CHECK_BAN = '/ban/search/existsByUser'
    GET_BAN_INFO = '/ban/search/byTgId'

    POST_ADD_USER = '/users'
    POST_BAN_USER = '/ban'

    PUT_USERS_SET = '/users'

    PATCH_BAN_SET = '/ban'

    DELETE_BAN = '/ban'
    DELETE_USER = '/users'

    RESPONSE_OK_RANGE = range(200, 301)

    RESPONSE_OK = 200, 'OK'
    RESPONSE_ACCESS_DENIED = 403, 'Access denied'
    RESPONSE_NOT_FOUND = 404, 'Not Found'

    class UserParams:
        ID = 'id'
        ROLE = 'role'
        TG_ID = 'tgId'
        SCREEN_NAME = 'screenName'
        NUMBER_PHONE = 'numberPhone'
        GAMENICK = 'gamenick'

    class BanParams:
        ID = 'id'
        USER = 'user'
        USER_ID = 'id'
        OWNER_ID = 'owner'
        CAUSE = 'cause'
        PROOFS = 'proofs'


class ApiRequest:
    HEADER_TG_ACCESS = 'Access-Telegram'

    def __init__(self, access: TgAccess):
        self._access = access

    def _build_access_header(self, tg_id) -> dict:
        return {ApiRequest.HEADER_TG_ACCESS: self._access.build(tg_id)}

    def _packing_user(self, response):
        if response.status_code == Requests.RESPONSE_OK[0]:
            obj = response.json()
            return User(obj[Requests.UserParams.ID], obj[Requests.UserParams.ROLE], obj[Requests.UserParams.TG_ID],
                        obj[Requests.UserParams.SCREEN_NAME], obj[Requests.UserParams.NUMBER_PHONE],
                        obj[Requests.UserParams.GAMENICK])
        elif response.status_code == Requests.RESPONSE_ACCESS_DENIED[0]:
            return Requests.RESPONSE_ACCESS_DENIED[1]
        elif response.status_code == Requests.RESPONSE_NOT_FOUND[0]:
            return Requests.RESPONSE_NOT_FOUND[1]

    def _packing_ban_info(self, response) -> tuple:
        if response.ok:
            obj = response.json()
            return 200, BanInfo(obj[Requests.BanParams.ID], obj[Requests.BanParams.USER][Requests.BanParams.ID],
                                obj[Requests.BanParams.OWNER_ID], obj[Requests.BanParams.CAUSE],
                                obj[Requests.BanParams.PROOFS])
        else:
            return Requests.RESPONSE_NOT_FOUND

    def add_user(self, access_tg_id: int, user: User) -> int:
        obj = json.dumps(user.to_params())
        r = post(f'{Requests.ORIGIN}{Requests.POST_ADD_USER}', obj, headers=self._build_access_header(access_tg_id))
        return r.status_code

    def set_user(self, access_tg_id: int, user: User) -> int:
        obj = user.to_params()
        user_uuid = user.uuid
        r = put(f'{Requests.ORIGIN}{Requests.PUT_USERS_SET}/{user_uuid}', json.dumps(obj),
                headers=self._build_access_header(access_tg_id))
        return r.status_code

    def get_user(self, access_tg_id: int, tg_id: int) -> tuple:
        response = get(f'{Requests.ORIGIN}{Requests.GET_USER}',
                       params={Requests.UserParams.TG_ID: tg_id},
                       headers=self._build_access_header(access_tg_id))
        return response.status_code, self._packing_user(response)

    def delete_user(self, access_tg_id: int, tg_id: int) -> None:
        user_info = self.get_user(access_tg_id, tg_id)
        if user_info[0] != Requests.RESPONSE_OK[0]:
            raise ApiError('User not found')
        user = user_info[1]
        r = delete(f'{Requests.ORIGIN}{Requests.DELETE_USER}/{user.uuid}',
                   headers=self._build_access_header(access_tg_id))
        if not r.ok:
            raise ApiError(f'Oops! {r.status_code}')

    def get_user_by(self, access_tg_id: int, screen_name: str = None, phone: str = None):
        url = Requests.ORIGIN + (Requests.GET_USER_BY_NAME if screen_name else Requests.GET_USER_BY_PHONE)
        param = Requests.UserParams.SCREEN_NAME if screen_name else Requests.UserParams.NUMBER_PHONE
        response = get(url, {param: screen_name if screen_name else phone},
                       headers=self._build_access_header(access_tg_id))
        return response.status_code, self._packing_user(response)

    def check_user(self, access_tg_id: int, tg_id: int = None, screen_name: str = None, phone: str = None) -> bool:
        if tg_id:
            return get(f'{Requests.ORIGIN}{Requests.GET_CHECK_BAN}', params={Requests.UserParams.TG_ID: tg_id}).json()
        elif screen_name or phone:
            res = self.get_user_by(access_tg_id, screen_name=screen_name, phone=phone)
            if res[0] != Requests.RESPONSE_OK[0]:
                raise ApiError('Incorrect user')
            return self.check_user(0, res[1].tg_id)

    def ban_user(self, access_tg_id: int, tg_id: int, ban_inf: BanInfo) -> int:
        api = self.get_user(access_tg_id, tg_id)
        if api[0] not in Requests.RESPONSE_OK_RANGE:
            raise ApiError('User not found')
        user = api[1]
        ban_inf.user_id = user.uuid
        ban_data = ban_inf.to_params()
        del ban_data[Requests.BanParams.ID]
        r = post(f'{Requests.ORIGIN}{Requests.POST_BAN_USER}', json.dumps(ban_data),
                 headers=self._build_access_header(access_tg_id))
        return r.status_code

    def set_ban_info(self, access_tg_id: int, ban_inf: BanInfo):
        ban_id = ban_inf.uuid
        ban_data = ban_inf.to_params()
        del ban_data[Requests.BanParams.ID]
        r = patch(f'{Requests.ORIGIN}{Requests.PATCH_BAN_SET}/{ban_id}', json.dumps(ban_data),
                  headers=self._build_access_header(access_tg_id))
        return r.status_code

    def get_ban_info(self, tg_id: int) -> BanInfo:
        r = get(f'{Requests.ORIGIN}{Requests.GET_BAN_INFO}', {Requests.UserParams.TG_ID: tg_id})
        ban_inf = self._packing_ban_info(r)
        if ban_inf[0] != Requests.RESPONSE_OK[0]:
            raise ApiError('Ban not found')
        return ban_inf[1]

    def delete_ban_info(self, access_tg_id: int, tg_id: int) -> None:
        ban_info = self.get_ban_info(tg_id)
        r = delete(f'{Requests.ORIGIN}{Requests.DELETE_BAN}/{ban_info.uuid}',
                   headers=self._build_access_header(access_tg_id))
        if not r.ok:
            raise ApiError(f'Oops! {r.status_code}')
