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

    def get_inbound(self, inbound_id: int) -> Inbound:
        result = self._rest_adapter.get(f"/get/{inbound_id}")
        if not result.data:
            raise XuipyException(result.message)
        return utils.handle_raw_inbound(result.data)

    def create_backup(self):
        result = self._rest_adapter.get("/createbackup")
        return True

    def add_inbound(self, inbound: Inbound) -> Inbound:
        pass

    def delete_inbound(self, inbound_id: int) -> Result:
        return self._rest_adapter.post(f"/del/{inbound_id}")


    def update_inbound(self, inbound_id: int) -> Inbound:
        pass

    def add_client(self, inbound_id: int, email: str, uuid: Optional[Union[UUID,str]] = None, password: Optional[str] = None, enable: bool = True,
                   flow: Optional[str] = "", limit_ip: Optional[int] = None, total_traffic: Optional[int] = 0,
                   expire_time: Optional[int] = None,  # TODO : support Datetime directly
                   telegram_id: Optional[Union[str, int]] = None, subscription_id: Optional[Union[str, int]] = None
                   ) -> Result:

        settings = {
            "clients": [
                {
                    "id": uuid,
                    "email": email,
                    "enable": enable,
                    "flow": flow,
                    "limitIp": limit_ip,
                    "totalGB": total_traffic,
                    "tgId": telegram_id,
                    "subId": subscription_id
                }
            ],
            "decryption": "none",
            "fallbacks": []
        }
        if expire_time:
            settings["clients"][0]["expiryTime"] = expire_time

        data = {
            "id": inbound_id,
            "settings": json.dumps(settings)
        }
        return self._rest_adapter.post(f"/addClient", data=data)

    def delete_client(self, inbound_id: int, client_uuid: UUID) -> Result:
        return self._rest_adapter.post(f"/:{inbound_id}/delClient/{client_uuid}")

    def update_client(self, inbound_id: int, email: str, uuid: Optional[Union[UUID,str]] = None, password: Optional[str] = None,
                       enable: bool = True,
                       flow: Optional[str] = "", limit_ip: Optional[int] = None, total_traffic: Optional[int] = 0,
                       expire_time: Optional[int] = None,  # TODO : support Datetime directly
                       telegram_id: Optional[Union[str, int]] = None, subscription_id: Optional[Union[str, int]] = None
                       ) -> Client:
            settings = {
                "clients": [
                    {
                        "id": uuid,
                        "email": email,
                        "enable": enable,
                        "flow": flow,
                        "limitIp": limit_ip,
                        "totalGB": total_traffic,
                        "tgId": telegram_id,
                        "subId": subscription_id
                    }
                ],
                "decryption": "none",
                "fallbacks": []
            }
            if expire_time:
                settings["clients"][0]["expiryTime"] = expire_time

            data = {
                "id": inbound_id,
                "settings": json.dumps(settings)
            }
            return self._rest_adapter.post(f"/updateClient/{uuid}", data=data)

    def get_client_traffic(self, client_email: Union[int, str]) -> ClientStat:
        result = self._rest_adapter.get(f"/getClientTraffics/{client_email}")
        if result.success and result.data:
            return ClientStat(**utils.json_to_snake_case(result.data))

    def reset_client_traffic(self, inbound_id: int, client_email: Union[int, str]) -> Result:
        return self._rest_adapter.post(f"/{inbound_id}/resetClientTraffic/{client_email}")

    def reset_all_inbounds_traffic(self) -> Result:
        return self._rest_adapter.post("/resetAllTraffics")

    def reset_inbound_clients_traffic(self, inbound_id: Union[int]) -> Result:
        return self._rest_adapter.post(f"/resetAllClientTraffics/{inbound_id}")

    def delete_depleted_clients(self, inbound_id: int) -> Result:
        return self._rest_adapter.post(f"/delDepletedClients/{inbound_id}")

    def get_get_onlines(self) -> List[str]:
        return self._rest_adapter.post("/onlines")
