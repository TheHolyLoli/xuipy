import json
import re
from typing import Dict

from xuipy.models import Inbound, ClientStat


def json_to_snake_case(data: Dict) -> Dict:
    return {re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower(): value for key, value in data.items()}


def handle_raw_inbound(inbound_raw: Dict) -> Inbound:
    inbound = json_to_snake_case(inbound_raw)
    clients = []
    if "client_stats" in inbound and inbound["client_stats"]:
        for client_raw in inbound["client_stats"]:
            client = json_to_snake_case(client_raw)
            clients.append(client)
    inbound["client_stats"] = clients
    inbound["settings"] = json_to_snake_case(json.loads(inbound['settings']))
    for idx, settings_client in enumerate(inbound["settings"]["clients"]):
        inbound["settings"]["clients"][idx] = json_to_snake_case(settings_client)
    inbound["sniffing"] = json_to_snake_case(json.loads(inbound["sniffing"]))
    inbound["stream_settings"] = json_to_snake_case(json.loads(inbound["stream_settings"]))
    return Inbound(**inbound)