---
version: '1.0'
description: Build OLED-menu multi-protocol 2.4GHz jammer based on RF Jammer architecture
name: rf-multi-protocol-jammer
license: MIT
metadata:
  hermes_origin: import
tags:
- rf-jammer
- nrf24
- esp32
- multi-protocol
- jammer
- constcarrier
- bluetooth-classic
- wifi-jamming
- ble-jamming
related_skills: []
---

# RF Jammer Style Multi-Protocol 2.4GHz Jammer

## 🎯 Trigger Conditions
- Building OLED-menu multi-protocol 2.4GHz jammer (WiFi/BLE/BT/VideoTX/RC/Zigbee/USB/nRF24)
- Based on cifertech/rf-jammer or  architecture
- ESP32 + 3×nRF24L01+PA+LNA on shared SPI bus
- Breadboard/high-R connections requiring bit-bang SPI with verified writes
- Need ShockBurst for WiFi/BLE, fast sweep for BT Classic, channel hopping for others

## 📂 Reference Architecture: cifertech/rf-jammer

### Hardware
- **MCU**: ESP32-D0WDQ6 (or S3/C3/C6/H2)
- **Radios**: 3× nRF24L01+PA+LNA
- **SPI**: Shared SCK=18, MISO=19, MOSI=23
- **CE/CSN**: Radio A: CE=5, CSN=17 | Radio B: CE=16, CSN=4 | Radio C: CE=14, CSN=13
- **OLED**: SSD1306 I2C (SDA/SCL per board)
- **Buttons**: 3× input-only GPIO (34/36/39) with 10kΩ pullups
- **NeoPixel**: GPIO 33 (moved from 14 to avoid CE_C conflict)

### Firmware Modes (8 protocols)

| Mode | Constant | Target | Method | Channels |
|------|----------|--------|--------|----------|
| WiFi | `WiFi_MODULE` | 802.11 b/g/n | constCarrier static 100% duty | ch 12, 37, 62 (WiFi 1/6/11) |
| BLE | `BLE_MODULE` | BLE advertising | constCarrier static 100% duty | ch 2, 26, 80 (adv 37/38/39) |
| BT Classic | `Bluetooth_MODULE` | BR/EDR 79ch | constCarrier + fast segmented sweep | A:2-27, B:28-53, C:54-80 |
| Video TX | `VIDEO_TX_MODULE` | Analog FPV | constCarrier + 3ms hop, ch+2/+4 offset | videoTransmitter_channels[] |
| RC | `RC_MODULE` | 2.4GHz RC | constCarrier + 3ms hop, ch+2/+4 offset | rc_channels[] |
| Zigbee | `ZIGBEE_MODULE` | 802.15.4 | constCarrier + 3ms hop, ch+2/+4 offset | zigbee_channels[] |
| USB Wireless | `USB_WIRELESS_MODULE` | Logitech/etc | constCarrier + 3ms hop, ch+2/+4 offset | usbWireless_channels[] |
| nRF24 | `NRF24_MODULE` | nRF24 links | constCarrier + 3ms hop, ch+2/+4 offset | nrf24_channels[] |

## ⚡ Core Technical Patterns

### 1. SoftNRF Bit-Bang Driver (Shared SPI)
All 3 radios share SCK/MOSI/MISO. Each has independent CE/CSN. Bit-bang delay per radio:
- Radio A/B (healthy): 10µs
- Radio C (high-R): 150µs

```cpp
SoftNRF::busInit();  // Once at boot
RadioA.beginPins(); RadioB.beginPins(); RadioC.beginPins();
```

### 2. startConstCarrier — The ONLY Working TX Method (ALL Modes)

**CRITICAL**: Pure ShockBurst TX fires ONE packet then stops (FIFO empties, TX_DS set, radio idle). Pure CW carrier (CONT_WAVE alone, no payload) does NOT trigger WiFi CCA backoff. The ONLY configuration that produces continuous effective interference is the RF24 library's `startConstCarrier()` pattern: **CONT_WAVE + PLL_LOCK + W_TX_PAYLOAD_NOACK + REUSE_TX_PL used together**.

See `references/nrf24-tx-mode-truth.md` for the full empirical analysis and verification data.

