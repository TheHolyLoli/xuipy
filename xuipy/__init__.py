import json
import logging
from typing import Iterator,Callable

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
            inbound = utils.json_to_snake_case(inbound_raw)
            clients = []
            for client_raw in inbound_raw["clientStats"]:
                client = utils.json_to_snake_case(client_raw)
                clients.append(client)
            inbound["client_stats"] = clients
            inbound["settings"] = utils.json_to_snake_case(json.loads(inbound['settings']))
            for idx,settings_client in enumerate(inbound["settings"]["clients"]):
                inbound["settings"]["clients"][idx] = utils.json_to_snake_case(settings_client)
            inbound["sniffing"] = utils.json_to_snake_case(json.loads(inbound["sniffing"]))
            inbound["stream_settings"] = utils.json_to_snake_case(json.loads(inbound["stream_settings"]))

            inbounds.append(Inbound(**inbound))
            # client_stats = []
            # inbound = utils.json_to_snake_case(inbound_raw)
            # for client_raw in inbound_raw["clientStats"]:
            #     client = utils.json_to_snake_case(client_raw)
            #     client_stats.append(ClientStat(**client))
            # inbound["client_stats"] = client_stats

            inbounds.append(Inbound(**inbound))
        return inbounds
