#!/usr/scripts/env python3.7
"""LibSEA Base Tests Init: Jerod Gawne, 2019.03.14 <https://github.com/jerodg/>"""
import logging
import sys
import traceback

from sealib_activedirectory.tests import test_get_computers, test_get_users

___all___ = ['test_get_users', 'test_get_computers']

logger = logging.getLogger(__name__)
DBG = logger.isEnabledFor(logging.DEBUG)
NFO = logger.isEnabledFor(logging.INFO)

if __name__ == '__main__':
    try:
        print(__doc__)
    except Exception as excp:
        logger.exception(traceback.print_exception(*sys.exc_info()))
