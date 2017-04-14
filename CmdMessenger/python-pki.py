# ------------------------------------------------------------------------------
# Python program using the library to interface with the arduino sketch above.
# ------------------------------------------------------------------------------

import PyCmdMessenger
from random import choice
from string import ascii_uppercase

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






# Define a private and public key representing the producer
tag1_privkey, tag1_pubkey = crypto.generate_key_pair()

print("Tag1 PKI: ")
print(tag1_privkey)
print(tag1_pubkey)
print('')

# Define a private and public key representing a future product owner
tag2_privkey, tag2_pubkey = crypto.generate_key_pair()

print("Tag2 PKI: ")
print(tag2_privkey)
print(tag2_pubkey)
print('')

# Define a private and public key representing a future product owner
tag3_privkey, tag3_pubkey = crypto.generate_key_pair()

print("Tag3 PKI: ")
print(tag3_privkey)
print(tag3_pubkey)
print('')

# Define a private and public key representing a future product owner
tag4_privkey, tag4_pubkey = crypto.generate_key_pair()

print("Tag4 PKI: ")
print(tag4_privkey)
print(tag4_pubkey)
print('')

# Define a private and public key representing a future product owner
tag5_privkey, tag5_pubkey = crypto.generate_key_pair()

print("Tag5 PKI: ")
print(tag5_privkey)
print(tag5_pubkey)
print('')

# Define a private and public key representing a future product owner
tag6_privkey, tag6_pubkey = crypto.generate_key_pair()

print("Tag6 PKI: ")
print(tag6_privkey)
print(tag6_pubkey)
print('')
