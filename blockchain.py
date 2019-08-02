import pdb
from functools import reduce
import hashlib as hl
import json
import pickle
import requests

from utility.hash_util import hash_block
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet

# Setting our mining reward
MINING_REWARD = 10


class Blockchain:
    def __init__(self, host_node_id):
        # Our starting block for the blockchain
        genesis_block = Block(0, "", [], 100)
        # Initializing out (empty) blockchain list
        self.chain = [genesis_block]
        # Unhandled transactions
        self.__open_transactions = []
        # Read in blockchain from text file
        self.host_node = host_node_id
        self.__peer_nodes = set()
        self.load_data()

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_transactions(self):
        return self.__open_transactions[:]

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
                    converted_tx = [Transaction(tx["sender"], tx["recipient"], tx["signature"], tx["amount"])
                                    for tx in block["transactions"]]
                    updated_block = Block(
                        block["index"], block["previous_hash"], converted_tx, block["proof"])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1][:-1])
                updated_open_transactions = []
                for tx in open_transactions:
                    updated_tx = Transaction(
                        tx["sender"], tx["recipient"], tx["signature"], tx["amount"])
                    updated_open_transactions.append(updated_tx)
                self.__open_transactions = updated_open_transactions
                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)
        except (IOError, IndexError):
            print("Handled exception")

    def save_data(self):
        try:
            with open("blockchain.txt", mode="w") as f:
                saveable_chain = [block.__dict__ for block in
                                  [Block(block_el.index, block_el.previous_hash,
                                         [tx.__dict__ for tx in block_el.transactions], block_el.proof) for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write("\n")
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                f.write("\n")
                f.write(json.dumps(list(self.__peer_nodes)))
                # save_data = {
                #     "chain": blockchain,
                #     "ot": open_transactions
                # }
                # f.write(pickle.dumps(save_data ))
        except IOError:
            print("Saving failed!")

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self):
        participant = self.host_node

        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant]
                     for block in self.__chain]
        open_tx_sender = [tx.amount
                          for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)

        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant]
                        for block in self.__chain]
        open_tx_recipient = [tx.amount
                             for tx in self.__open_transactions if tx.recipient == participant]
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
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, recipient, sender, signature, amount=1.0):
        """Adds the amount plus the last blockchain block to the blockchain

        Arguments:
            :sender: sender of the coins
            :recipient: recipient of the coins
            :amount: the amount of coins sent with the transaction (default 1.0)
        """
        if self.host_node == None:
            return False

        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            for node in self.__peer_nodes:
                url = "http://{}/broadcast-transaction".format(node)
                try:
                    response = requests.post(url, json={"sender": sender, "recipient": recipient, "amount": amount, "signature": signature})
                    if response.status_code == 400 or response.status_code == 500:
                        print("Transaction declined. Needs resolving.")
                        return False
                except requests.exceptions.ConnectionError:
                    continue


            return True
        return False

    def mine_block(self):
        """Create a new block and add open transactions to it"""
        # First check if the wallet has been loaded
        if self.host_node == None:
            return None
        # Fetch the current last block of the blockchain
        last_block = self.__chain[-1]
        # Hash the last block
        hashed_block = hash_block(last_block)
        # print(hashed_block)
        # Create proof of work
        proof = self.proof_of_work()
        # Miners are rewarded
        reward_transaction = Transaction(
            "MINING", self.host_node, "", MINING_REWARD)
        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block,
                      copied_transactions, proof)

        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return block

    def add_peer_node(self, node):
        """Adds a new node to the peer node set
        
        Arguments:
            :node: The node url to be added
        """
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        """Removes a node from the peer node set if it exists, otherwise does nothing
        
        Arguments:
            :node: The node url to be removed
        """
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        """Gets a set of all peer nodes"""
        return list(self.__peer_nodes)

