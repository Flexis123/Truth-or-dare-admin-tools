from api.abstract import ControllerWrapper
from requests import get


class PropsController(ControllerWrapper):
    def __init__(self):
        ControllerWrapper.__init__(self, "/props")

    def get_config(self):
        return get(self.prefix + "/mod").json()

