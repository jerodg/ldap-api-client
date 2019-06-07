#!/usr/bin/env python3.7
"""Test: Get Computers
   Jerod Gawne, 2019.04.03 <https://github.com/jerodg/>"""
import time

import pytest
from sealib_base.base_utils import bprint

from sea_lib_activedirectory.activedirectory_api import ActiveDirectoryApi


@pytest.mark.asyncio
async def test_get_computers():
    ts = time.perf_counter()
    bprint('Test: Get Computers')

    with ActiveDirectoryApi() as aapi:
        results = await aapi.get_computers()
        # print('results:', results)

        assert type(results) is dict
        assert results['success'] is not None
        assert results['failure'][0] is None

        print('Top 5 Success Results:')
        print(*results['success'][:5], sep='\n')
        print('\nTop 5 Failure Result:')
        print(*results['failure'][:5], sep='\n')

    bprint(f'-> Completed in {time.perf_counter() - ts} seconds.')
