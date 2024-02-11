from dataclasses import dataclass
from typing import List, Optional, Union, Dict, Any
from uuid import UUID

from requests.structures import CaseInsensitiveDict
from pydantic import BaseModel, ConfigDict
from pydantic.dataclasses import dataclass


class Result(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    status_code: int
    headers: CaseInsensitiveDict
    success: bool
    message: Optional[str]
    data: Optional[Union[list, dict]]

@dataclass
class Client:
    email: str
    enable: bool
    id: Optional[UUID] = None
    password: Optional[str] = None
    flow: Optional[str] = None
    total_gb: Optional[int] = None
    limit_ip: Optional[int] = None
    sub_id: Optional[str] = None
    tg_id: Optional[str] = None
    expiry_time: Optional[int] = None
    reset: Optional[int] = None


@dataclass
class ClientStat:
    id: int
    inbound_id: int
    enable: bool
    email: str
    up: int
    down: int
    total: int
    reset: int
    expiry_time: Optional[int] = None


@dataclass
class InboundSettings:
    clients: List[Client]

@dataclass
class InboundSniffing:
    enabled: bool
    dest_override: List[str]


@dataclass
class WSSettings:
    path: str
    headers: Optional[Dict] = None
    accept_proxy_protocol: Optional[bool] = None


@dataclass
class InboundStreamSettings:
    network: str
    security: str
    external_proxy: Optional[List] = None
    ws_settings: Optional[WSSettings] = None

@dataclass
class Inbound:
    id: int
    up: int
    down: int
    total: int
    remark: str
    enable: bool
    expiry_time: int
    client_stats: Optional[List[ClientStat]]
    listen: str
    port: int
    protocol: str
    settings: InboundSettings
    stream_settings: InboundStreamSettings
    tag: str
    sniffing: InboundSniffing

