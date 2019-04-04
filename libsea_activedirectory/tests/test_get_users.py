#!/usr/bin/env python3.7
"""Test ActiveDirectory API: Jerod Gawne, 2019.02.01 <https://github.com/jerodg/>"""
import asyncio
import logging
import sys
import time
import traceback

from os.path import (abspath, dirname)

from libsea_activedirectory.activedirectory_api import ActiveDirectoryApi

logger = logging.getLogger(__name__)
DBG = logger.isEnabledFor(logging.DEBUG)
NFO = logger.isEnabledFor(logging.INFO)


def format_banner(message) -> str:
    msg_len = len(message)
    if msg_len >= 80:
        return message

    ast = (80 - msg_len) // 2
    ast = '*' * ast
    msg = f'\n{ast}{message}{ast}\n'

    return msg


ROOT: str = dirname(abspath(__file__))
SEM: int = 100

with ActiveDirectoryApi(ROOT, SEM) as adapi:
    def test_get_users():
        ts = time.perf_counter()
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(adapi.get_users())
        # print('\nresults: ', results)  # debug

        assert type(results) is dict
        assert results['success'] is not None
        assert results['failure'][0] is None

        te = time.perf_counter()
        print(format_banner(f'Test: Get Users'))
        print(f'Top 5 Success Results: {len(results["success"])}')
        print(*results['success'][:5], sep='\n')
        print(f'\nTop 5 Failure Results: {len(results["failure"])}')
        print(*results['failure'][:5], sep='\n')
        print(f'Processed {len(results["success"])} records in {round((te - ts) / 60, 2)} minutes.')


if __name__ == '__main__':
    try:
        print(__doc__)
    except Exception as excp:
        logger.exception(traceback.print_exception(*sys.exc_info()))
