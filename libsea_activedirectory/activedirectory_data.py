#!/usr/bin/env python3.7
"""Active Directory API Data: Jerod Gawne 2019.02.20 <https://github.com/jerodg>"""
import logging
from dataclasses import dataclass
from sys import exc_info
from traceback import print_exception
from typing import Any

from os.path import basename

logger = logging.getLogger(basename(__file__)[:-3])
DBG = logger.isEnabledFor(logging.DEBUG)
NFO = logger.isEnabledFor(logging.INFO)



@dataclass()
class User:
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

    def dict(self):
        return dict(sorted({k: v for k, v in self.__dict__.items() if v is not None}.items()))


@dataclass()
class Computer:
    name: str
    last_logon: str

    def __post_init__(self):
        pass

    def dict(self):
        return dict(sorted({k: v for k, v in self.__dict__.items() if v is not None}.items()))


if __name__ == '__main__':
    try:
        print(__doc__)
    except Exception as excp:
        logging.exception(print_exception(*exc_info()))
