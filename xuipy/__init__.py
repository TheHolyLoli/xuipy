import json
import logging
from typing import Iterator, Callable

from xuipy import utils
from xuipy.rest_adapter import RestAdapter
from xuipy.exceptions import XuipyException
from xuipy.models import *


class Xuipy:
    def __init__(self, hostname: str,
                 port: int = 443, https: bool = False, path: str = "",
                 ssl_verify: bool = True, logger: logging.Logger = None):
        self._rest_adapter = RestAdapter(hostname, port, https, path, ssl_verify, logger)

    def login(self, username: str, password: str) -> Result:
        result = self._rest_adapter.post('/login',
                                         data={"username": username, "password": password}, prefix="")
        return result

    def get_all_inbounds(self) -> List[Inbound]:
        result = self._rest_adapter.get(endpoint="/")
        inbounds = []
        inbounds_raw = result.data
        for inbound_raw in inbounds_raw:
            inbounds.append(utils.handle_raw_inbound(inbound_raw))
        return inbounds

    def get_inbound(self,inbound_id: int) -> Inbound:
        result = self._rest_adapter.get(f"/get/{inbound_id}")
        if not result.data:
            raise XuipyException(result.message)
        return utils.handle_raw_inbound(result.data)

    def create_backup(self):
        result = self._rest_adapter.get("/createbackup")
        return True
