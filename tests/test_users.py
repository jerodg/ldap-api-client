#!/usr/bin/env python3.8
"""LDAP API Client: Test Users
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
import time

import pytest
from os import getenv

from base_api_client import bprint, Results, tprint
from ldap_api_client import LDAPApiClient, Query


@pytest.mark.asyncio
async def test_get_all_users():
    ts = time.perf_counter()
    bprint('Test: Get All Users')

    async with LDAPApiClient(cfg=f'{getenv("CFG_HOME")}/ldap_api_client.toml') as adac:
        results = await adac.get_records(Query(search_base=adac.cfg['Defaults']['SearchBase'],
                                               search_filter='(objectClass=person)'))
        # print(results)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_all_users_filtered():
    ts = time.perf_counter()
    bprint('Test: Get All Users Filtered')

    async with LDAPApiClient(cfg=f'{getenv("CFG_HOME")}/ldap_api_client.toml') as adac:
        results = await adac.get_records(Query(search_base=adac.cfg['Defaults']['SearchBase'],
                                               search_filter='(cn=t24620a)'))
        # print(results)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_check_invalid_credentials():
    ts = time.perf_counter()
    bprint('Test: Check Invalid Credentials')

    async with LDAPApiClient(cfg=f'{getenv("CFG_HOME")}/ldap_api_client.toml', autoconnect=False) as adac:
        results = await adac.check_credentials(username='t84750b', password='wrongpassword')
        # print(f'results: {results}')

        assert type(results) is Results
        assert len(results.failure) == 1
        assert not results.success

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_check_valid_credentials():
    ts = time.perf_counter()
    bprint('Test: Check Valid Credentials')

    async with LDAPApiClient(cfg=f'{getenv("CFG_HOME")}/ldap_api_client.toml', autoconnect=False) as adac:
        results = await adac.check_credentials(username=adac.cfg['Auth']['Username'], password=adac.cfg['Auth']['Password'])
        # print(f'results: {results}')

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
