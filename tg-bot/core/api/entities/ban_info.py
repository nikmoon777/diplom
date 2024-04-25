class BanInfo:
    def __init__(self, uuid: str, user_id: str, owner_id: str, cause: str, proofs: dict):
        self.uuid = uuid
        self.user_id = user_id
        self.owner_id = owner_id
        self.cause = cause
        self.proofs = proofs

    def to_params(self) -> dict:
        from core.api.request import Requests
        return {
            Requests.BanParams.ID: self.uuid,
            Requests.BanParams.USER: {
                Requests.BanParams.USER_ID: self.user_id
            },
            Requests.BanParams.OWNER_ID: {
                Requests.BanParams.USER_ID: self.owner_id
            },
            Requests.BanParams.CAUSE: self.cause,
            Requests.BanParams.PROOFS: self.proofs
        }
