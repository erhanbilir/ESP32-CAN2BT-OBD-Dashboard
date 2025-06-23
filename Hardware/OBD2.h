#ifndef OBD2_H
#define OBD2_H

#include <Arduino.h>
#include <mcp2515.h>
#include "CANBus.h"

class OBD2 {
public:
    OBD2(CANBus &canBus);
    void requestNextPID();
    bool parseResponse(const struct can_frame &frame);
    int getRPM() const;
    int getSpeed() const;
    int getTemp() const;
    float getLoad() const;
    String getDataString() const;
private:
    CANBus &canBus;
    int rpm, speed, temp;
    float load;
    uint8_t currentPIDIndex;
    unsigned long lastRequestTime;
    static const uint8_t pidList[];
    static const int numPIDs;
    static const unsigned long requestDelay;
};

#endif // OBD2_H 