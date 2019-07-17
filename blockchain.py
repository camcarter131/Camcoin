import pdb
from functools import reduce
import hashlib as hl
import json
import pickle

from hash_util import hash_block
from block import Block
from transaction import Transaction
from verification import Verification

MINING_REWARD = 10

# Initializing out (empty) blockchain list
blockchain = []
# Unhandled transactions
open_transactions = []
# We are the owner of this blockchain node
owner = "Cam"


def load_data():
    global blockchain
    global open_transactions
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
            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])
            updated_open_transactions = []
            for tx in open_transactions:
                updated_tx = Transaction(
                    tx["sender"], tx["recipient"], tx["amount"])
                updated_open_transactions.append(updated_tx)
            open_transactions = updated_open_transactions
    except (IOError, IndexError):
        print("File not found!")
        # Our starting block for the blockchain
        genesis_block = Block(0, "", [], 100)
        # Initializing out (empty) blockchain list
        blockchain = [genesis_block]
        # Unhandled transactions
        open_transactions = []


load_data()


def save_data():
    try:
        with open("blockchain.txt", mode="w") as f:
            saveable_chain = [block.__dict__ for block in
                              [Block(block_el.index, block_el.previous_hash,
                                     [tx.__dict__ for tx in block_el.transactions], block_el.proof) for block_el in blockchain]]
            f.write(json.dumps(saveable_chain))
            f.write('\n')
            saveable_tx = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(saveable_tx))
            # save_data = {
            #     "chain": blockchain,
            #     "ot": open_transactions
            # }
            # f.write(pickle.dumps(save_data ))
    except IOError:
        print("Saving failed!")


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    verifier = Verification()
    while not verifier.valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant]
                 for block in blockchain]
    open_tx_sender = [tx.amount
                      for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)

    tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant]
                    for block in blockchain]
    open_tx_recipient = [tx.amount
                         for tx in open_transactions if tx.recipient == participant]
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


def get_last_blockchain_value():
    """Returns the last value of the current blockchain"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
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
    if verifier.verify_transaction(transaction, get_balance):
        open_transactions.append(transaction)
        save_data()
        return True
    return False


def mine_block():
    """Create a new block and add open transactions to it"""
    # Fetch the current last block of the blockchain
    last_block = blockchain[-1]
    # Hash the last block
    hashed_block = hash_block(last_block)
    # print(hashed_block)
    # Create proof of work
    proof = proof_of_work()
    # Miners are rewarded
    # reward_transaction = {
    #     "sender": "MINING",
    #     "recipient": owner,
    #     "amount": MINING_REWARD
    # }

    reward_transaction = Transaction("MINING", owner, MINING_REWARD)
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    blockchain.append(block)
    return True


def get_transaction_value():
    """Returns the input of the user (a new transaction amount) as a float"""
    recipient = input("Enter the recipient: ")
    amount = float(input("Enter your transaction amount: "))
    return recipient, amount


def get_user_choice():
    user_input = input("Your choice: ")
    return user_input


def print_blockchain():
    for block in blockchain:
        print('Outputting block')
        print(block)
    else:
        print("-" * 20)


waiting_for_input = True
verifier = Verification()

while waiting_for_input:
    print("Please choose")
    print("1: Add a new transaction value")
    print("2: Mine a new block")
    print("3: Output the blockchain blocks")
    print("4: Check transaction validity")
    print("q: Quit")
    print("-" * 20)
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print("Transaction added")
        else:
            print("Transaction failed!")

    elif user_choice == "2":
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == "3":
        print_blockchain()
    elif user_choice == "4":
        if verifier.verify_transactions(open_transactions, get_balance):
            print("All transactions are valid")
        else:
            print("There are invalid transactions")
    elif user_choice == "q":
        waiting_for_input = False
    else:
        print("Invalid input")
    if not verifier.verify_chain(blockchain):
        print_blockchain()
        print("Invalid blockchain!")
        break
    print("Balance of {}: {:6.2f}".format(owner, get_balance(owner)))
else:
    print("User left!")

print('Done')
