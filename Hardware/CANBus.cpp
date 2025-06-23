#include "CANBus.h"

CANBus::CANBus(uint8_t csPin, uint8_t intPin) : mcp2515(csPin), intPin(intPin) {}

/*!< Initializes the CAN bus interface */
void CANBus::begin() {
    SPI.begin();
    mcp2515.reset();
    mcp2515.setBitrate(CAN_500KBPS, MCP_8MHZ);
    mcp2515.setNormalMode();
    pinMode(intPin, INPUT);
}

/*!< Sends a CAN message */
bool CANBus::sendMessage(const struct can_frame &frame) {
    return mcp2515.sendMessage(&frame) == MCP2515::ERROR_OK;
}

/*!< Reads a CAN message into the provided frame structure */
bool CANBus::readMessage(struct can_frame &frame) {
    return mcp2515.readMessage(&frame) == MCP2515::ERROR_OK;
}

/*!< Checks if there is a new CAN message available */
bool CANBus::hasMessage() {
    return digitalRead(intPin) == LOW;
} 