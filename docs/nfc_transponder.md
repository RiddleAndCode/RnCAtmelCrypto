Active NFC Transponder Lib
==========================

The RiddleAndCode platform uses primarily an active NFC transponder to communicate with MCU and crypto chip. The NFC transponder is controlled by an Arduino and Arduino IDE compliant library which supports the standards ISO/IEC 14443-2, 14443-3 and 14443-4.

RnC uses primarily a Type 2 tag which also supports the I2C bus for communication purposes.
This enables to run challenge-response requests via NFC radio frequency instead of requiring a physical connection between a reader device an MCU and the security chip.

RnC uses the simple and energy efficient NXP NTAG I2C - NT3H1201.
The NTAG I2C is the first product of NXP’s NTAG family offering both contactless and contact interfaces. In addition to the passive NFC Forum compliant contactless interface, the IC features an I2C contact interface, which can communicate with a microcontroller if the NTAG I2C is powered from an external power supply. An additional externally powered SRAM mapped into the memory allows a fast data transfer between the RF and I2C interfaces and vice versa, without the write cycle limitations of the EEPROM memory.

## Library Usage

The ntag library consists of a 3 different groups of command. The generic NFC commands to generate the different kinds of NDEF messages like text records, links, simple text strings, etc...

The second command group addresses the special capabilities of the NTAG tags with its combination of EEPROM and SRAM for data storage and exchange. The EEPROM is basically meant to keep data sustainable while the SRAM is  meant to store data only for the time a tag stays connected to NFC readers or NFC enabled mobile phones.

Command group consists of only one command - setting the NTAG NFC ship into "pass-through"
mode. Enabling NTAG and reader to pass through data from phone to I2C connected MCU and other ICs and vice versa.

# Library Interface

## Init Library

Load the necessary ntag modules:

```
  #include <NdefRecord.h>
  #include <ntagsramadapter.h>
  #include "Arduino.h"
  #define HARDI2C
  #include <Wire.h>

  Ntag ntag(Ntag::NTAG_I2C_2K,7,9, 0x55);
  NtagSramAdapter ntagAdapter(&ntag);

```

As this code is meant to be run with additional TWI code (Two Way Interface equals hardware I2C by Atmel), the Arduino and Wire modules are loaded, too.
The NT3H2211 is a 2K EEPROM type device and uses PIN 7 for Field Detection and PIN 9 for  VOUT (Energy Harvesting module) with 0x55 as its I2C HEX address.

As the lib supports different types of NFC tags the specific classes for the NTAG I2C (Mifare Ultralight) with its specific SRAM have to be activated.

## Firmware

This library depends on the following Arduino libraries, which must also be installed:

* [Bounce2](https://github.com/thomasfredericks/Bounce2) by Thomas Fredericks
* [NDEF](https://github.com/LieBtrau/NDEF) by Chridtof Tack & Don Coleman

Arduino library to interface through I²C with the NXP NTAG (NT3H2201)

***WARNING***
-------------

This software is in pre-alpha! It's probably best to make yourself acquainted with all the NTAG I2C capabilities with one of the evaluation and development kits offered by NXP within its NFC IC product line.


Feel free to create a new issue for bugs and features requests. Pull requests are welcome too :)

License
---

To be defined and to be explored. All the code examples follow the many open sourced examples from the tools published on [NXP's webite](https://nxp-rfid.com/products/ntag/ntag-i2c-design-resources/).
