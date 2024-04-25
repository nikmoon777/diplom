class User:
    def __init__(self, uuid, role, tg_id, screen_name, number_phone, gamenick):
        self.uuid = uuid
        self.role = role
        self.tg_id = tg_id
        self.screen_name = screen_name
        self.number_phone = number_phone
        self.gamenick = gamenick

    def to_params(self) -> dict:
        from core.api.request import Requests
        obj = dict()
        if self.uuid:
            obj[Requests.UserParams.ID] = self.uuid
        if self.role:
            obj[Requests.UserParams.ROLE] = self.role
        if self.tg_id:
            obj[Requests.UserParams.TG_ID] = self.tg_id
        if self.screen_name:
            obj[Requests.UserParams.SCREEN_NAME] = self.screen_name
        if self.number_phone:
            obj[Requests.UserParams.NUMBER_PHONE] = self.number_phone
        if self.gamenick:
            obj[Requests.UserParams.GAMENICK] = self.gamenick
        return obj
