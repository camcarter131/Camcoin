blockchain = []


def get_last_blockchain_value():
    return blockchain[-1]


def add_value(amount, last_transaction=[1]):
    blockchain.append([last_transaction, amount])

input("Enter amount to add: ")
add_value(2)
add_value(last_transaction=get_last_blockchain_value(), amount=0.7)
add_value(4, get_last_blockchain_value())
print(blockchain)
