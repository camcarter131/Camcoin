import pdb
from functools import reduce
import hashlib as hl
import json
import pickle

from hash_util import hash_block
from block import Block
from transaction import Transaction
from verification import Verification

# Setting our mining reward
MINING_REWARD = 10


class Blockchain:
    def __init__(self):
        # Our starting block for the blockchain
        genesis_block = Block(0, "", [], 100)
        # Initializing out (empty) blockchain list
        self.chain = [genesis_block]
        # Unhandled transactions
        self.open_transactions = []
        # Read in blockchain from text file
        self.load_data()

    def load_data(self):
        try:
            with open("blockchain.txt", mode="r") as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()
                # blockchain = file_content["chain"]
                # open_transactions = file_content["ot"]
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx["sender"], tx["recipient"], tx["amount"])
                                    for tx in block["transactions"]]
                    updated_block = Block(
                        block["index"], block["previous_hash"], converted_tx, block["proof"])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                updated_open_transactions = []
                for tx in open_transactions:
                    updated_tx = Transaction(
                        tx["sender"], tx["recipient"], tx["amount"])
                    updated_open_transactions.append(updated_tx)
                self.open_transactions = updated_open_transactions
        except (IOError, IndexError):
            print("Handled exception")

    def save_data(self):
        try:
            with open("blockchain.txt", mode="w") as f:
                saveable_chain = [block.__dict__ for block in
                                  [Block(block_el.index, block_el.previous_hash,
                                         [tx.__dict__ for tx in block_el.transactions], block_el.proof) for block_el in self.chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.open_transactions]
                f.write(json.dumps(saveable_tx))
                # save_data = {
                #     "chain": blockchain,
                #     "ot": open_transactions
                # }
                # f.write(pickle.dumps(save_data ))
        except IOError:
            print("Saving failed!")

    def proof_of_work(self):
        last_block = self.chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        verifier = Verification()
        while not verifier.valid_proof(self.open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self, participant):
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant]
                     for block in self.chain]
        open_tx_sender = [tx.amount
                          for tx in self.open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)

        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant]
                        for block in self.chain]
        open_tx_recipient = [tx.amount
                             for tx in self.open_transactions if tx.recipient == participant]
        tx_recipient.append(open_tx_recipient)

        # Calculate total sent and received for participant
        # print(tx_sender)
        amount_sent = 0
        amount_rec = 0
        # amount_sent = reduce(lambda tx_sum, tx: tx_sum + tx[0] if len(tx) > 0 else 0, tx_sender, 0)
        # amount_rec = reduce(lambda tx_sum, tx: tx_sum + tx[0] if len(tx) > 0 else 0, tx_recipient, 0)

        for tx_list in tx_sender:
            for tx in tx_list:
                amount_sent += tx

        for tx_list in tx_recipient:
            for tx in tx_list:
                amount_rec += tx

        return amount_rec - amount_sent

    def get_last_blockchain_value(self):
        """Returns the last value of the current blockchain"""
        if len(self.chain) < 1:
            return None
        return self.chain[-1]

    def add_transaction(self, recipient, sender, amount=1.0):
        """Adds the amount plus the last blockchain block to the blockchain

        Arguments:
            :sender: sender of the coins
            :recipient: recipient of the coins
            :amount: the amount of coins sent with the transaction (default 1.0)
        """
        # transaction = {
        #     "sender": sender,
        #     "recipient": recipient,
        #     "amount": amount
        # }

        transaction = Transaction(sender, recipient, amount)

        verifier = Verification()
        if verifier.verify_transaction(transaction, self.get_balance):
            self.open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self, node):
        """Create a new block and add open transactions to it"""
        # Fetch the current last block of the blockchain
        last_block = self.chain[-1]
        # Hash the last block
        hashed_block = hash_block(last_block)
        # print(hashed_block)
        # Create proof of work
        proof = self.proof_of_work()
        # Miners are rewarded
        # reward_transaction = {
        #     "sender": "MINING",
        #     "recipient": owner,
        #     "amount": MINING_REWARD
        # }

        reward_transaction = Transaction("MINING", node, MINING_REWARD)
        copied_transactions = self.open_transactions[:]
        copied_transactions.append(reward_transaction)

        block = Block(len(self.chain), hashed_block,
                      copied_transactions, proof)
        self.chain.append(block)
        return True
