#include <Arduino.h>
#include "CANBus.h"
#include "OBD2.h"
#include "BluetoothManager.h"

CANBus canBus(5, 4); // CS pin 5, INT pin 4
OBD2 obd2(canBus);
BluetoothManager btManager;

void setup() {
    Serial.begin(115200);
    canBus.begin();
    btManager.begin("OBD_BT");
    Serial.println("CAN ready, Bluetooth started.");
}

void loop() {
    obd2.requestNextPID(); // Request the next PID from the OBD-II device
    if (canBus.hasMessage()) {
        struct can_frame frame; // Create a CAN frame to hold the incoming message
        if (canBus.readMessage(frame)) {
            if (obd2.parseResponse(frame)) {
                String dataOut = obd2.getDataString();
                Serial.println("BT -> " + dataOut);
                btManager.sendData(dataOut);
            }
        }
    }
}
