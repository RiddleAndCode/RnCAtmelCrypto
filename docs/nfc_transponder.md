Active NFC Transponder Lib
==========================

The RiddleAndCode platform uses primarily an active NFC transponder to communicate with MCU and crypto chip. The NFC transponder is controlled by an Arduino and Arduino IDE compliant library which supports the standards ISO/IEC 14443-2, 14443-3 and 14443-4.

RnC uses primarily a Type 2 tag which also supports the I2C bus for communication purposes.
This enables to run challenge-response requests via NFC radio frequency instead of requiring a physical connection between a reader device an MCU and the security chip.




***WARNING***
-------------

This software is in pre-alpha! It's probably best to provision your ATECC508a with one of the evaluation and development kits offered by Atmel within its Security IC product line.


Feel free to create a new issue for bugs and features requests. Pull requests are welcome too :)

License
---

Atmel's code is licensed under a custom open source license. It is
included under `extras`. We  share Josh Datko's and ThingInnovations interpretation of the license which follows the view of
[these guys](https://github.com/Pinoccio/library-atmel-lwm/blob/master/README.md).
