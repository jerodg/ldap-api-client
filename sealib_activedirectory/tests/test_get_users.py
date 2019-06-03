#!/usr/scripts/env python3.7
"""Test: Get Users
   Jerod Gawne, 2019.02.01 <https://github.com/jerodg/>"""
import time

import pytest

from sealib_base.base_utils import bprint
from sealib_activedirectory.activedirectory_api import ActiveDirectoryApi


@pytest.mark.asyncio
async def test_get_users():
    ts = time.perf_counter()
    bprint('Test: Get Users')

    with ActiveDirectoryApi() as aapi:
        results = await aapi.get_users()
        # print('results:', results)

        assert type(results) is dict
        assert results['success'] is not None
        assert results['failure'][0] is None

        print('Top 5 Success Results:')
        print(*results['success'][:5], sep='\n')
        print('\nTop 5 Failure Result:')
        print(*results['failure'][:5], sep='\n')

    bprint(f'-> Completed in {time.perf_counter() - ts} seconds.')
