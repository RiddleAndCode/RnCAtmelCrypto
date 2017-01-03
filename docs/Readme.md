#Riddle&Code NFC Intro
==========================

## Toolset

1. [Android Studio](https://developer.android.com/studio/index.html)
2. [NXP NTAG I2C DK](http://www.nxp.com/products/wireless-connectivity/nfc-and-reader-ics/connected-tag-solutions/ntag-ic-plus-explorer-kit-development-kit:OM5569-NT322E)
3. [NXP Taginfo](https://play.google.com/store/apps/details?id=com.nxp.taginfolite&hl=en)
4. [NXP TagWriter](https://play.google.com/store/apps/details?id=com.nxp.nfc.tagwriter&hl=en)
5. [NXP I2C Demoboard](https://play.google.com/store/apps/details?id=com.nxp.ntagi2cdemo&hl=en)

The toolset is essential to have the as a reference to validate the binary data strings constituting the diverse NFC protocols.

## Documentation

Riddle&Code uses NXP's NTAG I2C active transponder chips. These are NFC Forum Type 2 tags supporting I2C bus system and energy harvesting via a special addon module. This means the chip initially supports two different communication protocols. I2C to control the transponder from an approprite MCU (Microcontroller) and at the same time via radio frequency according to the  ISO/IEC 14443-2 protocol.

[NTAG I2C - Energy harvesting Type 2 Tag with I2C interface](http://www.nxp.com/documents/data_sheet/NT3H1101_1201.pdf)

All the peculiarities of the NTAG I2C NFC tag casn be fount in its documentation and specification sheet.

[Atmel Intro ISO/IEC 14443](http://www.atmel.com/images/doc2056.pdf)

A basic introduction into the ISO/IEC 14443 to get a feeling for the command structure of the protocol and to be able to understand what the Android NFC methods are meant to do. Android's NFC API supports several protocols and it is initially not easy to distinguish between them.

[NDEF NFC Data Exchange Format](https://learn.adafruit.com/adafruit-pn532-rfid-nfc/ndef)

NDEF defines the way data gets transferred and exchanged within the Riddle&Code system between tags, microcontrollers, sensors, actuator, mobile pones and big data services. Adafruit offers several NFC ready MCUs and their NFC tutorials are excellent. Way easier to follow compared to reading the original NFC Forum specifications.

## Basic Architecture

The basic setup of Riddle&Code smart tag components consist of a microcontroller (ARM Cortex M0+ and M4) connected via I2C bus to a crypto chips (ECC-Elliptic Curve Crypto) and a NFC chip. The MCU is powered via an energy harvesting module that draws power from the induction field that happens when bringing a NFC reader or mobile phone close to the tag. This way the smart tag operates battery-less. This combinations offers a lot of innovative use cases for proximity and identity services.

As within this architecture the MCU and the NFC reader/writer can communicate with the NFC chip at the same time any kind of data exchange has to be well orchestrated.

NXP's NTAG I2C NFC chips supports this pretty well. But it take a a careful and defensive programming style.

[The NTAG I2C demoboard and demoboard application](http://www.nxp.com/documents/application_note/AN11597.pdf)

The demo app is a good example but as showcase app to rich in functionality. this makes it difficult to get the essentials.

[Beginning NFC](https://www.amazon.com/Beginning-NFC-Communication-Arduino-PhoneGap-ebook/dp/B00HV1GP3W/ref=sr_1_1?s=digital-text&ie=UTF8&qid=1483436888&sr=1-1&keywords=Beginning+NFC)

A book written by and for the Arduino community ( Tom Igoe, Don Coleman, Brian Jepson) as an intro text into the all matters of NFC. NFC is a mix of many technologoes and protocols and it takes a while to understand and digest all the informations.

***WARNING***
-------------

This software is in pre-alpha! It's probably best to make yourself acquainted with all the NTAG I2C capabilities with one of the evaluation and development kits offered by NXP within its NFC IC product line.


Feel free to create a new issue for bugs and features requests. Pull requests are welcome too :)

License
---

To be defined and to be explored. All the code examples follow the many open sourced examples from the tools published on [NXP's webite](https://nxp-rfid.com/products/ntag/ntag-i2c-design-resources/).
