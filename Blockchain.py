import copy
from Block import Block
import datetime


class Blockchain:
    def __init__(self):  # initialize when creating a chain
        self.blocks = [self.get_genesis_block()]
        self.difficulty = 4

    @staticmethod
    def get_genesis_block():
        return Block(index=0,
                     timestamp=datetime.datetime.now().isoformat(),
                     data='Genesis',
                     previous_hash='arbitrary', nonce=0, merkle_tree='0')

    def get_latest_block(self):
        return self.blocks[len(self.blocks) - 1]

    def add_block(self, data, merkle_tree):
        new_block = Block(index=len(self.blocks),
                          timestamp=datetime.datetime.now().isoformat(),
                          data=data,
                          previous_hash=self.get_latest_block().hash, nonce=0, merkle_tree=merkle_tree)
        new_block.mine_block(difficulty=self.difficulty)
        self.blocks.append(new_block)
        return len(self.blocks) - 1

    def get_chain_size(self):  # exclude genesis block
        return len(self.blocks) - 1

    def verify(self, verbose=True):
        flag = True
        for i in range(1, len(self.blocks)):
            if self.blocks[i].index != i:
                flag = False
                if verbose:
                    print(f'Wrong block index at block {i}.')
            if self.blocks[i - 1].hash != self.blocks[i].previous_hash:
                flag = False
                if verbose:
                    print(f'Wrong previous hash at block {i}.')
            if self.blocks[i].hash != self.blocks[i].calculate_hash():
                flag = False
                if verbose:
                    print(f'Wrong hash at block {i}.')
            if self.blocks[i - 1].timestamp >= self.blocks[i].timestamp:
                flag = False
                if verbose:
                    print(f'Backdating at block {i}.')
        return flag

    def fork(self, head='latest'):
        if head in ['latest', 'whole', 'all']:
            return copy.deepcopy(self)  # deepcopy since they are mutable
        else:
            c = copy.deepcopy(self)
            c.blocks = c.blocks[0:head + 1]
            return c

    def get_root(self, chain_2):
        min_chain_size = min(self.get_chain_size(), chain_2.get_chain_size())
        for i in range(1, min_chain_size + 1):
            if self.blocks[i] != chain_2.blocks[i]:
                return self.fork(i - 1)
        return self.fork(min_chain_size)
