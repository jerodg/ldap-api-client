#!/usr/scripts/env python3.7
"""LibSEA: ActiveDirectory API
   Jerod Gawne, 2019.02.01 <https://github.com/jerodg>"""
import logging.config
from ldap3 import ALL, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, Connection, NTLM, Server
from os import getenv
from os.path import abspath, basename, dirname
from sys import argv, exc_info
from tenacity import after_log, before_sleep_log, retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential
from traceback import print_exception
from typing import List, Optional

from sealib_base.base_api import BaseApi

logger = logging.getLogger(__name__)
DBG = logger.isEnabledFor(logging.DEBUG)
NFO = logger.isEnabledFor(logging.INFO)


class ActiveDirectoryApi(BaseApi):
    ROOT: str = dirname(abspath(__file__))
    SEM: int = 100
    AD_REPL: List[str] = ['CN=', 'DN=', 'OU=', 'DC=']

    def __init__(self):
        BaseApi.__init__(self)
        self.adserver: Server = Server(getenv('AD_HOST'), use_ssl=True, get_info=ALL)

    def __aenter__(self):
        return self

    def __aexit__(self, exc_type, exc_val, exc_tb):
        BaseApi.__exit__(self, exc_type, exc_val, exc_tb)

    @retry(retry=retry_if_exception_type(ConnectionResetError),
           wait=wait_random_exponential(multiplier=1.25, min=3, max=60),
           after=after_log(logger, logging.DEBUG),
           stop=stop_after_attempt(7),
           before_sleep=before_sleep_log(logger, logging.DEBUG))
    async def get_users(self) -> dict:
        with Connection(self.adserver, auto_bind=True, user=getenv('AD_USER'),
                        password=getenv('AD_PASS'),
                        authentication=NTLM) as adconn:
            entries = adconn.extend.standard.paged_search('dc=dm0001,dc=info53,dc=com', '(objectClass=person)',
                                                          attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES], paged_size=100)

        return await self.process_results(results=[e['attributes'] for e in entries])

    @retry(retry=retry_if_exception_type(ConnectionResetError),
           wait=wait_random_exponential(multiplier=1.25, min=3, max=60),
           after=after_log(logger, logging.DEBUG),
           stop=stop_after_attempt(7),
           before_sleep=before_sleep_log(logger, logging.DEBUG))
    async def get_computers(self) -> dict:
        with Connection(self.adserver, auto_bind=True, user=getenv('AD_USER'),
                        password=getenv('AD_PASS'),
                        authentication=NTLM) as adconn:
            entries = adconn.extend.standard.paged_search('dc=dm0001,dc=info53,dc=com', '(objectClass=computer)',
                                                          attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES], paged_size=100)

        return await self.process_results(results=[e['attributes'] for e in entries])


if __name__ == '__main__':
    try:
        print(__doc__)
    except Exception as excp:
        logger.exception(print_exception(*exc_info()))
