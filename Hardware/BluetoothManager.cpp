#include "BluetoothManager.h"

BluetoothManager::BluetoothManager() {}

/*!< Initializes the Bluetooth manager with a default name */
void BluetoothManager::begin(const String &deviceName) {
    SerialBT.begin(deviceName);
}

/*!< Sends data over Bluetooth */
void BluetoothManager::sendData(const String &data) {
    SerialBT.println(data);
} 