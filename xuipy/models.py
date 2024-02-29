from typing import List, Optional, Union, Dict, Any
from requests import Response
from requests.structures import CaseInsensitiveDict
from pydantic import BaseModel, ConfigDict


class Result(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    status_code: int
    headers: Optional[CaseInsensitiveDict]
    response: Optional[Response]
    success: bool
    message: Optional[str]
    data: Optional[Union[list, dict]]



class Client(BaseModel):
    email: str
    enable: bool
    id: Optional[str] = None
    password: Optional[str] = None
    flow: Optional[str] = None
    total_gb: Optional[int] = None
    limit_ip: Optional[int] = None
    sub_id: Optional[str] = None
    tg_id: Optional[str] = None
    expiry_time: Optional[int] = None
    reset: Optional[int] = None



class ClientStat(BaseModel):
    id: int
    inbound_id: int
    enable: bool
    email: str
    up: int
    down: int
    total: int
    reset: int
    expiry_time: Optional[int] = None



class InboundSettings(BaseModel):
    clients: List[Client]



class InboundSniffing(BaseModel):
    enabled: bool
    dest_override: List[str]



class TransmissionTypeHeader(BaseModel):
    type: Optional[str] = None



class WSSettings(BaseModel):
    path: str
    headers: Optional[Dict] = None
    accept_proxy_protocol: Optional[bool] = None



class GrpcSettings(BaseModel):
    service_name: Optional[str] = None
    multi_mode: Optional[bool] = None



class HTTPSettings(BaseModel):
    path: Optional[str] = None
    host: Optional[List[str]] = None



class QuicSettings(BaseModel):
    security: Optional[str] = None
    key: Optional[str] = None
    header: Optional[TransmissionTypeHeader] = None



class KcpSettings(BaseModel):
    mtu: Optional[int] = None
    tti: Optional[int] = None
    uplink_capacity: Optional[int] = None
    downlink_capacity: Optional[int] = None
    congestion: Optional[bool] = None
    read_buffer_size: Optional[int] = None
    write_buffer_size: Optional[int] = None
    header: Optional[TransmissionTypeHeader] = None
    seed: Optional[str] = None



class TCPSettings(BaseModel):
    accept_proxy_protocol: Optional[bool] = None
    header: Optional[TransmissionTypeHeader] = None



class TCPSettingsRequest(BaseModel):
    version: Optional[str] = None
    method: Optional[str] = None
    path: Optional[List[str]] = None
    headers: Optional[dict] = None



class TCPSettingsResponse(BaseModel):
    status: Optional[int] = None
    version: Optional[str] = None
    reason: Optional[str] = None
    headers: Optional[dict] = None



class TCPSettingsHeader(BaseModel):
    type: Optional[str] = None
    request: Optional[TCPSettingsRequest] = None
    response: Optional[TCPSettingsResponse] = None



class TLSSettingsConfig(BaseModel):
    allow_insecure: Optional[bool] = None
    fingerprint: Optional[str] = None
    # REALITY ONLY:
    public_key: Optional[str] = None
    server_name: Optional[str] = None
    spider_x: Optional[str] = None



class TLSCertificate(BaseModel):
    certificate_file: Optional[str] = None
    key_file: Optional[str] = None
    ocsp_stapling: Optional[int] = None



class TLSSettings(BaseModel):
    server_name: Optional[str] = None
    min_version: Optional[str] = None
    max_version: Optional[str] = None
    cipher_suites: Optional[str] = None
    reject_unknown_sni: Optional[bool] = None
    certificates: Optional[List[TLSCertificate]] = None
    alpn: Optional[List[str]] = None
    settings: Optional[TLSSettingsConfig] = None



class RealitySettings(BaseModel):
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



class ExternalProxy(BaseModel):
    force_tls: Optional[str] = None
    dest: Optional[str] = None
    port: Optional[int] = None
    remark: Optional[str] = None



class Sockopt(BaseModel):
    accept_proxy_protocol: Optional[bool] = None
    tcp_fast_open: Optional[bool] = None
    mark: Optional[int] = None
    tproxy: Optional[str] = None



class InboundStreamSettings(BaseModel):
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



class Inbound(BaseModel):
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
