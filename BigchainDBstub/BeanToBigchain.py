# Using the Bigchain Python API to provision TagTok's with BigchainDB's blockchain

from bigchaindb import Bigchain
import binascii
import hashlib
import sha3
import base58
from bigchaindb import crypto

# create a BigchainDB instance "b"
b = Bigchain()

# The following HEX string represents an ECC public key belonging to the secret key
# of a crypto tag inside a product
# '6ABCA66658E30D4808F6DDABD900723BFB3DE8BF77F86B3DC84584D7F2039B1FED0
# 4CFE79C39390D7A6240B7713FFF1891AB687E62ADAE8460FCF040D02105D2'

# Define the product public key derived from a Riddle&Code crypto tag
tag_pubkey = b'6ABCA66658E30D4808F6DDABD900723BFB3DE8BF77F86B3DC84584D7F2039B1FED04CFE79C39390D7A6240B7713FFF1891AB687E62ADAE8460FCF040D02105D2'
# Translate public key from tag into a bicgchaindb compliant address
# Results in '5GjT173hXbwm9R5x2Sk4y6NgeqCCA2JrwdyZdzKPvC6a'
prdct_pubkey = binascii.hexlify(tag_pubkey)
prdct_pubkey = hashlib.sha3_256(prdct_pubkey).digest()
prdct_pubkey = base58.b58encode(prdct_pubkey)


# Define a private and public key representing the producer
prdusr_privkey, prdusr_pubkey = crypto.generate_key_pair()

# Define a private and public key representing a future product owner
ownr_privkey, ownr_pubkey = crypto.generate_key_pair()

# Create a multisig transaction including the three pre-produced public keys signed with
# master key of the BigchainDB instance holder
tx_msig = b.create_transaction(b.me, [prdct_pubkey, prdusr_pubkey, ownr_pubkey], None, 'CREATE')

# Sign the multisig
tx_msig_signed = b.sign_transaction(tx_msig, b.me_private)

# Write the signed multig transaction to the federated BigchainDB
# Results in {'deleted': 0, 'unchanged': 0, 'errors': 0, 'skipped': 0, 'inserted': 1, 'replaced': 0}
b.write_transaction(tx_msig_signed)

# Check the uploaded multisig transaction
tx_msig_retrieved = b.get_transaction(tx_msig_signed['id'])

"""

Has to result in JSON string like :

{'transaction': {'timestamp': '1481491650', 'operation': 'CREATE', 'data': {'uuid': 'f75d216a-1966-4cef-8de4-71ce57563aae', 'payload': None}, 'conditions': [{'cid': 0, 'condition': {'details': {'type_id': 2, 'subfulfillments': [{'signature': None, 'weight': 1, 'public_key': '5GjT173hXbwm9R5x2Sk4y6NgeqCCA2JrwdyZdzKPvC6a', 'type_id': 4, 'type': 'fulfillment', 'bitmask': 32}, {'signature': None, 'weight': 1, 'public_key': '3NdRQzR9x1vuPJmHcKFJzFZnErjs3NS9LVCzU5UWDrQt', 'type_id': 4, 'type': 'fulfillment', 'bitmask': 32}, {'signature': None, 'weight': 1, 'public_key': 'BSoNeHng8wc1CJXF4gwTKZYQDuL6AXKuNuisQ57VZDuo', 'type_id': 4, 'type': 'fulfillment', 'bitmask': 32}], 'type': 'fulfillment', 'threshold': 3, 'bitmask': 41}, 'uri': 'cc:2:29:Qy_H1gssES5-IxGKOJv-pNtUDEz17TmGAlJn6rDkriE:306'}, 'new_owners': ['5GjT173hXbwm9R5x2Sk4y6NgeqCCA2JrwdyZdzKPvC6a', '3NdRQzR9x1vuPJmHcKFJzFZnErjs3NS9LVCzU5UWDrQt', 'BSoNeHng8wc1CJXF4gwTKZYQDuL6AXKuNuisQ57VZDuo']}], 'fulfillments': [{'current_owners': ['5sShezEyMTWsSM7D4mHVLBMksEr3AxNdP7RB9XjgEm59'], 'input': None, 'fid': 0, 'fulfillment': 'cf:4:SFrZKwost0FPXd7KN210xFM47KHIweSunvI5Ue6LkljQADZJ9AidR9JdR_B8rN-PX_qbz5meeGTJdf8oJPxa4rR3K-_eTh6yLNYnTeBjA_i4N9cE3rukkAzZGpGV1FwK'}]}, 'id': 'bd36ee938e6b5b1cf1b54eed2537c38445eaad672d3c882288cfc01f22b56a14', 'version': 1}

"""
