#!/usr/bin/env python3.7
"""ActiveDirectory API: Jerod Gawne, 2019.02.01 <https://github.com/jerodg>"""
import logging.config
from sys import argv, exc_info
from traceback import print_exception
from typing import List, Optional

from jgutils.replace import replace as rpl
from ldap3 import ALL, Connection, NTLM, Server
from os import getenv
from os.path import abspath, basename, dirname
from tenacity import after_log, retry, retry_if_exception_type, wait_random_exponential
from tqdm import tqdm

from libsea_activedirectory.activedirectory_data import ADUser
from libsea_base.base_api import ApiBase

logger = logging.getLogger(__name__)
DBG = logger.isEnabledFor(logging.DEBUG)
NFO = logger.isEnabledFor(logging.INFO)
RETRY: int = 5


# todo: remove tqdn

class ActiveDirectoryApi(ApiBase):
    ROOT: str = dirname(abspath(__file__))
    SEM: int = 100
    AD_ATTR: List[str] = ['badPwdCount', 'cn', 'department', 'displayName', 'manager', 'memberOf', 'title']
    AD_REPL: List[str] = ['CN=', 'DN=', 'OU=', 'DC=']

    def __init__(self, root: str, sem: Optional[int] = None):
        ApiBase.__init__(self, root=root or self.ROOT, sem=sem or self.SEM, parent=basename(argv[0][:-3]))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ApiBase.__exit__(self, exc_type, exc_val, exc_tb)

    @retry(retry=retry_if_exception_type(ConnectionResetError),
           wait=wait_random_exponential(max=RETRY),
           after=after_log(logger, logging.WARNING))
    async def fetch_ad(self) -> dict:
        adserver: Server = Server(getenv('AD_HOST'), use_ssl=True, get_info=ALL)
        adconn: Connection = Connection(adserver, auto_bind=True, user=getenv('AD_USER'),
                                        password=getenv('AD_PASS'),
                                        authentication=NTLM)

        entries = adconn.extend.standard.paged_search('dc=dm0001,dc=info53,dc=com', '(objectClass=person)',
                                                      attributes=self.AD_ATTR, paged_size=25)
        try:
            adcnt = self.cache['ad_count']
        except KeyError:
            adcnt = 100000  # Base was 97400; this is an estimate

        ad_users: list = []

        for entry in tqdm(entries, desc='Processing AD', unit=' records', total=adcnt):
            e = entry['attributes']
            ident = e['cn']
            name = e['displayName'] if e['displayName'] else ''
            memberof = set(rpl(''.join(e['memberOf']), self.AD_REPL, '').split(','))
            department = [d.lower() for d in e['department']] if type(e['department']) is list else e['department']
            manager = rpl(''.join(e['manager']), self.AD_REPL, '').split(',')[0].lower()
            title = e['title']

            ad_users.append(ADUser(ident=ident,
                                   name=name,
                                   memberof=memberof,
                                   department=department,
                                   manager=manager,
                                   title=title).dict())

        return await self.process_results(results=ad_users)


if __name__ == '__main__':
    try:
        print(__doc__)
    except Exception as excp:
        logger.exception(print_exception(*exc_info()))
