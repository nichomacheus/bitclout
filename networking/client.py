import urllib.parse
from enum import Enum
from functools import reduce

from cloudscraper import CloudScraper
from cloudscraper import create_scraper
from requests import Response
from typing import Callable

"""
Instantiate constants / re-usables
"""

API_ROOT_PATH = "https://api.bitclout.com"
EXPLORER_PATH = "api/v1/"
TRANSACTION_INFO_PATH = "transaction-info"
GET_PROFILES_PATH = "get-profiles"
GET_EXCHANGE_RATE_PATH = "get-exchange-rate"
SUCCESS_STATUS_CODE = 200
TIMEOUT = 180

"""
Base Client
"""

IdentifierType = Enum("IdentifierType", "USERNAME PUBLIC_KEY")


class BitCloutBaseClient:
    def __init__(self, client: CloudScraper = None):
        if not client:
            self.__client = create_scraper()
        else:
            self.__client = client

    def _execute_request_carefully(
        self, method: Callable[[], Response], **kwargs
    ) -> Response:
        try:
            response = method(**kwargs)
            if SUCCESS_STATUS_CODE == response.status_code:
                return response
            else:
                raise RuntimeError(
                    "Received a non-zero response code: {} due to: {}".format(
                        response.status_code, response.reason
                    )
                )
        except Exception as e:
            raise RuntimeError("Error getting current block.") from e

    def get_request(self, url: str) -> Response:
        return self._execute_request_carefully(
            self.__client.get, url=url, timeout=TIMEOUT
        )

    def post_request(self, url: str, payload: dict) -> Response:
        return self._execute_request_carefully(
            self.__client.post,
            url=url,
            json=payload,
            timeout=TIMEOUT,
        )

    def get_current_block(self) -> Response:
        target_url = urllib.parse.urljoin(API_ROOT_PATH, EXPLORER_PATH)
        return self.get_request(target_url)

    def get_exchange_rate(self) -> Response:
        target_url = urllib.parse.urljoin(API_ROOT_PATH, GET_EXCHANGE_RATE_PATH)
        return self.get_request(target_url)

    def get_transaction_info(self, public_key: str, is_mempool: bool) -> Response:
        target_url = reduce(
            urllib.parse.urljoin, [API_ROOT_PATH, EXPLORER_PATH, TRANSACTION_INFO_PATH]
        )
        payload = {"PublicKeyBase58Check": public_key, "isMempool": is_mempool}
        return self.post_request(target_url, payload)

    def get_profiles(
        self, tag: str = None, tag_type: IdentifierType = None
    ) -> Response:
        payload = {}
        if not tag:
            pass
        elif tag_type == IdentifierType.PUBLIC_KEY:
            payload["PublicKeyBase58Check"] = tag
        elif tag_type == IdentifierType.USERNAME:
            payload["Username"] = tag
        target_url = reduce(urllib.parse.urljoin, [API_ROOT_PATH, GET_PROFILES_PATH])
        return self.post_request(target_url, payload)
