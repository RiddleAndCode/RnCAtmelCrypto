# RnCAtmelCrypto
================

Riddle&Code's Crypto library is the beginning of a platform combining hardware security, public ledger technology and RF technology into a tag and token system. The intention of the system to bring all the innovative capabilities of blockchains into the physical world.

## Prerequisites

- Install the Arduino IDE from [arduino.cc](https://www.arduino.cc/en/Main/Software).
- Clone or download the RnCAtmelCrypto code to your desktop.
- Copy all files to the library folder within your Arduino working library.
- Start the Arduino IDE.
- Follow the cryptoauth-arduino directory into the Examples directory. Start the file Crypto_Examples.ino from within the Crypto_Examples folder.

Beside this, to follow through with all examples it also takes:

For NFC Transponder:

- [NXP Taginfo Reader for Android](https://play.google.com/store/apps/details?id=com.nxp.taginfolite&hl=en)
- [NXP Tagwriter for Android](https://play.google.com/store/apps/details?id=com.nxp.nfc.tagwriter&hl=en)
- [NTAG I2C for Android](https://play.google.com/store/apps/details?id=com.nxp.ntagi2cdemo&hl=en)
- [Basic Android NFC Example Code]()

For Public Ledger/Blockchain:

- [BigchainDB Scalable Blockchain](https://github.com/bigchaindb/bigchaindb)
- [Rnc Blockchain Stub Example]()

## ATECC508a Basics: Provision, Sign and verify

Once the Crypto_Examples code gets executed open the console window from within the Arduino IDE. The console will show a list of basic commands that can be used to operate the crypto IC.

```
    Atmel ATECC508A Test Suite
    ==========================
    1 - Chip Info
    2 - Personalize
    3 - Random Number
    4 - Gen Private Key
    5 - Get Public Key
    6 - Lock key slot
    7 - Hash Data
    8 - Sign Data
    9 - Verify Data
    Choice [1 - 9]
```

**1 - Chip Info** informs about serial and revision number of the specific security IC and about the status of configuration and data zone. The configuration zone defines the most important functionalities of the chip.

**2 - Personalize** The security IC gets initiated with the so called **Personalize** command.
Before using the Atmel® CryptoAuthenticationTM ATECCX08a devices (crypto devices), there are some initialization processes that need to be performed first. The initialization processes consist of personalizing the device and then locking the device.
To make working with the library more convenient all the necessary configuration data are preconfigured to enable provisioning the chip for the specific use case defined by blockchain tech.

**3 - Random Number** starts a continuously running process creating real random numbers. The process can be stopped by sending any deliberate number.

**4 - Generate Private Key** defines one of the three core functionalities (beside Sign & Verify) of the chip. The ATECC508a is set up in a way that it can create up to 15 ECC keys. Every created key has to be stored inside a slot register between 0 and 14. Slot 15 is reserved. Keys can be generated many times for one and the same slot. As long as the slot is not locked with command **6 - Lock key slot**. When a new key gets generated for a slot the old one gets overridden - take care!

**5 - Get Public Key** As it is never possible to read out the original ECC secret key only the Public Key can be derived from a specify slot. When the Public Key gets requested the program also asks for the slot number the according Secret Key is stored in.
Although the secret key can not be read out the key can be used to derive other keys. This way the secret key of one slot can become the seed for another ECC key.

**6 - Lock key slot** freezes the secret key into its slot register. Once this happens it is not possible anymore to generate a new ECC for the locked slot.

**7 - Hash Data** defines a hardware accelerated SHA256 hashing algorithm that can be use with command number 7. It always require a string to be hashed. The routine behind command 7 is also an integral part of the signing and verifying commands.

**8 - Sign Data** requires an input string which first gets hashed and then signed with the secret key from a also to be defined slot. It's up to the program to handle the signature as the crypto chip doesn't store it anywhere.

**9 - Verify Data** To operate the verify commands takes first the constituting string of the signature, the signature itself and the public key belonging to the secret key that was used for the production of the signature. Once all requested inputs are made available to the cryptochip the validation part of the challenge response routine can happen.


## Connect Riddle&Code Half-Bean to Arduino UNO

The RnC Half-Bean is a I2C ready flexible circuit board combining an crypto chip with an active NFC transponder. Any connected MCU can talk to both ICs - to the crypto IC and to the NFC IC - over the I2C bus.

The NFC transponder enables beside the I2C bus also a direct RF communication with the crypto chip.

To connect an Arduino Uno to the Half-Bean the 3.3V, GND, SDA and SCL pins have to connected to each other. To avoid capacitance problems on the I2C bus the connection between the devices should be as short as possible.

The connection logic follows the [PIN connection](imgs/halfbean_uno_connect.png) as shown:

![PIN connections](https://github.com/RiddleAndCode/RnCAtmelCrypto/blob/master/imgs/halfbean_uno_connect.png)

## Next Steps

This repo is containing the ongoin development process of the RiddleAndCode platform including the official protocol docs, hardware designs, blockchain stubs, etc....

Quick links to other documents:

* [Active NFC Transponder Library](https://github.com/RiddleAndCode/RnCAtmelCrypto/blob/master/docs/nfc_transponder.md)
* [Connect Half-Bean to Blockchain](https://github.com/RiddleAndCode/RnCAtmelCrypto/blob/master/BigchainDBstub/bigchain_stub.md)
