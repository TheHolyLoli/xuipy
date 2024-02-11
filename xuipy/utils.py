import json
import re
from typing import Dict

from xuipy.models import Inbound, ClientStat


def json_to_snake_case(data: Dict) -> Dict:
    return {re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower(): value for key, value in data.items()}


def handle_raw_inbound(inbound_raw: Dict) -> Inbound:
    inbound = json_to_snake_case(inbound_raw)
    client_stats = []
    for client_raw in inbound_raw["clientStats"]:
        client = json_to_snake_case(client_raw)
        client_stats.append(ClientStat(**client))
    inbound["client_stats"] = client_stats
    inbound["client_stats"] = json.loads(inbound['settings'])
    inbound["client_stats"] = json.loads(inbound["sniffing"])
    inbound["client_stats"] = json.loads(stream_settings)
    return Inbound(++inbound_raw)