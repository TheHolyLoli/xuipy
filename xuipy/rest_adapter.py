import requests
import logging
from typing import List, Dict
from json import JSONDecodeError
from xuipy.exceptions import XuipyException
from xuipy.models import Result


class RestAdapter:
    def __init__(self, hostname: str,
                 port: int = 443, https: bool = False, path: str = "",
                 ssl_verify: bool = True, logger: logging.Logger = None):
        """
        Constructor for RestAdapter
        :param hostname: Normally, api.thecatapi.com
        :param username:
        :param password:
        :param port:
        :param https:
        :param path:
        :param ssl_verify: Normally set to True, but if having SSL/TLS cert validation issues, can turn off with False
        :param logger: (optional) If your app has a logger, pass it in here.
        """
        self._logger = logger or logging.getLogger(__name__)
        self.url = f"{'https' if https else 'http'}://{hostname}:{port}{'/' + path if path else ''}"
        self._port = port
        self._https = https
        self._path = path
        self._ssl_verify = ssl_verify
        self.session = requests.Session()
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

    def _do(self, http_method: str, endpoint: str, prefix: str = "/xui/API/inbounds", ep_params: Dict = None, data: Dict = None) -> Result:
        """
        Private method for get(), post(), delete(), etc. methods
        :param http_method: GET, POST, DELETE, etc.
        :param endpoint: URL Endpoint as a string
        :param prefix:
        :param ep_params: Dictionary of Endpoint parameters (Optional)
        :param data: Dictionary of data to pass to TheCatApi (Optional)
        :return: a Result object
        """
        prefix = prefix if prefix is not None else "/xui/API/inbounds"
        full_url = self.url + prefix + endpoint
        headers = {}
        log_line_pre = f"method={http_method}, url={full_url}, params={ep_params}"
        log_line_post = ', '.join((log_line_pre, "success={}, status_code={}, message={}"))

        # Log HTTP params and perform an HTTP request, catching and re-raising any exceptions
        try:
            self._logger.debug(msg=log_line_pre)
            response = self.session.request(method=http_method, url=full_url, verify=self._ssl_verify,
                                            headers=headers, params=ep_params, json=data)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise XuipyException("Request failed") from e

        # Deserialize JSON output to Python object, or return failed Result on exception
        try:
            data_out = None
            if response.status_code == 200 and response.text and response.text != "":
                data_out = response.json()
            # If status_code in 200-299 range, return success Result with data, otherwise raise exception
            is_success = 299 >= response.status_code >= 200  # 200 to 299 is OK
            log_line = log_line_post.format(is_success, response.status_code, response.reason)
            if is_success and data_out:
                self._logger.debug(msg=log_line)
                return Result(status_code=response.status_code, headers=response.headers,
                              success=data_out['success'], message=data_out['msg'], data=data_out['obj'])
            if not is_success:
                self._logger.error(msg=log_line)
                raise XuipyException(f"{response.status_code}: {response.reason}")
            return Result(status_code=response.status_code, headers=response.headers,
                          success=True,message=response.reason, data=None)
        except (ValueError, TypeError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise XuipyException("Bad JSON in response") from e



    def get(self, endpoint: str, ep_params: Dict = None, prefix: str = None) -> Result:
        return self._do(http_method='GET', endpoint=endpoint, ep_params=ep_params, prefix=prefix)

    def post(self, endpoint: str, ep_params: Dict = None, data: Dict = None, prefix: str = None) -> Result:
        return self._do(http_method='POST', endpoint=endpoint, ep_params=ep_params, data=data, prefix=prefix)

    def delete(self, endpoint: str, ep_params: Dict = None, data: Dict = None, prefix: str = None) -> Result:
        return self._do(http_method='DELETE', endpoint=endpoint, ep_params=ep_params, data=data, prefix=prefix)

    def fetch_data(self, url: str) -> bytes:
        # GET URL; catching, logging, and re-raising any exceptions
        http_method = 'GET'
        try:
            log_line = f"method={http_method}, url={url}"
            self._logger.debug(msg=log_line)
            response = self.session.request(method=http_method, url=url, verify=self._ssl_verify)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise XuipyException(str(e)) from e

        # If status_code in 200-299 range, return byte stream, otherwise raise exception
        is_success = 299 >= response.status_code >= 200
        log_line = f"success={is_success}, status_code={response.status_code}, message={response.reason}"
        self._logger.debug(msg=log_line)
        if not is_success:
            raise XuipyException(response.reason)
        return response.content
