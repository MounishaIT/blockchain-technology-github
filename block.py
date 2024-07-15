import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, transactions):
    value = str(index) + str(previous_hash) + str(timestamp) + str(transactions)
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def create_genesis_block():
    return Block(0, "0", int(time.time()), "Genesis Block", calculate_hash(0, "0", int(time.time()), "Genesis Block"))

def create_new_block(previous_block, transactions):
    index = previous_block.index + 1
    timestamp = int(time.time())
    hash = calculate_hash(index, previous_block.hash, timestamp, transactions)
    return Block(index, previous_block.hash, timestamp, transactions, hash)

def is_block_valid(new_block, previous_block):
    if previous_block.index + 1 != new_block.index:
        return False
    if previous_block.hash != new_block.previous_hash:
        return False
    if calculate_hash(new_block.index, new_block.previous_hash, new_block.timestamp, new_block.transactions) != new_block.hash:
        return False
    return True

class Blockchain:
    def __init__(self):
        self.chain = [create_genesis_block()]
        self.pending_transactions = []

    def add_block(self, transactions):
        previous_block = self.chain[-1]
        new_block = create_new_block(previous_block, transactions)
        if is_block_valid(new_block, previous_block):
            self.chain.append(new_block)
            return new_block
        else:
            return None

    def create_transaction(self, voter_id, vote):
        transaction = {'voter_id': voter_id, 'vote': vote}
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        if not self.pending_transactions:
            return None
        new_block = self.add_block(self.pending_transactions)
        self.pending_transactions = []
        return new_block

    def get_votes(self):
        votes = {}
        for block in self.chain:
            if block.index == 0:
                continue  # Skip genesis block
            for transaction in block.transactions:
                vote = transaction['vote']
                if vote in votes:
                    votes[vote] += 1
                else:
                    votes[vote] = 1
        return votes

def main():
    blockchain = Blockchain()

    # Simulate voting transactions
    blockchain.create_transaction('voter_1', 'Alice')
    blockchain.create_transaction('voter_2', 'Bob')
    blockchain.create_transaction('voter_3', 'Alice')
    blockchain.mine_pending_transactions()

    blockchain.create_transaction('voter_4', 'Alice')
    blockchain.create_transaction('voter_5', 'Bob')
    blockchain.mine_pending_transactions()

    # Print the votes
    votes = blockchain.get_votes()
    print("Votes:", votes)

if __name__ == '__main__':
    main()
