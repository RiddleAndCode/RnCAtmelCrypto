cryptoauth-arduino
==================

An Arduino library for Atmel's CryptoAuthentication ICs ( ATECC108a and  ATECC508a). The library is derived from code originally done by Josh Datko and from code explorations by ThingInnovations. The implementations contained a lot of legacy code, bugs and didn't make the most interesting aspects of the new ATECC508A available.

It is a rewrite and extension of the original code done in 2015 by Riddle&Code.

This version is a fork of the original Cryptotronix cryptoauth-arduino library with the following changes:

* Replace Atmel code with updated code that supports the ATECC508 chips
* Update API to implement additional functionality to retrieve chip info, lock individual slots, add key selection to sign and verify functions.
* Provide a comprehensive example/demo sketch covering personalization, public and private key generation, SHA256 hash generation, Diffie-Hellmann key exchange, message signing and verification functions, active NFC transponder support via I2C bus connection etc, ....

We follow the original Readme warning below:


***WARNING***
-------------

This software is in pre-alpha! It's probably best to provision your ATECC508a with one of the evaluation and development kits offered by Atmel within its Security IC product line.


Feel free to create a new issue for bugs and features requests. Pull requests are welcome too :)

License
---

Atmel's code is licensed under a custom open source license. It is
included under `extras`. We  share Josh Datko's and ThingInnovations interpretation of the license which follows the view of
[these guys](https://github.com/Pinoccio/library-atmel-lwm/blob/master/README.md).
