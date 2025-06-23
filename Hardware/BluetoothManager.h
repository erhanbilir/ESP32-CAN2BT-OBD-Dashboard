#ifndef BLUETOOTHMANAGER_H
#define BLUETOOTHMANAGER_H

#include <BluetoothSerial.h>
#include <Arduino.h>

class BluetoothManager {
public:
    BluetoothManager();
    void begin(const String &deviceName);
    void sendData(const String &data);
private:
    BluetoothSerial SerialBT;
};

#endif // BLUETOOTHMANAGER_H 