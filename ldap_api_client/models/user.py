#!/usr/bin/env python3.8
"""LDAP API Client: Models.User
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

from dataclasses import dataclass
from typing import Any

from base_api_client.models import Record


@dataclass()
class User(Record):
    ident: str
    name: str = None
    memberof: Any = None
    department: Any = None
    manager: str = None
    title: Any = None

    def __post_init__(self):
        self.ident = self.ident.lower()
        self.name = ';'.join(self.name.lower().split(','))
        self.memberof = ';'.join([m.lower() for m in self.memberof])

        if type(self.department) is list:
            self.department = ';'.join([d.lower() for d in self.department])
        else:
            self.department = self.department.lower()

        self.manager = self.manager.lower()

        if type(self.title) is list:
            self.title = ';'.join([t.lower() for t in self.title])
        else:
            self.title = self.title.lower()


if __name__ == '__main__':
    print(__doc__)
