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
from typing import Union

from ldap3 import ALL, Connection, NTLM, Server
from tenacity import after_log, before_sleep_log, retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential

from base_api_client import BaseApiClient, Results
from ldap_api_client.models import ComputerQuery, Query, UserQuery

logger = logging.getLogger(__name__)
DBG = logger.isEnabledFor(logging.DEBUG)
NFO = logger.isEnabledFor(logging.INFO)


# todo: date filter for lastlogon, created, changed


class LDAPApiClient(BaseApiClient):

    def __init__(self, cfg: Union[str, dict], autoconnect=True):
        BaseApiClient.__init__(self, cfg=cfg)
        self.adserver: Server = Server(self.cfg['URI']['Base'], get_info=ALL)

        if autoconnect:
            self.connection: Connection = Connection(self.adserver,
                                                     auto_bind=True,
                                                     user=self.cfg['Auth']['Username'],
                                                     password=self.cfg['Auth']['Password'],
                                                     authentication=self.cfg['Auth']['Type'] or None)
        else:
            self.connection = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.unbind()  # Close Connection
        await BaseApiClient.__aexit__(self, exc_type, exc_val, exc_tb)

    @retry(retry=retry_if_exception_type(ConnectionResetError),
           wait=wait_random_exponential(multiplier=1.25, min=3, max=60),
           after=after_log(logger, logging.DEBUG),
           stop=stop_after_attempt(7),
           before_sleep=before_sleep_log(logger, logging.DEBUG))
    async def get_records(self, query: Union[Query, ComputerQuery, UserQuery]) -> Results:
        entries = self.connection.extend.standard.paged_search(search_base=query.search_base or self.cfg['Defaults']['SearchBase'],
                                                               search_filter=query.search_filter,
                                                               search_scope=query.search_scope,
                                                               attributes=query.attributes,
                                                               paged_size=query.paged_size)

        return Results(data=entries, success=[e['attributes'] for e in entries])

    async def check_credentials(self, username, password) -> Results:
        """

        Args:
            username (str):
            password (str):

        Returns:
            results (Results)"""
        connection: Connection = Connection(self.adserver,
                                            user=username,
                                            password=password,
                                            authentication=self.cfg['Auth']['Type'] or None)
        connection.bind()

        cr = connection.result

        if cr['description'] == 'success':
            return Results(data=connection.result, success=[cr])
        else:
            return Results(data=connection.result, failure=[cr])


if __name__ == '__main__':
    print(__doc__)
