#!/usr/bin/env python3
# Copyright (c) 2019 Bitcoin Association
# Copyright (c) 2020* Jimmy N. Lose
# * Gregorian calendar years
# Distributed under the Open BSV software license, see the accompanying file LICENSE.

from genesis_upgrade_tests import tests
from test_framework.height_based_test_framework import SimplifiedTestFramework

if __name__ == "__main__":
    t = SimplifiedTestFramework([t() for t in tests()])
    t.main()