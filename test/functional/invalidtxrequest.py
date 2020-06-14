#!/usr/bin/env python3
# Copyright (c) 2015-2016 The Bitcoin Core developers
# Copyright (c) 2019 Bitcoin Association
# Copyright (c) 2020* Jimmy N. Lose
# * Gregorian calendar years
# Distributed under the Open BSV software license, see the accompanying file LICENSE.

from test_framework.test_framework import ComparisonTestFramework
from test_framework.comptool import TestManager, TestInstance, RejectResult
from test_framework.blocktools import *
import time


'''
In this test we connect to one node over p2p, and test tx requests.
'''

# Use the ComparisonTestFramework with 1 node: only use --testbinary.


class InvalidTxRequestTest(ComparisonTestFramework):

    ''' Can either run this test as 1 node with expected answers, or two and compare them. 
        Change the "outcome" variable from each TestInstance object to only do the comparison. '''

    def set_test_params(self):
        self.num_nodes = 1
        self.setup_clean_chain = True
        self.tip = None
        self.block_time = None

    def run_test(self):
        self.test.run()

    def get_tests(self):
        if self.tip is None:
            self.tip = int("0x" + self.nodes[0].getbestblockhash(), 0)
        self.block_time = int(time.time()) + 1

        '''
        Create a new block with an anyone-can-spend coinbase
        '''
        height = 1
        block = create_block(
            self.tip, create_coinbase(height), self.block_time)
        self.block_time += 1
        block.solve()
        # Save the coinbase for later
        self.block1 = block
        self.tip = block.sha256
        height += 1
        yield TestInstance([[block, True]])

        '''
        Now we need that block to mature so we can spend the coinbase.
        '''
        test = TestInstance(sync_every_block=False)
        for i in range(100):
            block = create_block(
                self.tip, create_coinbase(height), self.block_time)
            block.solve()
            self.tip = block.sha256
            self.block_time += 1
            test.blocks_and_transactions.append([block, True])
            height += 1
        yield test

        # b'\x64' is OP_NOTIF
        # Transaction will be rejected with code 16 (REJECT_INVALID)
        tx1 = create_transaction(
            self.block1.vtx[0], 0, b'\x64', 50 * COIN - 12000)
        yield TestInstance([[tx1, RejectResult(16, b'mandatory-script-verify-flag-failed')]])

        # TODO: test further transactions...


if __name__ == '__main__':
    InvalidTxRequestTest().main()
