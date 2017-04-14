# ------------------------------------------------------------------------------
# Python program using the library to create Multiple Owner transactioon.
# ------------------------------------------------------------------------------



import jwt

# Using the Bigchain Python API to provision TagTok's with BigchainDB's blockchain

from bigchaindb import Bigchain
import binascii
import hashlib
import sha3
import base58
from bigchaindb.common import crypto

# create a BigchainDB instance "b"
from bigchaindb_driver import BigchainDB
bdb = BigchainDB('http://localhost:9984')



# The following HEX string represents an ECC public key belonging to the secret key
# of a crypto tag inside a product
# '6ABCA66658E30D4808F6DDABD900723BFB3DE8BF77F86B3DC84584D7F2039B1FED0
# 4CFE79C39390D7A6240B7713FFF1891AB687E62ADAE8460FCF040D02105D2'

# Define the product public key derived from a Riddle&Code crypto tag
# tag_pubkey = b'6ABCA66658E30D4808F6DDABD900723BFB3DE8BF77F86B3DC84584D7F2039B1FED04CFE79C39390D7A6240B7713FFF1891AB687E62ADAE8460FCF040D02105D2'
# Translate public key from tag into a bicgchaindb compliant address
# Results in '5GjT173hXbwm9R5x2Sk4y6NgeqCCA2JrwdyZdzKPvC6a'
# tag_pubkey = ''.join(msg).encode('UTF-8')

# tag_pubkey = b'6ABCA66658E30D4808F6DDABD900723BFB3DE8BF77F86B3DC84584D7F2039B1FED04CFE79C39390D7A6240B7713FFF1891AB687E62ADAE8460FCF040D02105D2'
tag_pubkey = b'AA8BC774646ADF5C9B753652379DE877C70087EB711A351580CC7261738BB65ABE33E1E370190EE74FE79421C8C4F80F9375CE2E687CC5D155C453CB33876Cf7'
print(binascii.hexlify(tag_pubkey))
prdct_pubkey = binascii.hexlify(tag_pubkey)
prdct_pubkey = hashlib.sha3_256(prdct_pubkey).digest()
prdct_pubkey = base58.b58encode(prdct_pubkey)

# prdct_pubkey = b'5GjT173hXbwm9R5x2Sk4y6NgeqCCA2JrwdyZdzKPvC6a'
print(prdct_pubkey)


# Define a private and public key representing the producer
prdusr_privkey, prdusr_pubkey = crypto.generate_key_pair()

print(prdusr_privkey)
print(prdusr_pubkey)

# Define a private and public key representing a future product owner
ownr_privkey, ownr_pubkey = crypto.generate_key_pair()

print(ownr_privkey)
print(ownr_pubkey)

product_asset = {'data': {'product': {'serial_number': '5293748','manufacturer': 'gucci'}}}

metadata = {'spring_season': '2017'}

token_enc = jwt.encode( {'payload':{'asset':product_asset,'meta':metadata}},'secret', algorithm='HS256')


# Create a simple transaction including the  public key signed with
# master key of the BigchainDB instance holder recently created
## prepared_creation_tx = bdb.transactions.prepare(operation='CREATE',signers=prdusr_pubkey,asset=bicycle,metadata=metadata)

# Create a multisig transaction including the three pre-produced public keys signed with
# master key of the BigchainDB instance holder
product_creation_tx = bdb.transactions.prepare(operation='CREATE', signers=prdusr_pubkey, recipients=(prdusr_pubkey, prdct_pubkey, ownr_pubkey),asset=product_asset)

# Sign the multisig
fulfilled_creation_tx = bdb.transactions.fulfill(product_creation_tx, private_keys=prdusr_privkey)

# Write the signed multig transaction to the federated BigchainDB
# Results in {'deleted': 0, 'unchanged': 0, 'errors': 0, 'skipped': 0, 'inserted': 1, 'replaced': 0}
sent_creation_tx = bdb.transactions.send(fulfilled_creation_tx)

# Check the uploaded multisig transaction
# 1st TX id: da7a66280914be1a8f0496598fc15f763cbd70b486f12ee815bf1d8815565c2b
# http://localhost:9984/api/v1/transactions/da7a66280914be1a8f0496598fc15f763cbd70b486f12ee815bf1d8815565c2b

txid = fulfilled_creation_tx['id']
print(txid)

tx_retrieved = bdb.transactions.retrieve(fulfilled_creation_tx['id'])
print(tx_retrieved)

#(riddleenv) Toms-MacBook-Pro:bigchain tomfuerstner$ python3 /Users/tomfuerstner/Documents/Arduino/libraries/CmdMessanger/python-ecc.py
#Connecting to arduino on /dev/cu.usbmodem14311... done.
#D73B763B163E825AA0D2CC39488D4269A213527A5B4DB1E6BC1ED124E015811B068422C86B593E89D36C25B5C34BACAA946114AC4D69CBC81E67A4F8D6C05CCE
#BH6aT2SmwiRW75JwacF5zza7bj6R3HddyazBTK64D7JT
#87onpBweJSvMKw3DPgHVEeotLUZNSUUMgVTxdjyfdBb9
#BsY93oqstqSEqgt473ftQxueMUUJMfC82BWxZ92dJ6Yo
#FTLPmvqdTbPX9awrf2Kbf8gBmm8HbxFqWoTreYyDT7Ww
#9ujXsCydRKt1HzcNyAsPvkPkFZAyrV5arPUSvrjt512x
#da7a66280914be1a8f0496598fc15f763cbd70b486f12ee815bf1d8815565c2b

# Send a challenge
#chl = ''.join(choice(ascii_uppercase) for i in range(12))
#c.send("challenge", chl)
#msg = c.receive()

# should give ["sum_is",[5],TIME_RECEIVED]
#print(msg)
