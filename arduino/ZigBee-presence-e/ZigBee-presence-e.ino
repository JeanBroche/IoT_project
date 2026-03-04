#include <XBee.h>
#include <SoftwareSerial.h>

XBee xbee = XBee();
SoftwareSerial xbeeSerial(0, 1);

// ==================== Helpers AT ====================

bool sendATCommand(uint8_t* cmd, uint8_t* value, uint8_t valueLen) {
    AtCommandRequest atRequest = AtCommandRequest(cmd, value, valueLen);
    AtCommandResponse atResponse = AtCommandResponse();
    xbee.send(atRequest);
    delay(500);
    if (xbee.readPacket(1000)) {
        if (xbee.getResponse().getApiId() == AT_COMMAND_RESPONSE) {
            xbee.getResponse().getAtCommandResponse(atResponse);
            return atResponse.getStatus() == AT_OK;
        }
    }
    return false;
}

bool sendATCommandNoValue(uint8_t* cmd) {
    AtCommandRequest atRequest = AtCommandRequest(cmd);
    AtCommandResponse atResponse = AtCommandResponse();
    xbee.send(atRequest);
    delay(500);
    if (xbee.readPacket(1000)) {
        if (xbee.getResponse().getApiId() == AT_COMMAND_RESPONSE) {
            xbee.getResponse().getAtCommandResponse(atResponse);
            return atResponse.getStatus() == AT_OK;
        }
    }
    return false;
}

// ✅ Teste si le XBee répond au baudrate donné
bool probeXBee(long baudrate) {
    xbeeSerial.end();
    delay(100);
    xbeeSerial.begin(baudrate);
    xbee.setSerial(xbeeSerial);
    delay(200);

    uint8_t cmdVR[] = {'V', 'R'};
    AtCommandRequest atRequest = AtCommandRequest(cmdVR);
    AtCommandResponse atResponse = AtCommandResponse();
    xbee.send(atRequest);
    delay(500);
    if (xbee.readPacket(1000)) {
        if (xbee.getResponse().getApiId() == AT_COMMAND_RESPONSE) {
            xbee.getResponse().getAtCommandResponse(atResponse);
            return atResponse.getStatus() == AT_OK;
        }
    }
    return false;
}

// ==================== Configuration ====================

void configureXBee() {
    uint8_t cmdID[] = {'I', 'D'};
    uint8_t panId[] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x12, 0x34};
    Serial.println(sendATCommand(cmdID, panId, sizeof(panId)) ? "✓ PAN ID" : "✗ PAN ID");

    // Coordinateur CE=1 (différence avec le récepteur)
    uint8_t cmdCE[] = {'C', 'E'};
    uint8_t coordValue[] = {0x01};
    Serial.println(sendATCommand(cmdCE, coordValue, sizeof(coordValue)) ? "✓ Coordinateur" : "✗ Coordinateur");

    uint8_t cmdAP[] = {'A', 'P'};
    uint8_t apiMode[] = {0x02};
    Serial.println(sendATCommand(cmdAP, apiMode, sizeof(apiMode)) ? "✓ API 2" : "✗ API 2");

    uint8_t cmdSC[] = {'S', 'C'};
    uint8_t channel[] = {0x00, 0x0C};
    Serial.println(sendATCommand(cmdSC, channel, sizeof(channel)) ? "✓ Canal" : "✗ Canal");

    uint8_t cmdBD[] = {'B', 'D'};
    uint8_t baud[] = {0x07};
    Serial.println(sendATCommand(cmdBD, baud, sizeof(baud)) ? "✓ Baudrate 115200" : "✗ Baudrate");

    uint8_t cmdWR[] = {'W', 'R'};
    Serial.println(sendATCommandNoValue(cmdWR) ? "✓ Sauvegardé" : "✗ Sauvegarde");

    uint8_t cmdAC[] = {'A', 'C'};
    Serial.println(sendATCommandNoValue(cmdAC) ? "✓ Appliqué" : "✗ Apply");

    xbeeSerial.end();
    delay(200);
    xbeeSerial.begin(115200);
    xbee.setSerial(xbeeSerial);
    delay(200);
    while (xbeeSerial.available()) xbeeSerial.read();

    Serial.println("Configuration terminée.");
}

// ==================== Émission ====================

XBeeAddress64 destAddr = XBeeAddress64(0x00000000, 0x0000FFFF);
#define PIR_MOTION_SENSOR 2

void sendBool(bool value) {
    uint8_t payload[1];
    payload[0] = value ? 0x01 : 0x00;
    ZBTxRequest zbTx = ZBTxRequest(destAddr, payload, sizeof(payload));
    xbee.send(zbTx);
}

void loop() {
    int sensorValue = digitalRead(PIR_MOTION_SENSOR);
    sendBool(sensorValue == HIGH);
    delay(2000);
}

// ==================== Setup ====================

void setup() {
    pinMode(PIR_MOTION_SENSOR, INPUT);
    Serial.begin(115200);
    delay(2000);

    Serial.println("Détection baudrate XBee...");

    if (probeXBee(115200)) {
        Serial.println("XBee détecté à 115200, pas de reconfiguration baudrate.");
        configureXBee();
    } else if (probeXBee(9600)) {
        Serial.println("XBee détecté à 9600, configuration complète...");
        configureXBee();
    } else {
        Serial.println("⚠ XBee non détecté ! Vérifie le câblage.");
    }
}