import hashlib


class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce, merkle_tree):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.merkle_tree = merkle_tree
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        key = hashlib.sha256()
        key.update(str(self.index).encode('utf-8'))
        key.update(str(self.timestamp).encode('utf-8'))
        key.update(str(self.data).encode('utf-8'))
        key.update(str(self.previous_hash).encode('utf-8'))
        key.update(str(self.nonce).encode('utf-8'))
        return key.hexdigest()

    def mine_block(self, difficulty):
        while self.hash[0: difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
