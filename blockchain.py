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


def get_transaction_value():
    """Returns the input of the user (a new transaction amount) as a float"""
    return float(input("Enter your transaction amount: "))


def get_user_choice():
    user_input = input("Your choice: ")
    return user_input


def print_blockchain():
    for block in blockchain:
        print('Outputting block')
        print(block)


tx_amount = get_transaction_value()
add_value(tx_amount)

while True:
    print("Please choose")
    print("1: Add a new transaction value")
    print("2: Output the blockchain block")
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_amount = get_transaction_value()
        add_value(tx_amount, get_last_blockchain_value())
    elif user_choice == '2':
        print_blockchain()


print('Done')
