#!/usr/bin/env python3.7
"""ActiveDirectory API: Jerod Gawne, 2019.02.01 <https://github.com/jerodg>"""
import logging.config
from sys import argv, exc_info
from traceback import print_exception
from typing import List, Optional

from ldap3 import ALL, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, Connection, NTLM, Server
from os import getenv
from os.path import abspath, basename, dirname
from tenacity import after_log, before_sleep_log, retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential

from libsea_base.base_api import ApiBase

logger = logging.getLogger(__name__)
DBG = logger.isEnabledFor(logging.DEBUG)
NFO = logger.isEnabledFor(logging.INFO)


class ActiveDirectoryApi(ApiBase):
    ROOT: str = dirname(abspath(__file__))
    SEM: int = 100
    USER_ATTR: List[str] = ['badPwdCount', 'cn', 'department', 'displayName', 'manager', 'memberOf', 'title']
    COMPUTER_ATTR: List[str] = ['Name', 'lastLogonTimestamp']
    AD_REPL: List[str] = ['CN=', 'DN=', 'OU=', 'DC=']
    DOMAINS: List[str] = ['dm0001', 'dm0007']

    def __init__(self, root: str, sem: Optional[int] = None):
        ApiBase.__init__(self, root=root or self.ROOT, sem=sem or self.SEM, parent=basename(argv[0][:-3]))
        self.adserver: Server = Server(getenv('AD_HOST'), use_ssl=True, get_info=ALL)

    def __aenter__(self):
        return self

    def __aexit__(self, exc_type, exc_val, exc_tb):
        self.cache.sync()
        ApiBase.__exit__(self, exc_type, exc_val, exc_tb)

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

        # for entry in entries:
        #     e = entry['attributes']
        #     ident = e['cn']
        #     name = e['displayName'] if e['displayName'] else ''
        #     memberof = set(rpl(''.join(e['memberOf']), self.AD_REPL, '').split(','))
        #     department = [d.lower() for d in e['department']] if type(e['department']) is list else e['department']
        #     manager = rpl(''.join(e['manager']), self.AD_REPL, '').split(',')[0].lower()
        #     title = e['title']
        #
        #     users.append(User(ident=ident,
        #                       name=name,
        #                       memberof=memberof,
        #                       department=department,
        #                       manager=manager,
        #                       title=title).dict())

        return await self.process_results(results=[e['attributes'] for e in entries])

    @retry(retry=retry_if_exception_type(ConnectionResetError),
           wait=wait_random_exponential(multiplier=1.25, min=3, max=60),
           after=after_log(logger, logging.DEBUG),
           stop=stop_after_attempt(7),
           before_sleep=before_sleep_log(logger, logging.DEBUG))
    async def get_computers(self, last_logon: int = 7, domains: List[str] = None) -> dict:
        with Connection(self.adserver, auto_bind=True, user=getenv('AD_USER'),
                        password=getenv('AD_PASS'),
                        authentication=NTLM) as adconn:
            entries = adconn.extend.standard.paged_search('dc=dm0001,dc=info53,dc=com', '(objectClass=computer)',
                                                          attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES], paged_size=100)

            # for entry in entries:
            #     try:
            #         e = entry['attributes']
            #         last_log = e['lastLogonTimestamp']
            #     except KeyError:
            #         print('entry has no attributes:\n\t', entry)
            #         continue
            #
            #     try:
            #         if last_log >= last_week:
            #             computers.append(Computer(name=e['name'], last_logon=last_log).dict())
            #     except TypeError:
            #         continue

            return await self.process_results(results=[e['attributes'] for e in entries])


if __name__ == '__main__':
    try:
        print(__doc__)
    except Exception as excp:
        logger.exception(print_exception(*exc_info()))
