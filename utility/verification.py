from utility.hash_util import hash_block, hash_string_256
from wallet import Wallet

class Verification:
    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        """Validate a proof of work number and see if it solves the puzzle algorithm

        Arguments:
            :transactions: The transactions for the last block for which the proof is being validated
            :last_hash: The previous block's hash which will be stored in the current block
            :proof: The proof number we're testing
        """
        guess = (str([tx.to_ordered_dict() for tx in transactions]) +
                str(last_hash) + str(proof)).encode()
        # print(guess)
        guess_hash = hash_string_256(guess)
        # print(guess_hash)
        return guess_hash[0:2] == "00"

    @classmethod
    def verify_chain(cls, blockchain):
        """Verify the current blockchain, return True if valid, False otherwise"""
        for i, block in enumerate(blockchain):
            if i == 0:
                continue
            if block.previous_hash != hash_block(blockchain[i-1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print("Proof of work is invalid")
                return False
        return True

    @staticmethod
    def verify_transaction(transaction, get_balance, check_funds=True):
        if check_funds:
            sender_balance = get_balance(sender=transaction.sender)
            return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction)
        else:
            return Wallet.verify_transaction(transaction)

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        """Verify that all transactions that are in open_transactions are valid"""
        return all([cls.verify_transaction(tx, get_balance, False) for tx in open_transactions])
