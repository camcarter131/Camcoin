from verification import Verification


class Node:
    def __init__(self):
        self.blockchain = []

    def get_user_choice(self):
        user_input = input("Your choice: ")
        return user_input

    def get_transaction_value(self):
        """Returns the input of the user (a new transaction amount) as a float"""
        recipient = input("Enter the recipient: ")
        amount = float(input("Enter your transaction amount: "))
        return recipient, amount

    def print_blockchain(self):
        for block in self.blockchain:
            print('Outputting block')
            print(block)
        else:
            print("-" * 20)

    def listen_for_input(self):
        """A while loop for the user input interface"""
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
            user_choice = self.get_user_choice()
            if user_choice == "1":
                tx_data = self.get_transaction_value()
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
                self.print_blockchain()
            elif user_choice == "4":
                if verifier.verify_transactions(open_transactions, get_balance):
                    print("All transactions are valid")
                else:
                    print("There are invalid transactions")
            elif user_choice == "q":
                waiting_for_input = False
            else:
                print("Invalid input")
            if not verifier.verify_chain(self.blockchain):
                self.print_blockchain()
                print("Invalid blockchain!")
                break
            print("Balance of {}: {:6.2f}".format(owner, get_balance(owner)))
        else:
            print("User left!")

        print('Done')
