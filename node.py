from flask import Flask, jsonify, request
from flask_cors import CORS
from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(app)

###############################-----UI-----#####################################


@app.route("/", methods=["GET"])
def get_ui():
    return "Works"

###############################-----WALLET-----#####################################


@app.route("/wallet", methods=["POST"])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            "public_key": wallet.public_key,
            "private_key": wallet.private_key,
            "funds": blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "Saving keys failed"
        }
        return jsonify(response), 500


@app.route("/wallet", methods=["GET"])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            "public_key": wallet.public_key,
            "private_key": wallet.private_key,
            "funds": blockchain.get_balance()
        }
        return jsonify(response), 200
    else:
        response = {
            "message": "Loading keys failed"
        }
        return jsonify(response), 500


###############################-----MINE-----#####################################

@app.route("/mine", methods=["POST"])
def mine():
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy()
        dict_block["transactions"] = [
            tx.__dict__ for tx in dict_block["transactions"]]
        response = {
            "message": "Block added successfully",
            "block": dict_block,
            "funds": blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "Adding a block failed...",
            "wallet_set_up": wallet.public_key != None
        }
        return jsonify(response), 500

###############################-----BLOCKCHAIN-----#####################################


@app.route("/chain", methods=["GET"])
def get_chain():
    chain_snapshot = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dict_chain:
        dict_block["transactions"] = [
            tx.__dict__ for tx in dict_block["transactions"]]
    return jsonify(dict_chain), 200

###############################-----BALANCE-----#####################################


@app.route("/balance", methods=["GET"])
def get_balance():
    if blockchain.get_balance() != None:
        response = {
            "message": "Funds loaded successfully",
            "funds": blockchain.get_balance()
        }
        return jsonify(response), 200
    else:
        response = {
            "message": "Loading balance failed...",
            "wallet_set_up": wallet.public_key != None
        }
        return jsonify(response), 500

###############################-----TRANSACTIONS-----#####################################


@app.route("/transaction", methods=["POST"])
def add_transaction():
    if wallet.public_key == None:
        response = {
            "message": "No wallet set up..."
        }
        return jsonify(response), 400
    values = request.get_json()
    if not values:
        response = {
            "message": "No data found..."
        }
        return jsonify(response), 400
    required_fields = ["recipient", "amount"]
    if not all(field in values for field in required_fields):
        response = {
            "message": "Required data is missing..."
        }
        return jsonify(response), 400
    recipient = values["recipient"]
    amount = values["amount"]
    signature = wallet.sign_transaction(recipient, amount)
    success = blockchain.add_transaction(
        recipient, wallet.public_key, signature, amount)
    if success:
        response = {
            "message": "Successfully added transaction",
            "transaction": {
                "sender": wallet.public_key,
                "recipient": recipient,
                "signature": signature,
                "amount": amount
            },
            "funds": blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "Creating a transaction failed..."
        }
        return jsonify(response), 500

@app.route("/transactions", methods=["GET"])
def get_transactions():
    pass

###############################----------------------#####################################


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