```cpp
void SoftNRF::startConstCarrier() {
  // 1) CONT_WAVE + PLL_LOCK in RF_SETUP (carrier stays on)
  writeRegChecked(RF_SETUP, 0x0F | 0x90);  // 2Mbps + PA max + LNA + CONT_WAVE + PLL_LOCK
  // 2) No auto-ack, no retries
  writeRegChecked(EN_AA, 0x00);
  writeRegChecked(SETUP_RETR, 0x00);
  // 3) TX_ADDR + RX_ADDR_P0 = 5 bytes 0xFF (spectrum-rich)
  // 4) PWR_UP=1, PRIM_RX=0, CRC off → CONFIG=0x02
  writeRegChecked(CONFIG, 0x02);
  delay(2);  // Tpd2stby >= 1.5ms
  // 5) FLUSH_TX → W_TX_PAYLOAD_NOACK (0xB0) with 32 bytes 0xFF
  // 6) CE HIGH → delay 1ms
  // 7) sendReuseTXPL(): CE LOW → clear MAX_RT → transfer(0xE3) → CE HIGH
}
```

**Expected register state after start**: RF_SETUP=**0x9F**, CONFIG=0x02, STATUS=0x0e. To verify TX is running: FIFO_STATUS should show **TX_FULL=1, TX_EMPTY=0** (FIFO has data, carrier active). If TX_EMPTY=1 and TX_DS=1, the radio fired one packet and stopped — startConstCarrier was not called or REUSE_TX_PL failed.

**ALL 8 modes now use startConstCarrier** — WiFi, BLE, BT, VideoTX, RC, Zigbee, nRF24, USB. The mode only changes which channels the radios sit on or sweep through. The TX mechanism is always constCarrier.

```cpp
// In initAllRadios() — same for ALL modes
RadioA.setChannelChecked(chA);
RadioB.setChannelChecked(chB);
RadioC.setChannelChecked(chC);
RadioA.startConstCarrier();
RadioB.startConstCarrier();
RadioC.startConstCarrier();
// Verify: RF_SETUP must be 0x9F on all 3 radios
```

### 3. Bluetooth Classic: Fast Segmented Sweep (constCarrier stays ON)
BT Classic hops 1600×/s over 79 channels with AFH. Slow 3ms hopping lets AFH map and avoid us. Solution: **parallel segmented sweep** at ~350µs/hop. CONT_WAVE carrier stays ON — only RF_CH changes (PLL re-locks ~130µs).

```cpp
// In jamLoop() - ONLY for Bluetooth_MODULE
static uint8_t swA = 2, swB = 28, swC = 54, cDiv = 0;
RadioA.setChannel(swA);           // A: 2-27 (every loop)
RadioB.setChannel(swB);           // B: 28-53 (every loop)
if (++cDiv >= 4) {                // C: 54-80 (1/4 rate due to 150µs delay)
  RadioC.setChannel(swC);
  swC = (swC >= 80) ? 54 : swC + 1;
  cDiv = 0;
}
swA = (swA >= 27) ? 2 : swA + 1;
swB = (swB >= 53) ? 28 : swB + 1;
```

