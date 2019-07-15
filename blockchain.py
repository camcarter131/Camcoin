import pdb
from functools import reduce
import hashlib as hl
from collections import OrderedDict
import json

from hash_util import hash_block, hash_string_256

MINING_REWARD = 10

genesis_block = {
    "previous_hash": "",
    "index": 0,
    "transactions": [],
    "proof": 100
}
blockchain = [genesis_block]
open_transactions = []
owner = "Cam"
participants = {owner}


def load_data():
    with open("blockchain.txt", mode="r") as f:
        file_content = f.readlines()
        global blockchain
        global open_transactions
        blockchain = json.loads(file_content[0][:-1])
        updated_blockchain = []
        for block in blockchain:
            updated_block = {
                "previous_hash": block["previous_hash"],
                "index": block["index"],
                "proof": block["proof"],
                "transactions": [OrderedDict(
                    [("sender", tx["sender"]), ("recipient", tx["recipient"]), ("amount", tx["amount"])])
                    for tx in block["transactions"]]
            }
            updated_blockchain.append(updated_block)
        blockchain = updated_blockchain
        open_transactions = json.loads(file_content[1])
        updated_open_transactions = []
        for tx in open_transactions:
            updated_tx = OrderedDict(
                [("sender", tx["sender"]), ("recipient", tx["recipient"]), ("amount", tx["amount"])])
            updated_open_transactions.append(updated_tx)
        open_transactions = updated_open_transactions


load_data()


def save_data():
    with open("blockchain.txt", mode="w") as f:
        f.write(json.dumps(blockchain))
        f.write('\n')
        f.write(json.dumps(open_transactions))


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    print(guess)
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:2] == "00"


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    tx_sender = [[tx["amount"] for tx in block["transactions"] if tx["sender"] == participant]
                 for block in blockchain]
    open_tx_sender = [tx["amount"]
                      for tx in open_transactions if tx["sender"] == participant]
    tx_sender.append(open_tx_sender)

    tx_recipient = [[tx["amount"] for tx in block["transactions"] if tx["recipient"] == participant]
                    for block in blockchain]
    open_tx_recipient = [tx["amount"]
                         for tx in open_transactions if tx["recipient"] == participant]
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


def verify_transaction(transaction):
    sender_balance = get_balance(transaction["sender"])
    return sender_balance >= transaction["amount"]


def verify_transactions():
    """Verify that all transactions that are in open_transactions are valid"""
    return all([verify_transaction(tx) for tx in open_transactions])


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

    transaction = OrderedDict(
        [("sender", sender), ("recipient", recipient), ("amount", amount)])

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    return False


def mine_block():
    """Create a new block and add open transactions to it"""
    # Fetch the current last block of the blockchain
    last_block = blockchain[-1]
    # Hash the last block
    hashed_block = hash_block(last_block)
    print(hashed_block)
    # Create proof of work
    proof = proof_of_work()
    # Miners are rewarded
    # reward_transaction = {
    #     "sender": "MINING",
    #     "recipient": owner,
    #     "amount": MINING_REWARD
    # }

    reward_transaction = OrderedDict(
        [("sender", "MINING"), ("recipient", owner), ("amount", MINING_REWARD)])

    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    block = {
        "previous_hash": hashed_block,
        "index": len(blockchain),
        "transactions": copied_transactions,
        "proof": proof
    }
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


def verify_chain():
    """Verify the current blockchain, return True if valid, False otherwise"""
    for i, block in enumerate(blockchain):
        if i == 0:
            continue
        if block["previous_hash"] != hash_block(blockchain[i-1]):
            return False
        if not valid_proof(block["transactions"][:-1], block["previous_hash"], block["proof"]):
            print("Proof of work is invalid")
            return False
    return True


waiting_for_input = True

while waiting_for_input:
    print("Please choose")
    print("1: Add a new transaction value")
    print("2: Mine a new block")
    print("3: Output the blockchain blocks")
    print("4: Output participants")
    print("5: Check transaction validity")
    print("h: Manipulate the chain")
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
        print(participants)
    elif user_choice == "5":
        if verify_transactions():
            print("All transactions are valid")
        else:
            print("There are invalid transactions")
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = {
                "previous_hash": "",
                "index": 0,
                "transactions": [{"sender": "Toto", "recipient": "Cam", "amount": 42.1}]
            }
    elif user_choice == "q":
        waiting_for_input = False
    else:
        print("Invalid input")
    if not verify_chain():
        print_blockchain()
        print("Invalid blockchain!")
        break
    print("Balance of {}: {:6.2f}".format(owner, get_balance(owner)))
else:
    print("User left!")

print('Done')
