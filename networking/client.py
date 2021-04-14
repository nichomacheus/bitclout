import urllib.parse

from cloudscraper import CloudScraper
from cloudscraper import create_scraper
from requests import Response
from typing import Callable

"""
Instantiate constants / re-usables
"""

API_ROOT_PATH = "https://api.bitclout.com/api/v1/"
TRANSACTION_INFO_PATH = "transaction-info"
SUCCESS_STATUS_CODE = 200
TIMEOUT = 180

"""
Base Client
"""


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

    def get_current_block(self) -> Response:
        return self._execute_request_carefully(
            self.__client.get, url=API_ROOT_PATH, timeout=TIMEOUT
        )

    def get_transaction_info(self, public_key: str, is_mempool: bool) -> Response:
        target_url = urllib.parse.urljoin(API_ROOT_PATH, TRANSACTION_INFO_PATH)
        return self._execute_request_carefully(
            self.__client.post,
            url=target_url,
            json={"PublicKeyBase58Check": public_key, "isMempool": is_mempool},
            timeout=TIMEOUT,
        )
