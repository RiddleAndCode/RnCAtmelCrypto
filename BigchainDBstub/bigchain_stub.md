Connect Riddle&Code Tags to BichchainDB
=======================================

The RiddleAndCode platform provisions secret keys representing physical objects, persons, institutions, contracts, etc... on own smart tag devices and on public ledgers or blockchains. Basically our architecture is blockchain agnostic and works with every blockchain supporting multisignature transactions and smart contracts.

The BigchainDBstub exemplifies this consequently through a connection to a federated BigchainDB instance.

## Setup

Before working with tags and blockchain several things have to be set up:

- Provision TagTok
- Install RethinkDB locally and federated on Amazon Cloud Services
- Install BigchainDB
- Install Python3 and several Python modules

## Provision TagTok

Follow the initial example of programming a Riddle&Code Half-Bean

## Install RethinkDB locally

Follow the instructions on the original [RethinkDB site](https://rethinkdb.com/docs/install/) to install the appropriate version for your operating system.

Once RethinkDB is installed and configured start a database instance locally from within your command line interface by typing in the command: >> RethinkDB

This should result in a console output like this one:

```
  Local-Device-ID:~ User$ rethinkdb
  Running rethinkdb 2.3.4 (CLANG 7.3.0 (clang-703.0.29))...
  Running on Darwin 16.0.0 x86_64
  Loading data from directory /Users/Oxus/rethinkdb_data
  Listening for intracluster connections on port 29015
  Listening for client driver connections on port 28015
  Listening for administrative HTTP connections on port 8080
  Listening on cluster addresses: 127.0.0.1, ::1
  Listening on driver addresses: 127.0.0.1, ::1
  Listening on http addresses: 127.0.0.1, ::1

```

## Install BigchainDB

As BigchainDB requires Python3 make sure that Python3 is installed on your machine.
Before you progress it is advised that Python3 is operated from within a virtual environment.
Therfore install virtualenv for Python. Create a virtualenv instance with the name riddleenv. then. Then start it:

```
  source .bashrc
  workon riddleenv

```

Take care to also install necessary Python extension modules in a next step from within the virtualenv instance:

*  binascii
*  hashlib
*  sha3
*  base58

Check with the Python import command whther they are installed successfully.

Follow the instructions on the BigchainDB GitHub account to install an BigchainDB instance.
Start the successfully installed Bigchain from within the virtualenv riddleenv:

```
  source .bashrc
  workon riddleenv
  bigchaindb start

```

In case everything works as expected your console will show the following output:

```
  (riddleenv) Local-Device-ID:~ User$ bigchaindb start
  INFO:bigchaindb.commands.bigchain:BigchainDB Version 0.5.1
  INFO:bigchaindb.config_utils:Configuration loaded from `/Users/Oxus/.bigchaindb`
  INFO:bigchaindb.commands.bigchain:Starting BigchainDB main process
  INFO:bigchaindb.processes:Initializing BigchainDB...
  INFO:bigchaindb.processes:starting bigchain mapper
  INFO:bigchaindb.processes:starting backlog mapper
  INFO:bigchaindb.processes:starting block
  INFO:bigchaindb.processes:starting voter
  [2016-12-11 22:29:06 +0100] [40453] [INFO] Starting gunicorn 19.6.0
  [2016-12-11 22:29:06 +0100] [40453] [INFO] Listening at: http://127.0.0.1:9984 (40453)
  [2016-12-11 22:29:06 +0100] [40453] [INFO] Using worker: threads
  [2016-12-11 22:29:06 +0100] [40469] [INFO] Booting worker with pid: 40469
  [2016-12-11 22:29:06 +0100] [40470] [INFO] Booting worker with pid: 40470
  INFO:bigchaindb.voter:voter waiting for new blocks
  INFO:bigchaindb.processes:starting election
  INFO:bigchaindb.processes:
  ****************************************************************************
  *                                                                          *
  *   Initialization complete. BigchainDB is ready and waiting for events.   *
  *   You can send events through the API documented at:                     *
  *    - http://docs.bigchaindb.apiary.io/                                   *
  *                                                                          *
  *   Listening to client connections on: localhost:9984                     *
  *                                                                          *
  ****************************************************************************

  [2016-12-11 22:29:06 +0100] [40477] [INFO] Booting worker with pid: 40477
  [2016-12-11 22:29:06 +0100] [40478] [INFO] Booting worker with pid: 40478
  [2016-12-11 22:29:06 +0100] [40479] [INFO] Booting worker with pid: 40479
  [2016-12-11 22:29:07 +0100] [40480] [INFO] Booting worker with pid: 40480
  [2016-12-11 22:29:07 +0100] [40481] [INFO] Booting worker with pid: 40481
  [2016-12-11 22:29:07 +0100] [40482] [INFO] Booting worker with pid: 40482
  [2016-12-11 22:29:07 +0100] [40483] [INFO] Booting worker with pid: 40483
  INFO:bigchaindb.pipelines.block:Write new block 649737ca3db4336edd99d4590a4ff304efdadeca98516e0bc52b09aa1f5b56b8 with 1 transactions
  INFO:bigchaindb.voter:new_block arrived to voter
  INFO:bigchaindb.voter:voting valid for block 649737ca3db4336edd99d4590a4ff304efdadeca98516e0bc52b09aa1f5b56b8

```
