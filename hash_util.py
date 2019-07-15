import hashlib as hl
import json


def hash_string_256(string):
    return hl.sha256(string).hexdigest()
 

def hash_block(block):
    """Hashes a block and returns it as a string

    Arguments:
        :block: The block to be hashed.
    """
    return hash_string_256(json.dumps(block, sort_keys=True).encode())