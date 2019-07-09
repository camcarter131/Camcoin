import pdb

genesis_block = {
    "previous_hash": "",
    "index": 0,
    "transactions": []
}
blockchain = [genesis_block]
open_transactions = []
owner = "Cam"
participants = {owner}


def hash_block(block):
    return " - ".join([str(block[key]) for key in block])


def get_balance(participant):
    amount_sent, amount_rec = 0, 0
    tx_sender = [[tx["amount"] for tx in block["transactions"] if tx["sender"] == participant]
                 for block in blockchain]
    tx_recipient = [[tx["amount"] for tx in block["transactions"] if tx["recipient"] == participant]
                    for block in blockchain]

    for tx in tx_sender:
        for each_tx in tx:
            amount_sent += each_tx

    for tx in tx_recipient:
        for each_tx in tx:
            amount_rec += each_tx

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
    transaction = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount
    }
    open_transactions.append(transaction)
    participants.add(sender)
    participants.add(recipient)


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    block = {
        "previous_hash": hashed_block,
        "index": len(blockchain),
        "transactions": open_transactions
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
    print("h: Manipulate the chain")
    print("q: Quit")
    print("-" * 20)
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == "2":
        if mine_block():
            open_transactions = []
    elif user_choice == "3":
        print_blockchain()
    elif user_choice == "4":
        print(participants)
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
    print(get_balance("Cam"))
else:
    print("User left!")

print('Done')
