from abc import ABC
import constants
from copy import deepcopy


class ControllerWrapper(ABC):
    def __init__(self, prefix):
        self.prefix = constants.BASE_URL + prefix

    def get_headers(self, **headers):
        h = deepcopy(constants.auth_body)
        h.update(headers)
        return h
