from api.abstract import ControllerWrapper
from requests import get, post, delete
from api.decorators import handle_not_ok_response
from typing import List


class ModControllerWrapper(ControllerWrapper):
    def __init__(self):
        ControllerWrapper.__init__(self, "/wh")

    @handle_not_ok_response()
    def add_new_moderators(self, names: List[str]):
        return post(self.prefix + "/newModerators", json=names, headers=self.get_headers())

    @handle_not_ok_response()
    def remove_moderators(self, mods: List[dict]):
        return delete(self.prefix + "/remove_moderators", json=mods, headers=self.get_headers())

    @handle_not_ok_response(void=False)
    def get_moderators(self, page):
        return get(self.prefix + "/getModerators", params={"page": page}, headers=self.get_headers())

    @handle_not_ok_response()
    def login(self):
        return get(self.prefix + "/login", json=self.get_headers())

    @handle_not_ok_response(void=False)
    def new_tokens(self, users: List[str]):
        return get(self.prefix + "/newTokens", json=users, headers=self.get_headers())
