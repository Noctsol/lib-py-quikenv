"""
Owner: Noctsol
Contributors: N/A
Date Created: 2021-10-24

Summary:
    Just here for messing around.

"""

# It works!
import quikenv

env = quikenv.ezload()
print(env.environment_variables)

from unittest.case import TestCase
import unittest
from StringIO import StringIO

import pkg_unit_tests

pkg_unit_tests.PkgTest()