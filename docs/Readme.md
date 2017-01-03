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

## Get Serial Number

Every NFC tag has its very own and unique serial number. It is a convenient way to see whether NFC tag is present and responding to commands sent:

```
  void getSerialNumber(){
    byte* sn=(byte*)malloc(ntag.getUidLength());
    Serial.println();
    if(ntag.getUid(sn,7))
    {
        Serial.print("Serial number of the tag is: ");
        for(byte i=0;i<ntag.getUidLength();i++)
        {
            Serial.print(sn[i], HEX);
            Serial.print(" ");
          }
        }
        Serial.println();
        free(sn);
      }

```

## Simple Write to Tag

Create a simple link-type NDEF message and write it to the tag. Then test it with a NFC reader program on your mobile phone, like [NXP's NFC Taginfo reader](https://play.google.com/store/apps/details?id=com.nxp.taginfolite&hl=en):

```
  void testWriteAdapter(){
    NdefMessage message = NdefMessage();
    message.addUriRecord("http://www.google.com");
    if(ntagAdapter.write(message)){
        Serial.println("Message written to tag.");
      }
    }

```

## Test Ntag's EEPROM

Ntag's EEPROM is called User Memory, opposed to the SRAM's name Session Memory.To test reading and writing to the User Memory use the writeEeprom() and readEeprom() commands:

```
void testUserMem(){
  byte eepromdata[2*16];
  byte readeeprom[16];

  for(byte i=0;i<2*16;i++){
      eepromdata[i]=0x80 | i;
  }

  Serial.println("Writing block 1");
  if(!ntag.writeEeprom(0,eepromdata,16)){
      Serial.println("Write block 1 failed");
  }
  Serial.println("Writing block 2");
  if(!ntag.writeEeprom(16,eepromdata+16,16)){
      Serial.println("Write block 2 failed");
  }
  Serial.println("\nReading memory block 1");
  if(ntag.readEeprom(0,readeeprom,16)){
      showBlockInHex(readeeprom,16);
  }
  Serial.println("Reading memory block 2");
  if(ntag.readEeprom(16,readeeprom,16)){
      showBlockInHex(readeeprom,16);
  }
  Serial.println("Reading bytes 10 to 20: partly block 1, partly block 2");
  if(ntag.readEeprom(10,readeeprom,10)){
      showBlockInHex(readeeprom,10);
  }
  Serial.println("Writing byte 15 to 20: partly block 1, partly block 2");
  for(byte i=0;i<6;i++){
      eepromdata[i]=0x70 | i;
  }
  if(ntag.writeEeprom(15,eepromdata,6)){
      Serial.println("Write success");
  }
  Serial.println("\nReading memory block 1");
  if(ntag.readEeprom(0,readeeprom,16)){
      showBlockInHex(readeeprom,16);
  }
  Serial.println("Reading memory block 2");
  if(ntag.readEeprom(16,readeeprom,16)){
      showBlockInHex(readeeprom,16);
  }
}

```


## Test Ntag's EEPROM

Ntag's SRAM is called Session Memory. Data written to the Session Memory only last for the time a reader stays connected to the Ntag. The reason is that the Session Memory doesn't know any read/write restrictions. In case it is important to store the Session data also within the USer Memory the setSramMirrorRf() command can be used to store data permanently in the User Memory. To test reading and writing to the Session Memory use the writeSram() and readSram() commands. Check the SramMirror example to learn how to map session data to the EEPROM:

```
void testSram(){
    byte data[16];
    Serial.println("Reading SRAM block 0xF8");
    if(ntag.readSram(0,data,16)){
        showBlockInHex(data,16);
    }
    for(byte i=0;i<16;i++){
        data[i]=0xF0 | i;
    }
    Serial.println("Writing dummy data to SRAM block 0xF8");
    if(!ntag.writeSram(0,data,16)){
        return;
    }
    Serial.println("Reading SRAM block 0xF8 again");
    if(ntag.readSram(0,data,16)){
        showBlockInHex(data,16);
    }
}

void testSramMirror(){
    byte readeeprom[16];
    byte data;

    if(!ntag.setSramMirrorRf(false,1))return;
    Serial.println("\nReading memory block 1, no mirroring of SRAM");
    if(ntag.readEeprom(0,readeeprom,16)){
        showBlockInHex(readeeprom,16);
    }
    Serial.println("\nReading SRAM block 1");
    if(ntag.readSram(0,readeeprom,16)){
        showBlockInHex(readeeprom,16);
    }
    if(!ntag.setSramMirrorRf(true,1))return;
    Serial.print("NC_REG: ");
    if(ntag.readRegister(Ntag::NC_REG,data)){
        Serial.println(data, HEX);
    }
    Serial.println("Use an NFC-reader to verify that the SRAM has been mapped to the memory area that the reader will access by default.");
}

```
## Ntag Register

Beside User Memory and Session Memory Ntag also knows a register. Data written to the register configure and define the overall behavior of the NTAG I2C. E.g.: the state the Ntag - whether the tag is communication with the RF module or via the I2C bus. The structure of the I2C register methods differ from the other commands. Therefor it take readRegister() and writeRegister(). Be aware of the fact that some register data can only be changed at the beginning of an RF session. To learn about all the details of configuring the Ntag chip check out the [Original documentation](http://www.nxp.com/products/identification-and-security/nfc-and-reader-ics/connected-tag-solutions/ntag-ic-plus-connected-nfc-tag-with-ic-interface:NT3H2111_2211?&fpsp=1&tab=Documentation_Tab#nogo):

```
  void testRegisterAccess(){
    byte data;
    Serial.println(ntag.readRegister(Ntag::NC_REG,data));
    Serial.println(data,HEX);
    Serial.println(ntag.writeRegister(Ntag::NC_REG,0x0C,0x0A));
    Serial.println(ntag.readRegister(Ntag::NC_REG,data));
    Serial.println(data,HEX);
  }

```

## Firmware

This library depends on the following Arduino libraries, which must also be installed:

* [Bounce2](https://github.com/thomasfredericks/Bounce2) by Thomas Fredericks
* [NDEF](https://github.com/LieBtrau/NDEF) by Christof Tack & Don Coleman

Arduino library to interface through I²C with the NXP NTAG (NT3H2111)

***WARNING***
-------------

This software is in pre-alpha! It's probably best to make yourself acquainted with all the NTAG I2C capabilities with one of the evaluation and development kits offered by NXP within its NFC IC product line.


Feel free to create a new issue for bugs and features requests. Pull requests are welcome too :)

License
---

To be defined and to be explored. All the code examples follow the many open sourced examples from the tools published on [NXP's webite](https://nxp-rfid.com/products/ntag/ntag-i2c-design-resources/).
