#ifndef CANBUS_H
#define CANBUS_H

#include <mcp2515.h>
#include <SPI.h>
#include <Arduino.h>

class CANBus {
public:
    CANBus(uint8_t csPin, uint8_t intPin);
    void begin();
    bool sendMessage(const struct can_frame &frame);
    bool readMessage(struct can_frame &frame);
    bool hasMessage();
private:
    MCP2515 mcp2515;
    uint8_t intPin;
};

#endif // CANBUS_H 