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

bool probeXBee(long baudrate) {
    xbeeSerial.end();
    delay(500);
    xbeeSerial.begin(baudrate);
    xbee.setSerial(xbeeSerial);
    delay(200);

    // Envoie commande AT "VR" (version) comme ping
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
    Serial.println("Configuration XBee...");

    uint8_t cmdID[] = {'I', 'D'};
    uint8_t panId[] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x12, 0x34};
    Serial.println(sendATCommand(cmdID, panId, sizeof(panId)) ? "✓ PAN ID" : "✗ PAN ID");

    uint8_t cmdCE[] = {'C', 'E'};
    uint8_t routerValue[] = {0x00};
    Serial.println(sendATCommand(cmdCE, routerValue, sizeof(routerValue)) ? "✓ Router" : "✗ Router");

    uint8_t cmdAP[] = {'A', 'P'};
    uint8_t apiMode[] = {0x02};
    Serial.println(sendATCommand(cmdAP, apiMode, sizeof(apiMode)) ? "✓ API 2" : "✗ API 2");

    uint8_t cmdSC[] = {'S', 'C'};
    uint8_t channel[] = {0x00, 0x0C};
    Serial.println(sendATCommand(cmdSC, channel, sizeof(channel)) ? "✓ Canal" : "✗ Canal");

    // N'envoie BD que si on était encore à 9600
    uint8_t cmdBD[] = {'B', 'D'};
    uint8_t baud[] = {0x07};
    Serial.println(sendATCommand(cmdBD, baud, sizeof(baud)) ? "✓ Baudrate 115200" : "✗ Baudrate");

    uint8_t cmdWR[] = {'W', 'R'};
    Serial.println(sendATCommandNoValue(cmdWR) ? "✓ Sauvegardé" : "✗ Sauvegarde");

    uint8_t cmdAC[] = {'A', 'C'};
    Serial.println(sendATCommandNoValue(cmdAC) ? "✓ Appliqué" : "✗ Apply");

    // Basculer à 115200 après config
    xbeeSerial.end();
    delay(200);
    xbeeSerial.begin(115200);
    xbee.setSerial(xbeeSerial);
    delay(200);
    while (xbeeSerial.available()) xbeeSerial.read();

    Serial.println("Configuration terminée.");
}

// ==================== Réception ====================

bool receiveBool() {
    ZBRxResponse rx = ZBRxResponse();
    xbee.getResponse().getZBRxResponse(rx);
    return rx.getData(0) == 0x01;
}

void loop() {
    if (xbeeSerial.available()) {
        xbee.readPacket();

        if (xbee.getResponse().isAvailable()) {
            if (xbee.getResponse().getApiId() == ZB_RX_RESPONSE) {
                bool value = receiveBool();
                Serial.println(value );
            }
        }

        /*if (xbee.getResponse().isError()) {
            Serial.print("Erreur XBee code: ");
            Serial.println(xbee.getResponse().getErrorCode());
        }*/
    }
}

// ==================== Setup ====================

void setup() {
    Serial.begin(9600);
    delay(2000);

    // Détection automatique du baudrate actuel du XBee
    Serial.println("Détection baudrate XBee...");

    if (probeXBee(115200)) {
        // Déjà à 115200 → pas besoin de renvoyer BD
        Serial.println("XBee détecté à 115200, pas de reconfiguration baudrate.");
        // On configure quand même les autres paramètres
        configureXBee();
    } else if (probeXBee(9600)) {
        // Encore à 9600 → configuration complète
        Serial.println("XBee détecté à 9600, configuration complète...");
        configureXBee();
    } else {
        Serial.println("⚠ XBee non détecté ! Vérifie le câblage.");
    }
}