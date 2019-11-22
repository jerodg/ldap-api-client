#!/usr/bin/env python3.8
"""LDAP API Client: Models.Query
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

import logging
from dataclasses import dataclass
from typing import List, Optional, Union

from ldap3 import ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES

from base_api_client.models import Record

logger = logging.getLogger(__name__)


def attributes():
    return [ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES]


@dataclass
class Query(Record):
    """
    search_base (Optional[str]): dc=<sub-domain>,dc=<domain>,dc=<extension>
        e.g. 'dc=ldap001,dc=mydomain,dc=com'
        Can be any or None
    search_filter_types (Optional[str]):
        cn -> Common Name (typically User Name)
        sn -> Surname (Last Name)
        givenName -> First Name
        c -> Country
        l -> Locality (City)
        st -> State
        title
        postalCode
    """
    search_base: Optional[str] = None
    search_filter: Optional[str] = None
    search_scope: Optional[str] = 'SUBTREE'  # BASE|LEVEL|SUBTREE
    attributes: Optional[Union[List[str], str]] = '*'  # * | 1.1 | +
    paged_size: Optional[int] = 1000


@dataclass
class ComputerQuery(Query):
    search_filter: Optional[str] = '(objectClass=computer)'


@dataclass
class UserQuery(Query):
    search_filter: Optional[str] = '(objectClass=person)'
