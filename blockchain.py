import pdb
from functools import reduce
import hashlib as hl
import json

MINING_REWARD = 10

genesis_block = {
    "previous_hash": "",
    "index": 0,
    "transactions": []
}
blockchain = [genesis_block]
open_transactions = []
owner = "Cam"
participants = {owner}

def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hl.sha256(guess)
    print(guess_hash)
    return guess_hash[0:2] == "00"

def hash_block(block):
    """Hashes a block and returns it as a string

    Arguments:
        :block: The block to be hashed.
    """
    return hl.sha256(json.dumps(block).encode()).hexdigest()


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
    transaction = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    print(hashed_block)
    reward_transaction = {
        "sender": "MINING",
        "recipient": owner,
        "amount": MINING_REWARD
    }

    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    block = {
        "previous_hash": hashed_block,
        "index": len(blockchain),
        "transactions": copied_transactions
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