**Coverage**: Full 2-80 sweep in ~9ms (vs BT's 625µs hop). AFH cannot adapt fast enough.

### 4. Other Sweep Modes: 3ms Channel Hop with Offsets
VideoTX/RC/Zigbee/nRF24/USB all sweep their channel tables at 3ms/hop with +2/+4 offsets. Carrier stays ON (CONT_WAVE) — only RF_CH changes.

```cpp
byte ch = channels[hopIndex % chCount];
hopIndex++;
RadioA.setChannel(ch);
RadioB.setChannel((ch + 2 <= 80) ? ch + 2 : ch);  // +2 offset
RadioC.setChannel((ch + 4 <= 80) ? ch + 4 : ch);  // +4 offset
```

### 5. stopConstCarrier + Periodic Health Check (Critical for High-R)
**stopConstCarrier**: Datasheet warns CONT_WAVE + REUSE_TX_PL together means CE LOW won't stop TX. Must `powerDown()` to release, then clear CONT_WAVE/PLL_LOCK bits, then FLUSH_TX.

```cpp
void SoftNRF::stopConstCarrier() {
  powerDown();                           // PWR_UP=0 — only way to release CE
  writeRegChecked(RF_SETUP, 0x0F);       // clear CONT_WAVE + PLL_LOCK
  // FLUSH_TX
}
```

**Runtime health check** (every 5s in main loop): If RF_SETUP != 0x9F on any radio, call `reloadP()` (FLUSH_TX → W_TX_PAYLOAD_NOACK 32B 0xFF → sendReuseTXPL). This re-arms continuous TX if high-R CSN glitches corrupted the config.

```cpp
// Every 5s, for ALL active modes (not just WiFi/BLE/BT)
for (auto* r : {&RadioA, &RadioB, &RadioC}) {
  if (r->readReg(0x06) != 0x9F) {  // expected: CONT_WAVE+PLL_LOCK+2Mbps+PA max
    r->reloadP();  // flush + reload payload + re-arm REUSE_TX_PL
  }
}
```

## 📡 nRF24 Channel ↔ Protocol Frequency Mapping

| Protocol | Freq (MHz) | nRF24 Channel |
|----------|------------|---------------|
| WiFi ch 1 | 2412 | **12** |
| WiFi ch 6 | 2437 | **37** |
| WiFi ch 11 | 2462 | **62** |
| BLE adv 37 | 2402 | **2** |
| BLE adv 38 | 2426 | **26** |
| BLE adv 39 | 2480 | **80** |
| BT Classic | 2402-2480 | **2-80** |
| Zigbee ch 11 | 2405 | **5** |
| Zigbee ch 26 | 2480 | **80** |

**Formula**: `nRF24_ch = freq_MHz - 2400`

## 🔧 Configuration Constants (config.h)

```cpp
// Pin definitions
#define NRF_CE_PIN_A    5
#define NRF_CSN_PIN_A   17
#define NRF_CE_PIN_B    16
#define NRF_CSN_PIN_B   4
#define NRF_CE_PIN_C    14
#define NRF_CSN_PIN_C   13

// SoftNRF delays (µs per bit)
#define NRF_DELAY_A     10
#define NRF_DELAY_B     10
#define NRF_DELAY_C     150

// NeoPixel (moved from GPIO 14 to avoid CE_C conflict)
#define NEOPIXEL_PIN    33

// Buttons (input-only GPIOs with 10kΩ pullups)
#define PIN_BTN_L       34
#define PIN_BTN_R       36
#define PIN_BTN_S       39
```

## 📋 Channel Tables (config.h)

```cpp
// WiFi: nRF24 channels for 1, 6, 11
const byte WiFi_channels[] = {12, 37, 62};

// BLE: advertising channels 37, 38, 39
const byte ble_channels[] = {2, 26, 80};

// Bluetooth Classic: all 79 channels (2-80)
const byte bluetooth_channels[] = {2,3,4,...,80};  // 79 entries

// Video TX (analog FPV bands)
const byte videoTransmitter_channels[] = {...};

// RC (FlySky, FrSky, etc.)
const byte rc_channels[] = {...};

// Zigbee (15.4 channels 11-26)
const byte zigbee_channels[] = {5,6,7,...,80};

// nRF24 native
const byte nrf24_channels[] = {2,3,...,80};

// USB Wireless (Logitech Unifying, etc.)
const byte usbWireless_channels[] = {...};
```

## 🚀 Boot Sequence

```cpp
void setup() {
  Serial.begin(115200);
  
  // 1. Park ALL radio pins FIRST (CSN HIGH, CE LOW)
  pinMode(NRF_CE_PIN_A, OUTPUT); digitalWrite(NRF_CE_PIN_A, LOW);
  pinMode(NRF_CSN_PIN_A, OUTPUT); digitalWrite(NRF_CSN_PIN_A, HIGH);
  // ... same for B, C
  
  // 2. Init shared SPI bus (bit-bang)
  SoftNRF::busInit();
  RadioA.beginPins(); RadioB.beginPins(); RadioC.beginPins();
  
  // 3. Verify all 3 radios present
  // 4. OLED init, button ISRs
  // 5. Disable ESP32 WiFi/BT (we use nRF24 for everything)
  esp_bt_controller_deinit();
  esp_wifi_stop(); esp_wifi_deinit(); esp_wifi_disconnect();
  
  // 6. Auto-activate after 3s (for remote testing)
  delay(3000);
  current = ACTIVE_MODE;
  initAllRadios();  // Calls startConstCarrier() on all 3 radios — starts jamming immediately
  // Verify: Serial.printf("A: RF_SETUP=0x%02x", RadioA.readReg(0x06)); // expect 0x9F
}
```

## 🎮 Button Controls
- **Left/Right**: Cycle through 8 modes
- **Select (OK)**: Toggle ACTIVE/STANDBY
- **Auto-activate**: 3s after boot (diagnostic mode)

## 🔄 jamLoop() Dispatch Logic

```cpp
void jamLoop() {
  // WiFi/BLE: static constCarrier - no hopping needed (set in initAllRadios)
  if (current_Mode == WiFi_MODULE || current_Mode == BLE_MODULE) return;
  
  // Bluetooth Classic: fast segmented sweep (constCarrier stays ON, only RF_CH changes)
  if (current_Mode == Bluetooth_MODULE) {
    // ... sweep A:2-27, B:28-53, C:54-80 at ~350µs/hop
    return;
  }
  
  // All other modes: 3ms hop with +2/+4 offsets (constCarrier stays ON)
  if (millis() - lastHop < 3) return;
  lastHop = millis();
  
  byte ch = channels[hopIndex++ % chCount];
  RadioA.setChannel(ch);
  RadioB.setChannel(min(ch + 2, 80));
  RadioC.setChannel(min(ch + 4, 80));
}
```

## ⚠️ Critical Pitfalls Learned

1. **GPIO 2 = CSN_C kills Radio C** — GPIO 2 has onboard LED + strapping function. Move CSN_C to GPIO 13, CE_C to GPIO 14.

2. **NeoPixel on GPIO 14 conflicts with CE_C** — Move NeoPixel to GPIO 33.

3. **Hardware SPI fails on high-R breadboard** — Nanosecond edges ring. Must use bit-bang with µs delays.

4. **Radio C needs 150µs delay** — 100µs still shows occasional register corruption during long FIFO loads.

5. **FIFO load (33 bytes) corrupts previous register writes** — CSN glitches during long transaction. Solution: verified writes (`writeRegChecked`) + periodic `reloadP()` if RF_SETUP drifts from 0x9F.

6. **BT Classic AFH defeats slow hopping** — Must sweep full band faster than AFH adaptation (~9ms full sweep).

7. **ShockBurst TX fires ONE packet then stops** ( empirically verified: STATUS TX_DS=1, FIFO TX_EMPTY=1, radio idle for 5s). DO NOT use `startShockBurst()` for interference — it looks like it works on a scope during the first 10ms but is actually a single shot. Use `startConstCarrier()` (CONT_WAVE + PLL_LOCK + W_TX_PAYLOAD_NOACK + REUSE_TX_PL) instead. See `references/nrf24-tx-mode-truth.md`.

8. **Pure CW carrier (CONT_WAVE without payload) does NOT trigger WiFi CCA** — CCA energy detect alone is insufficient; receivers also need preamble-like correlation. The RF24 library's `startConstCarrier()` combines CONT_WAVE with a loaded payload + REUSE_TX_PL, producing carrier modulated with packet data that triggers both CCA energy detect AND preamble correlation.

9. **CONT_WAVE + REUSE_TX_PL cannot be stopped by CE LOW** — Datasheet warns both set together makes CE unresponsive. Must `powerDown()` (PWR_UP=0) to release, then clear CONT_WAVE/PLL_LOCK bits + FLUSH_TX. This is why `stopConstCarrier()` calls `powerDown()` first.

10. **initAllRadios() must be called on mode switch** — checkMode() calls it when ACTIVE_MODE changes. setRadiosNeutralState() now calls `stopConstCarrier()` not `powerDown()` alone.

11. **REUSE_TX_PL (0xE3) is an SPI command, not a register write** — Must use `transfer(0xE3)` not `writeReg(0x1D, 0x04)`. The sequence is: CE LOW → clear MAX_RT (write STATUS 0x30) → transfer(0xE3) → CE HIGH.

## 📁 Project Structure

```
rf-jammer_fw/
├── src/
│   ├── main.cpp          # OLED, buttons, jamLoop, mode switching
│   ├── setting.cpp       # initAllRadios, SoftNRF instances, mode configs
│   ├── setting.h         # Radio declarations, mode enum
│   ├── softnrf.h         # Bit-bang driver class
│   ├── softnrf.cpp       # Implementation with verified writes
│   ├── config.h          # Pins, delays, channel tables
│   └── neopixel.cpp      # Status LED animations
├── test_radioC/          # Isolated Radio C diagnostics
└── platformio.ini
```

## 🛡️ Legal Notice
Taiwan Telecommunications Act Art 66/67: 2.4GHz jammer manufacture/possession/use illegal (fines 100-700萬 / 3-30萬). For **authorized research in Faraday cage only**.