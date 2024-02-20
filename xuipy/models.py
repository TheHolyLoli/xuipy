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
class TransmissionTypeHeader:
    type: Optional[str] = None


@dataclass
class WSSettings:
    path: str
    headers: Optional[Dict] = None
    accept_proxy_protocol: Optional[bool] = None


@dataclass
class GrpcSettings:
    service_name: Optional[str] = None
    multi_mode: Optional[bool] = None


@dataclass
class HTTPSettings:
    path: Optional[str] = None
    host: Optional[List[str]] = None


@dataclass
class QuicSettings:
    security: Optional[str] = None
    key: Optional[str] = None
    header: Optional[TransmissionTypeHeader] = None


@dataclass
class KcpSettings:
    mtu: Optional[int] = None
    tti: Optional[int] = None
    uplink_capacity: Optional[int] = None
    downlink_capacity: Optional[int] = None
    congestion: Optional[bool] = None
    read_buffer_size: Optional[int] = None
    write_buffer_size: Optional[int] = None
    header: Optional[TransmissionTypeHeader] = None
    seed: Optional[str] = None


@dataclass
class TCPSettings:
    accept_proxy_protocol: Optional[bool] = None
    header: Optional[TransmissionTypeHeader] = None


@dataclass
class TCPSettingsRequest:
    version: Optional[str] = None
    method: Optional[str] = None
    path: Optional[List[str]] = None
    headers: Optional[dict] = None


@dataclass
class TCPSettingsResponse:
    status: Optional[int] = None
    version: Optional[str] = None
    reason: Optional[str] = None
    headers: Optional[dict] = None


@dataclass
class TCPSettingsHeader:
    type: Optional[str] = None
    request: Optional[TCPSettingsRequest] = None
    response: Optional[TCPSettingsResponse] = None


@dataclass
class TLSSettingsConfig:
    allow_insecure: Optional[bool] = None
    fingerprint: Optional[str] = None
    # REALITY ONLY:
    public_key: Optional[str] = None
    server_name: Optional[str] = None
    spider_x: Optional[str] = None


@dataclass
class TLSCertificate:
    certificate_file: Optional[str] = None
    key_file: Optional[str] = None
    ocsp_stapling: Optional[int] = None


@dataclass
class TLSSettings:
    server_name: Optional[str] = None
    min_version: Optional[str] = None
    max_version: Optional[str] = None
    cipher_suites: Optional[str] = None
    reject_unknown_sni: Optional[bool] = None
    certificates: Optional[List[TLSCertificate]] = None
    alpn: Optional[List[str]] = None
    settings: Optional[TLSSettingsConfig] = None


@dataclass
class RealitySettings:
    show: Optional[bool] = None
    xver: Optional[int] = None
    dest: Optional[str] = None
    server_names: Optional[List[str]] = None
    private_key: Optional[str] = None
    min_client: Optional[str] = None
    max_client: Optional[str] = None
    max_timediff: Optional[int] = None
    short_ids: Optional[List[str]] = None
    settings: Optional[TLSSettingsConfig] = None


@dataclass
class ExternalProxy:
    force_tls: Optional[str] = None
    dest: Optional[str] = None
    port: Optional[int] = None
    remark: Optional[str] = None


@dataclass
class Sockopt:
    accept_proxy_protocol: Optional[bool] = None
    tcp_fast_open: Optional[bool] = None
    mark: Optional[int] = None
    tproxy: Optional[str] = None


@dataclass
class InboundStreamSettings:
    network: str
    security: str
    external_proxy: Optional[List[ExternalProxy]] = None
    ws_settings: Optional[WSSettings] = None
    tls_settings: Optional[TLSSettings] = None
    tcp_settings: Optional[TCPSettings] = None
    reality_settings: Optional[RealitySettings] = None
    grpc_settings: Optional[GrpcSettings] = None
    http_settings: Optional[HTTPSettings] = None
    sockopt: Optional[Sockopt] = None


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
