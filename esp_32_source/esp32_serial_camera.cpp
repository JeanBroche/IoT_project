#include "esp_camera.h"
#include "Arduino.h"

// Pinning for XIAO ESP32S3 Sense (OV2640)
#define PWDN_GPIO_NUM -1
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 10
#define SIOD_GPIO_NUM 40
#define SIOC_GPIO_NUM 39

#define Y9_GPIO_NUM 48
#define Y8_GPIO_NUM 11
#define Y7_GPIO_NUM 12
#define Y6_GPIO_NUM 14
#define Y5_GPIO_NUM 16
#define Y4_GPIO_NUM 18
#define Y3_GPIO_NUM 17
#define Y2_GPIO_NUM 15
#define VSYNC_GPIO_NUM 38
#define HREF_GPIO_NUM 47
#define PCLK_GPIO_NUM 13

unsigned long lastCaptureTime = 0;
const unsigned long captureInterval = 5000; // 5 secs

void sendImage() {
  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) return;

  uint32_t size = fb->len;
  uint8_t header[2] = {0xAA, 0x55};

  // Send header
  Serial.write(header, 2);
  // Send size (4 octets)
  Serial.write((uint8_t*)&size, 4);
  // Send image
  Serial.write(fb->buf, fb->len);

  Serial.flush();

  esp_camera_fb_return(fb);
}

void setup() {
  Serial.begin(921600);

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  config.frame_size = FRAMESIZE_VGA;  // 640x480
  config.jpeg_quality = 5;
  config.fb_count = 1;

  // if (psramFound()) {
  //   config.frame_size = FRAMESIZE_VGA;  // 640x480
  //   config.jpeg_quality = 5;
  //   config.fb_count = 1;
  // } else {
  //   config.frame_size = FRAMESIZE_VGA // FRAMESIZE_QVGA;  // 320x240
  //   config.jpeg_quality = 5;
  //   config.fb_count = 1;
  // }

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Error initializing camera: 0x%x\n", err);
    return;
  }

  Serial.println("Camera initialized");
}

void loop() {
  unsigned long currentTime = millis();

  if (currentTime - lastCaptureTime >= captureInterval) {
    sendImage();
    lastCaptureTime = currentTime;
  }
}