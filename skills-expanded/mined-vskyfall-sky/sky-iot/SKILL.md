---
name: sky-iot
description: >-
  IoT ve gömülü projeler: ESP32/ESP8266, Arduino, Raspberry Pi, Raspberry Pi Pico seçimi;
  PlatformIO / Arduino IDE / ESP-IDF / MicroPython, sensörler ve aktüatörler (I2C, SPI, UART,
  GPIO, ADC), güç ve uyku modları, Wi-Fi ve BLE, MQTT ile bulut/sunucu iletişimi, web paneli
  ve gerçek zamanlı grafik, OTA güncelleme, cihaz güvenliği, veri kaydı (zaman serisi), prototipten
  ürüne ve TÜBİTAK/okul projeleri için pratik tavsiyeler. Donanım, sensör, ESP32, Arduino,
  "akıllı ev", "IoT" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · IoT & Gömülü

## Kart seçimi

| İhtiyaç | Kart |
|---|---|
| Wi-Fi/BLE, düşük maliyet, sensör + bulut | **ESP32** (S3: daha çok RAM/USB, C3/C6: ucuz/düşük güç) |
| Basit, öğrenme, çok kütüphane | Arduino Uno/Nano (Wi-Fi yok) |
| Linux, kamera, görüntü işleme, Python, sunucu | **Raspberry Pi** (4/5, Zero 2 W) |
| MicroPython, düşük maliyet, PIO | Raspberry Pi Pico (W: Wi-Fi) |

## Geliştirme ortamı

**PlatformIO** (VS Code — kütüphane yönetimi, çoklu kart, test) önerilir; Arduino IDE hızlı başlangıç; ESP-IDF (resmi, FreeRTOS, ileri); MicroPython/CircuitPython (hızlı prototip, Python bilenler için).

## Donanım temelleri

- Mantık seviyesi: ESP32 **3.3V** — 5V sensörü doğrudan bağlama (seviye dönüştürücü).
- I2C (çoklu sensör, 2 kablo, adres çakışmasına dikkat), SPI (hızlı: ekran, SD), UART (GPS, seri modüller), ADC (analog — ESP32 ADC doğrusal değil, kalibre et), PWM (servo, LED).
- Röle/motor için ayrı güç, ortak GND, flyback diyot, sürücü kartı; doğrudan GPIO'dan yük çekme.
- Kararlı güç: dalgalanan besleme rastgele resetlerin 1 numaralı sebebi.

## Yazılım kalıpları

```cpp
// PlatformIO + Arduino çerçevesi (ESP32): bloklamayan döngü
unsigned long lastRead = 0;
void loop() {
  mqtt.loop();                                    // bağlantıyı canlı tut
  if (millis() - lastRead >= 10000) {             // delay() yerine zamanlayıcı
    lastRead = millis();
    float t = sht.readTemperature();
    if (!isnan(t)) mqtt.publish("sky/sera1/sicaklik", String(t, 1).c_str(), true);
  }
}
```
`delay()` yerine `millis()` zamanlayıcıları veya FreeRTOS görevleri; Wi-Fi/MQTT kopunca **yeniden bağlanma** döngüsü; watchdog; sensör okuma hatalarını (NaN) ele al.

## İletişim

- **MQTT** (hafif yayınla/abone ol): broker Mosquitto (kendi sunucun) / EMQX / HiveMQ Cloud; konu yapısı `proje/cihaz/ölçüm`, retained mesajlar son değer için, QoS 1 önemli veride, TLS + kullanıcı/şifre veya istemci sertifikası.
- HTTP(S) REST: seyrek veri gönderimi için basit.
- BLE: telefon uygulamasıyla yakın iletişim (Web Bluetooth ile tarayıcıdan bile — bkz. `sky-browser-apis`).
- ESP-NOW: cihazlar arası Wi-Fi'sız iletişim.

## Panel ve veri

Sunucu: MQTT → Node/Python abonesi → zaman serisi DB (TimescaleDB/InfluxDB/SQLite) → web paneli (canlı grafik WebSocket/SSE — bkz. `sky-realtime`, `sky-dataviz`); hızlı çözümler: Node-RED, Home Assistant, Grafana. Alarmlar: eşik aşılınca Telegram botu (bkz. `sky-bots`) — insanların en sevdiği özellik.

## OTA ve güvenlik

ArduinoOTA / ESP-IDF OTA / HTTPS OTA (imzalı firmware, geri dönüşlü bölümler); varsayılan parolaları değiştir, Wi-Fi bilgilerini koda gömme (WiFiManager ile kurulum portalı veya NVS), MQTT'de TLS, cihaz başına kimlik, fiziksel erişim riskini düşün.

## Güç

Pil projelerinde deep sleep (ESP32 µA seviyesi), ölçüm → gönder → uyu döngüsü, Wi-Fi bağlantı süresini kısalt (statik IP), pil gerilimini ADC ile izle.

## Okul / TÜBİTAK projeleri için

Problem → hipotez → prototip → ölçüm → sonuç zinciri; ölçümleri **kaydet** (CSV/DB) ve grafiğe dök (bkz. `sky-data-analysis`); devre şeması (Fritzing/KiCad), malzeme listesi ve maliyet tablosu, tekrarlanabilir kurulum (kod GitHub'da, README), güvenlik önlemleri (şebeke gerilimiyle çalışma yok), poster/rapor için net grafikler.
