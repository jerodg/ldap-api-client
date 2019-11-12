#!/usr/bin/env python3.8
"""LDAP API Client
Copyright © 2019 Jerod Gawne <https://github.com/jerodg/>

This program is free software: you can redistribute it and/or modify
it under the terms of the Server Side Public License (SSPL) as
published by MongoDB, Inc., either version 1 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
SSPL for more details.

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

You should have received a copy of the SSPL along with this program.
If not, see <https://www.mongodb.com/licensing/server-side-public-license>."""
import logging.config
from typing import List, Union

from ldap3 import ALL, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, Connection, NTLM, Server
from tenacity import after_log, before_sleep_log, retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential

from base_api_client import BaseApiClient, Results

logger = logging.getLogger(__name__)
DBG = logger.isEnabledFor(logging.DEBUG)
NFO = logger.isEnabledFor(logging.INFO)


class ActiveDirectoryApiClient(BaseApiClient):
    AD_REPL: List[str] = ['CN=', 'DN=', 'OU=', 'DC=']

    def __init__(self, cfg: Union[str, dict]):
        BaseApiClient.__init__(self, cfg=cfg)
        self.adserver: Server = Server(self.cfg['URI']['Base'], get_info=ALL)
        self.connection: Connection = Connection(self.adserver, auto_bind=True, user=self.cfg['Auth']['Username'],
                                                 password=self.cfg['Auth']['Password'],
                                                 authentication=NTLM)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.connection.unbind()  # Close Connection
        await BaseApiClient.__aexit__(self, exc_type, exc_val, exc_tb)

    @retry(retry=retry_if_exception_type(ConnectionResetError),
           wait=wait_random_exponential(multiplier=1.25, min=3, max=60),
           after=after_log(logger, logging.DEBUG),
           stop=stop_after_attempt(7),
           before_sleep=before_sleep_log(logger, logging.DEBUG))
    async def get_users(self) -> Results:
        entries = self.connection.extend.standard.paged_search('dc=dm0001,dc=info53,dc=com', '(objectClass=person)',
                                                               attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES],
                                                               paged_size=1000)

        return Results(data=entries, success=[e['attributes'] for e in entries])

    @retry(retry=retry_if_exception_type(ConnectionResetError),
           wait=wait_random_exponential(multiplier=1.25, min=3, max=60),
           after=after_log(logger, logging.DEBUG),
           stop=stop_after_attempt(7),
           before_sleep=before_sleep_log(logger, logging.DEBUG))
    async def get_computers(self) -> Results:
        entries = self.connection.extend.standard.paged_search('dc=dm0001,dc=info53,dc=com', '(objectClass=computer)',
                                                               attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES],
                                                               paged_size=1000)

        return Results(data=entries, success=[e['attributes'] for e in entries])


if __name__ == '__main__':
    print(__doc__)
