blockchain = []


def get_last_blockchain_value():
    """Returns the last value of the current blockchain"""
    return blockchain[-1]


def add_value(amount, last_transaction=[1]):
    """Adds the amount plus the last blockchain block to the blockchain

    Arguments:
        :amount: the amount to be added
        :last_transaction: the last blockchain transation, default [1]
    """
    blockchain.append([last_transaction, amount])


def get_user_input():
    """Returns the input of the user (a new transaction amount) as a float"""
    return float(input("Enter your transaction amount: "))


add_value(get_user_input())
add_value(last_transaction=get_last_blockchain_value(),
          amount=get_user_input())
add_value(get_user_input(), get_last_blockchain_value())
print(blockchain)
