# ------------------------------------------------------------------------------
# Python program using the library to interface with the arduino sketch above.
# ------------------------------------------------------------------------------

import PyCmdMessenger
from random import choice
from string import ascii_uppercase

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

# Initialize an ArduinoBoard instance.  This is where you specify baud rate and
# serial timeout.  If you are using a non ATmega328 board, you might also need
# to set the data sizes (bytes for integers, longs, floats, and doubles).
# Check the right board number from within the Arduino IDE. Take care that the
# internal Terminal of the Arduino IDE is not active. It would block the serial
# port for the PySerial.
arduino = PyCmdMessenger.ArduinoBoard("/dev/cu.usbmodem1431",baud_rate=9600)

# List of commands and their associated argument formats. These must be in the
# same order as in the sketch.
commands = [["rng_get",""],
            ["rng_set","s"],
            ["pubk_get",""],
            ["pubk_set","s"],
            ["hash_get","s"],
            ["hash_set","s"],
            ["sign_get","si"],
            ["sign_set","s"]]

# Initialize the messenger
c = PyCmdMessenger.CmdMessenger(arduino,commands)

# Send request for random number
c.send("rng_get")

# Receive random number
count = 0
msg = []
while (count < 32):
   count = count + 1
   msg.append(c.receive()[1][0])
   # print(c.receive())

print(''.join(msg))
print('')

# Send request for public key
c.send("pubk_get")
# Receive. Should give ["my_name_is",["HEXvalue"],TIME_RECIEVED]
count = 0
msg = []
while (count < 64):
   count = count + 1
   msg.append(c.receive()[1][0])
   # print(c.receive())

print(''.join(msg))
print('')

# Send request for hashing a string
c.send("hash_get","826762")

# Receive random number
count = 0
msg = []
while (count < 32):
   count = count + 1
   msg.append(c.receive()[1][0])
   # print(c.receive())

print(''.join(msg))
print('')

# Send request for signing a (randomized) string
c.send("sign_get","826762",0)

# Receive random number
count = 0
msg = []
while (count < 64):
   count = count + 1
   msg.append(c.receive()[1][0])
   # print(c.receive())

print(''.join(msg))
print('')

# The following HEX string represents an ECC public key belonging to the secret key
# of a crypto tag inside a product
# '6ABCA66658E30D4808F6DDABD900723BFB3DE8BF77F86B3DC84584D7F2039B1FED0
# 4CFE79C39390D7A6240B7713FFF1891AB687E62ADAE8460FCF040D02105D2'

# Define the product public key derived from a Riddle&Code crypto tag
# tag_pubkey = b'6ABCA66658E30D4808F6DDABD900723BFB3DE8BF77F86B3DC84584D7F2039B1FED04CFE79C39390D7A6240B7713FFF1891AB687E62ADAE8460FCF040D02105D2'
# Translate public key from tag into a bicgchaindb compliant address
# Results in '5GjT173hXbwm9R5x2Sk4y6NgeqCCA2JrwdyZdzKPvC6a'

tag_pubkey = ''.join(msg).encode('UTF-8')

prdct_pubkey = binascii.hexlify(bytearray(tag_pubkey))
prdct_pubkey = hashlib.sha3_256(prdct_pubkey).digest()
prdct_pubkey = base58.b58encode(prdct_pubkey)

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
fulfilled_creation_tx = bdb.transactions.fulfill(product_creation_tx, private_keys=(prdusr_privkey, ownr_pubkey))

# Write the signed multig transaction to the federated BigchainDB
# Results in {'deleted': 0, 'unchanged': 0, 'errors': 0, 'skipped': 0, 'inserted': 1, 'replaced': 0}
sent_creation_tx = bdb.transactions.send(fulfilled_creation_tx)

# Check the uploaded multisig transaction
# 1st TX id: da7a66280914be1a8f0496598fc15f763cbd70b486f12ee815bf1d8815565c2b
# http://localhost:9984/api/v1/transactions/da7a66280914be1a8f0496598fc15f763cbd70b486f12ee815bf1d8815565c2b

txid = fulfilled_creation_tx['id']
print(txid)

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
