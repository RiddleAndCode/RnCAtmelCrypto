/* -----------------------------------------------------------------------------
 * Example .ino file for arduino, compiled with CmdMessenger.h and
 * CmdMessenger.cpp in the sketch directory. 
 *----------------------------------------------------------------------------*/

#include <Arduino.h>
#include <cryptoauth.h>
#include "CmdMessenger.h"


// If using a ATECC508A then include this define, if ATECC108A then comment outbigchain
// It only affects the defaults on some of the personalisation data.
#define USE_ATECC508

// Object for ATECC508A
AtEccX08 ecc = AtEccX08();

// Keep a record of key slot state for use in error reporting
uint16_t slotLockState = 0xFF;  // Same as SlotLocked, bit per slot, 0=Locked
uint16_t eccKeyState = 0x00;    // Bit per slot, 1 = ECC Key.

// Utility functions

/** displayData - Display packet data in hex.
 *  @param rspPtr packet response pointer
 *  @param bufLen Length of data to display
 */
void displayData( const uint8_t *rspPtr, uint8_t bufLen ) {
  const uint8_t *bufPtr = rspPtr;
  // Display serial number and add to serialNum buffer
  for (int i = 0; i < bufLen; i++ ) {
    if ( bufPtr[i] < 16 ) Serial.print(F("0"));
    Serial.print(bufPtr[i], HEX);
  }
  Serial.println();
}

/** hexify - Convert a character string to its hex representation. Each char becomes
 *  2 hex chars.
 *  @param str - the string pointed to
 *  @param hex - Hex output buffer
 *  @param len -
 */
void hexify(const char *str, const uint8_t *hex, unsigned int len) {
  int i;

  Serial.write(str);
  for (i = 0; i < len; i++)  {
    static char tmp[4] = {};
    sprintf(tmp, "%02X", hex[i]);
    Serial.write(tmp);
  }

//  Serial.write("\n");
  Serial.println();

}

/** displayResponse - take a low I2C driver response code and display
 *  meaningfull message. Checks key slot flags if needed
 *  @param respCode - response code received from driver
 *  @param keyNum - Key number of the slot being worked on
 */
void displayResponse( uint8_t respCode, uint8_t keyNum ) {
  switch (respCode) {
    case 0xD2:
      Serial.print(F("CMD Fail - Parse Error"));
      break;
    case 0xD3:
      Serial.print(F("CMD Fail - "));
      Serial.print(isSlotLocked(keyNum) ? F("Slot locked") : F("No Private key") );
      break;
    case 0xE7:
      Serial.print(F("No Response"));
      break;
    default:
      Serial.print(respCode, HEX);
  }
  Serial.println();
}


/** isSlotLocked - use previously saved flags to test if a key slot has been locked.
 * @param keyNum - Key nubmer to check
 * @return true/false indicating lock state of key
 */
boolean isSlotLocked( uint8_t keyNum ) {
  return slotLockState & (1 << keyNum ) ? false : true;
}

/** displayLockState - display the lock state for the specified zone
 * @param zone - the zone to display, 0 for Config Zone, 1 for Data Zone
 */
void displayLockState( uint8_t zone ) {
  Serial.print( ecc.is_locked( zone ) ? F("") : F(" not" ));
  Serial.println(F(" Locked"));
}
  
void get_random(void) {
  ecc.getRandom();
}


/* Define available CmdMessenger commands */
enum {
    rng_get,
    rng_set,
    pubk_get,
    pubk_set,
    hash_get,
    hash_set,
    sign_get,
    sign_set,
    sum_two_ints,
    sum_is,
    error,
};

/* Initialize CmdMessenger -- this should match PyCmdMessenger instance */
const int BAUD_RATE = 9600;
CmdMessenger c = CmdMessenger(Serial,',',';','/');

/* Create callback functions to deal with incoming messages */

/* callback */
void on_rng_get(void){
    const uint8_t  rng_str[32];
    
    
    ecc.getRandom();
    memcpy (rng_str, ecc.rsp.getPointer(), sizeof(rng_str));

    for (int i = 0; i < 32; i++){
      static char tmp[4] = {};
      sprintf(tmp, "%02X", rng_str[i]);
      c.sendCmd(rng_set, String(tmp));
    }
}

/* callback */
void on_pubk_get(void){

    // D73B763B163E825AA0D2CC39488D4269A213527A5B4DB1E6BC1ED124E015811B068422C86B593E89D36C25B5C34BACAA946114AC4D69CBC81E67A4F8D6C05CCE
    
    const uint8_t pubk_str[64];

    int keyNum = 0;
    
    ecc.genEccKey((uint8_t)keyNum, false);
    memcpy (pubk_str, ecc.rsp.getPointer(), sizeof(pubk_str));
    
    for (int i = 0; i < 64; i++){
      static char tmp[4] = {};
      sprintf(tmp, "%02X", pubk_str[i]);
      c.sendCmd(pubk_set, String(tmp));
    }
}

/* callback */
void on_hash_get(void){
    const uint8_t  hash_str[32];
    // const uint8_t  rng_str[32];
    const uint8_t *req_str;
    
    // ecc.getRandom();
    // memcpy (rng_str, ecc.rsp.getPointer(), sizeof(rng_str));

    /* Grab requested string for hashing from command stream */
    req_str = c.readStringArg();
    
    ecc.calculateSHA256((uint8_t*)req_str, strlen((char*)req_str));
    memcpy (hash_str, ecc.rsp.getPointer(), sizeof(hash_str));

    for (int i = 0; i < 32; i++){
      static char tmp[4] = {};
      sprintf(tmp, "%02X", hash_str[i]);
      c.sendCmd(hash_set, String(tmp));
    }
}

/* callback */
void on_sign_get(void){
    const uint8_t  hash_str[64];
    const uint8_t  sig_str[64];
    const uint8_t *req_str;
    int key_num;

    /* Grab requested string for hashing from command stream */
    req_str = c.readStringArg();

    /* Grab requested ECC key slot number for  from command stream */
    key_num = c.readInt16Arg();
    
    ecc.calculateSHA256((uint8_t*)req_str, strlen((char*)req_str));
    memcpy (hash_str, ecc.rsp.getPointer(), sizeof(hash_str));

    ecc.sign(key_num, &hash_str[0], sizeof(hash_str));
    memcpy (sig_str, ecc.rsp.getPointer(), sizeof(sig_str));
    

    for (int i = 0; i < 64; i++){
      static char tmp[4] = {};
      sprintf(tmp, "%02X", sig_str[i]);
      c.sendCmd(sign_set, String(tmp));
    }
}


/* callback */
void on_unknown_command(void){
    c.sendCmd(error,"Command without callback.");
}

/* Attach callbacks for CmdMessenger commands */
void attach_callbacks(void) { 
  
    c.attach(rng_get,on_rng_get);
    c.attach(pubk_get,on_pubk_get);
    c.attach(hash_get,on_hash_get);
    c.attach(sign_get,on_sign_get);
    c.attach(on_unknown_command);
}

void setup() {
    Serial.begin(BAUD_RATE);
    attach_callbacks();    
}

void loop() {
    c.feedinSerialData();
}

