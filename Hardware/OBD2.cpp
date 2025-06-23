#include "OBD2.h"

/*!< pidList can be customized to obtain the desired data, different PIDs can be added or existing ones can be removed.. */
const uint8_t OBD2::pidList[] = {0x0C, 0x0D, 0x05, 0x04};
const int OBD2::numPIDs = sizeof(OBD2::pidList);

/*!< Data sending frequency */
const unsigned long OBD2::requestDelay = 31.25;

/*!< Constructor initializes the OBD2 object with a CANBus instance 
     and sets initial values for RPM, speed, temperature, load, and other parameters.*/
OBD2::OBD2(CANBus &canBus) : canBus(canBus), rpm(0), speed(0), temp(0), load(0.0), currentPIDIndex(0), lastRequestTime(0) {}

void OBD2::requestNextPID() {
    unsigned long now = millis();
    if (now - lastRequestTime >= requestDelay) {
        struct can_frame request;
        request.can_id = 0x7DF;
        request.can_dlc = 8;
        request.data[0] = 0x02;
        request.data[1] = 0x01;
        request.data[2] = pidList[currentPIDIndex];
        for (int i = 3; i < 8; i++) request.data[i] = 0x55;
        canBus.sendMessage(request);
        lastRequestTime = now;
        currentPIDIndex = (currentPIDIndex + 1) % numPIDs;
    }
}

/*!< Parses the response from the OBD-II device based on the CAN frame received. */
bool OBD2::parseResponse(const struct can_frame &frame) {
    if (frame.can_id == 0x7E8 && frame.data[0] >= 3 && frame.data[1] == 0x41) {
        uint8_t pid = frame.data[2];
        switch (pid) {
            case 0x0C:
                rpm = ((frame.data[3] << 8) | frame.data[4]) / 4;
                break;
            case 0x0D:
                speed = frame.data[3];
                break;
            case 0x05:
                temp = frame.data[3] - 40;
                break;
            case 0x04:
                load = (frame.data[3] * 100.0) / 255.0;
                break;
            default:
                return false;
        }
        return true;
    }
    return false;
}

/*!< Getters for the OBD-II data attributes */
int OBD2::getRPM() const { return rpm; }
int OBD2::getSpeed() const { return speed; }
int OBD2::getTemp() const { return temp; }
float OBD2::getLoad() const { return load; }

/*!< Returns a string representation of the OBD - II data in the format "speed,rpm,load,temp". */ 
String OBD2::getDataString() const {
    return String(speed) + "," + String(rpm) + "," + String(load, 1) + "," + String(temp);
} 