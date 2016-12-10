# RnCAtmelCrypto
================

Riddle&Code's Crypto library is the beginning of a platform combining hardware security, public ledger technology and RF technology into a tag and token system. The intention of the system to bring all the innovative capabilities of blockchains into the physical world.

## Prerequisites

- Install the Arduino IDE from [arduino.cc](https://www.arduino.cc/en/Main/Software).
- Clone or download the RnCAtmelCrypto code to your desktop.
- Copy all files to the library folder within your Arduino working library.
- Start the Arduino IDE.
- Follow the cryptoauth-arduino directory into the Examples directory. Start the file Crypto_Examples.ino from witin the Crypto_Examples folder.

### ATECC508a Basics: Provision, Sign and verify

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
