blockchain = []


def get_last_blockchain_value():
    """Returns the last value of the current blockchain"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(amount, last_transaction):
    """Adds the amount plus the last blockchain block to the blockchain

    Arguments:
        :amount: the amount to be added
        :last_transaction: the last blockchain transation, default [1]
    """
    if last_transaction == None:
        last_transaction = [1]
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
    else:
        print("-" * 20)


def verify_chain():
    # block_index = 0
    for i in range(len(blockchain)):
        if i == 0:
            continue
        elif blockchain[i][0] != blockchain[i-1]:
            return False

    return True


waiting_for_input = True

while waiting_for_input:
    print("Please choose")
    print("1: Add a new transaction value")
    print("2: Output the blockchain block")
    print("h: Manipulate the chain")
    print("q: Quit")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_amount = get_transaction_value()
        add_transaction(tx_amount, get_last_blockchain_value())
    elif user_choice == "2":
        print_blockchain()
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == "q":
        waiting_for_input = False
    else:
        print("Invalid input")
    if not verify_chain():
        print_blockchain()
        print("Invalid blockchain!")
        break
else:
    print("User left!")

print('Done')
