---
version: '1.0'
description: Bit-bang SPI driver for nRF24L01+ on ESP32 with verified writes, ShockBurst
  mode, and auto-repair for high-resistance breadboard connections. Solves SPI signal
  integrity issues on Dupont-wired nRF24 modules where hardware SPI fails due to nanosecond
  edge ringing.
name: nrf24-bitbang-spi
license: MIT
metadata:
  hermes_origin: import
tags:
- nrf24
- esp32
- bit-bang
- spi
- shockburst
- wireless-jamming
related_skills: []
---

# nRF24L01+ Bit-Bang SPI Driver with Verified Writes & Auto-Repair

## 🎯 Trigger Conditions
- nRF24 modules on breadboard with Dupont wires showing SPI corruption (STATUS 0x00/0xFF, register reads corrupted)
- Hardware SPI works on healthy connections but fails on high-resistance contacts
- Need continuous ShockBurst (max-length packet flood) for WiFi/Bluetooth interference
- Long-running firmware needs periodic health checks and self-repair

## 📋 Problem Context
Hardware SPI on ESP32 uses ~10-50ns edge rates. On breadboard with Dupont wires, contact resistance creates RC filters that round edges, causing bit errors. Bit-banging with configurable µs delays provides clean edges that pass through high-R connections.

**Proven thresholds (Radio C = high-R branch):**
- HW SPI 50kHz: **dead** (MISO stuck 0x00)
- Bit-bang 2kHz (500µs): **alive**, 0/20 errors
- Bit-bang 20kHz (50µs): **alive**, 0/20 errors but marginal  
- Bit-bang 40kHz (25µs): **occasional errors**
- Bit-bang 100kHz (10µs): **frequent errors**
- **Stable: 150µs delay (~6.6 kHz)** for high-R; 10µs for healthy branches

## 🏗️ Architecture

### Class Interface
```cpp
class SoftNRF {
public:
  SoftNRF(uint8_t cePin, uint8_t csnPin, uint16_t delayUs);
  
  static void busInit();           // Call ONCE at boot: SCK/MOSI outputs LOW, MISO input
  void beginPins();                // CE output LOW, CSN output HIGH
  bool isPresent();                // STATUS sanity: not 0x00 / not 0xFF = alive
  void configureTx();              // Power-up, TX, no CRC/ACK, 2Mbps, PA max
  void setChannel(uint8_t ch);     // Fast path (no verification)
  void setChannelChecked(uint8_t); // Verified write (for init)
  void carrierOn();                // CONT_WAVE + PLL_LOCK, CE HIGH
  void carrierOff();               // CE LOW, clear carrier bits
  void powerDown();                // Full power down
  
  // constCarrier mode — CONT_WAVE + REUSE_TX_PL = continuous carrier+payload flood
  // This is the ONLY working TX method for interference. See rf-jammer-multi-protocol-jammer/references/nrf24-tx-mode-truth.md
  void startConstCarrier();       // RF_SETUP=0x9F, load payload, REUSE_TX_PL
  void stopConstCarrier();        // powerDown + clear CONT_WAVE + FLUSH_TX
  void sendReuseTXPL();           // CE LOW → clear MAX_RT → transfer(0xE3) → CE HIGH
  void reloadP();                 // FLUSH_TX → W_TX_PAYLOAD_NOACK → sendReuseTXPL
  
  // Legacy ShockBurst mode — DO NOT USE for interference (fires 1 packet then stops)
  void startShockBurst();          // [DEPRECATED] Single-packet TX, not continuous
  void repairShockBurstConfig();   // [DEPRECATED] Use reloadP() with constCarrier instead
  
  uint8_t readReg(uint8_t reg);    // Verification helper

private:
  uint8_t transfer(uint8_t out);
  void writeReg(uint8_t reg, uint8_t val);
  bool writeRegChecked(uint8_t reg, uint8_t val);  // Write + read-back verify (4 retries)
  
  uint8_t _ce, _csn;
  uint16_t _d;  // per-bit delay in microseconds
};
```

## ⚡ Critical Implementation Patterns

### 1. Bus Initialization (Single Call)
```cpp
void SoftNRF::busInit() {
  pinMode(18, OUTPUT); digitalWrite(18, LOW);  // SCK
  pinMode(23, OUTPUT); digitalWrite(23, LOW);  // MOSI
  pinMode(19, INPUT);                          // MISO
}
```

### 2. Bit-Bang Transfer (Mode 0, MSB First)
```cpp
uint8_t SoftNRF::transfer(uint8_t out) {
  uint8_t in = 0;
  for (int i = 0; i < 8; i++) {
    digitalWrite(23, (out & 0x80) ? HIGH : LOW);  // MOSI
    out <<= 1;
    delayMicroseconds(_d);
    digitalWrite(18, HIGH);        // SCK rising
    delayMicroseconds(_d);
    in = (in << 1) | digitalRead(19);  // MISO
    digitalWrite(18, LOW);         // SCK falling
    delayMicroseconds(_d);
  }
  return in;
}
```

### 3. Verified Write with Retry (Core Reliability Pattern)
```cpp
bool SoftNRF::writeRegChecked(uint8_t reg, uint8_t val) {
  for (int attempt = 0; attempt < 4; attempt++) {
    writeReg(reg, val);
    if (readReg(reg) == val) return true;
  }
  return false;
}
```

### 4. ⚠️ startConstCarrier — The ONLY Working Continuous TX Method

**Pure ShockBurst TX fires ONE packet then stops** (empirically verified: TX_DS=1, FIFO TX_EMPTY=1, radio idle for 5+ seconds). Pure CW (CONT_WAVE without payload) does NOT trigger WiFi CCA. The ONLY method that produces continuous interference is the RF24 library's startConstCarrier pattern: CONT_WAVE + PLL_LOCK + W_TX_PAYLOAD_NOACK + REUSE_TX_PL.

Full analysis + verification data: see `rf-jammer-multi-protocol-jammer/references/nrf24-tx-mode-truth.md`

```cpp
void SoftNRF::startConstCarrier() {
  // RF_SETUP |= CONT_WAVE(bit7) + PLL_LOCK(bit4) = 0x90
  writeRegChecked(RF_SETUP, 0x0F | 0x90);  // = 0x9F
  writeRegChecked(EN_AA, 0x00);
  writeRegChecked(SETUP_RETR, 0x00);
  // TX_ADDR + RX_ADDR_P0 = 5 bytes 0xFF
  // CONFIG = 0x02 (PWR_UP, TX, CRC off)
  writeRegChecked(CONFIG, 0x02);
  delay(2);  // Tpd2stby >= 1.5ms
  // FLUSH_TX → W_TX_PAYLOAD_NOACK (0xB0) with 32 bytes 0xFF
  digitalWrite(_ce, HIGH);
  delay(1);
  // sendReuseTXPL(): CE LOW → STATUS clear → transfer(0xE3) → CE HIGH
}
// Expected RF_SETUP after start = 0x9F. FIFO shows TX_FULL=1, TX_EMPTY=0.
// If TX_EMPTY=1 → radio stopped. Call reloadP() to re-arm.
```

### 5. stopConstCarrier — Cannot Stop with CE LOW
Datasheet: CONT_WAVE + REUSE_TX_PL together → CE LOW doesn't stop TX. Must powerDown:
```cpp
void SoftNRF::stopConstCarrier() {
  powerDown();                         // PWR_UP=0 — only way to release
  writeRegChecked(RF_SETUP, 0x0F);     // clear CONT_WAVE + PLL_LOCK
  // FLUSH_TX
}
```

### 6. Periodic Health Check: reloadP()
```cpp
void SoftNRF::reloadP() {
  // FLUSH_TX → W_TX_PAYLOAD_NOACK 32×0xFF → sendReuseTXPL()
}
// Runtime: every 5s, if RF_SETUP != 0x9F → call reloadP()
```

### 7. [DEPRECATED] startShockBurst — Single-Packet TX (DO NOT USE for interference)
```cpp
void SoftNRF::startShockBurst() {
  writeRegChecked(EN_AA, 0x00);        // Auto-ack off
  writeRegChecked(SETUP_RETR, 0x00);   // No retries
  writeRegChecked(RF_SETUP, 0x0F);     // 2Mbps, PA max, LNA
  writeReg(STATUS, 0x70);              // Clear IRQ (not verifiable)
  writeRegChecked(CONFIG, 0x02);       // PWR_UP=1, PRIM_RX=0, CRC off
  delay(2);                            // Tpd2stby ≥ 1.5ms
  
  // TX address + payload width
  writeRegChecked(TX_ADDR, 0xE7);
  writeRegChecked(RX_ADDR_P0, 0xE7);
  writeRegChecked(RX_PW_P0, 32);
  
  // Fill TX FIFO with 32 bytes of 0xAA
  digitalWrite(_csn, LOW);
  delayMicroseconds(_d * 2);
  transfer(0xA0);  // W_TX_PAYLOAD
  for (int i = 0; i < 32; i++) transfer(0xAA);
  digitalWrite(_csn, HIGH);
  delayMicroseconds(_d * 2);
  
  // Dynamic payload + re-use TX payload (continuous re-transmit)
  writeRegChecked(FEATURE, 0x01);   // EN_DYN_ACK
  writeRegChecked(DYNPD, 0x01);     // DPL on pipe 0
  
  digitalWrite(_ce, HIGH);          // Continuous TX
}
```

### 5. Repair Pass (Fixes FIFO-Load Corruption)
Long 33-byte FIFO load on high-R CSN line glitches previously-written registers. Repair rewrites all critical config with CE low:

```cpp
void SoftNRF::repairShockBurstConfig() {
  digitalWrite(_ce, LOW);
  writeRegChecked(CONFIG, 0x02);
  delay(2);
  writeRegChecked(EN_AA, 0x00);
  writeRegChecked(SETUP_RETR, 0x00);
  writeRegChecked(RF_SETUP, SNRF_RF_SETUP_BASE);
  writeRegChecked(RX_PW_P0, 32);
  writeRegChecked(FEATURE, 0x01);
  writeRegChecked(DYNPD, 0x01);
  digitalWrite(_ce, HIGH);
}
```

## 🔄 Runtime Usage Pattern

### Boot Sequence
```cpp
SoftNRF RadioA(5, 17, 10);   // Healthy: 10µs
SoftNRF RadioB(16, 4, 10);   // Healthy: 10µs
SoftNRF RadioC(14, 13, 150); // High-R: 150µs

void setup() {
  SoftNRF::busInit();
  RadioA.beginPins(); RadioB.beginPins(); RadioC.beginPins();
  
  RadioA.configureTx(); RadioB.configureTx(); RadioC.configureTx();
  RadioA.setChannelChecked(12); RadioB.setChannelChecked(37); RadioC.setChannelChecked(62);
  
  // Use constCarrier — NOT startShockBurst (which fires 1 packet and stops)
  RadioA.startConstCarrier();
  RadioB.startConstCarrier();
  RadioC.startConstCarrier();
  
  // Verify: RF_SETUP must be 0x9F on all 3 radios
  // If any != 0x9F → call reloadP()
}
```

### Periodic Health Check (Every 5s)
```cpp
if (millis() - lastReport >= 5000) {
  for (auto* r : {&RadioA, &RadioB, &RadioC}) {
    uint8_t rf = r->readReg(0x06);
    if (rf != 0x9F) {  // Expected: CONT_WAVE + PLL_LOCK + 2Mbps + PA max
      r->reloadP();   // FLUSH_TX → reload payload → re-arm REUSE_TX_PL
    }
  }
}
```

## 📡 TX Mode Comparison for 2.4GHz Interference

| Aspect | Pure CW (CONT_WAVE only) | ShockBurst TX | **constCarrier** (CONT_WAVE + REUSE_TX_PL) |
|--------|--------------------------|---------------|---------------------------------------------|
| Signal | Single tone, no modulation | 32-byte packet, fire ONCE then stop | Continuous carrier modulated with payload data |
| Duration | Continuous (until CE/PWR down) | **Single packet** (~10µs at 2Mbps) | Continuous (until powerDown) |
| WiFi CCA Trigger | Energy detect only (often insufficient) | Brief, then gone | **Energy detect + preamble correlation** (persistent) |
| BT/BLE Impact | Minimal — no preamble | Minimal — one packet | **Effective — continuous modulated flood** |
| FIFO State | Empty (no payload) | Empty after 1 TX | TX_FULL=1 (always has data via REUSE_TX_PL) |
| How to Stop | CE LOW | CE LOW (auto-stops after packet) | **powerDown() only** (CE won't respond) |

**Result**: constCarrier is the ONLY working method. Verified empirically — see `rf-jammer-multi-protocol-jammer/references/nrf24-tx-mode-truth.md` for STATUS/FIFO observation data.

## 🔑 Key Register Map

| Register | Addr | ShockBurst Value | Purpose |
|----------|------|------------------|---------|
| CONFIG | 0x00 | 0x02 | PWR_UP=1, PRIM_RX=0, CRC off |
| EN_AA | 0x01 | 0x00 | Auto-ack disabled |
| EN_RXADDR | 0x02 | 0x01 | Pipe 0 only |
| SETUP_RETR | 0x04 | 0x00 | No retries |
| RF_CH | 0x05 | varies | Channel (0-125) |
| RF_SETUP | 0x06 | 0x0F | 2Mbps, PA max, LNA on |
| STATUS | 0x07 | read-only | FIFO status, IRQ flags |
| TX_ADDR | 0x10 | 0xE7... | TX address |
| RX_ADDR_P0 | 0x0A | 0xE7... | RX pipe 0 address |
| RX_PW_P0 | 0x11 | 32 | Max payload |
| DYNPD | 0x1C | 0x01 | Dynamic payload pipe 0 |
| FEATURE | 0x1D | 0x01 | EN_DYN_ACK |

## 📐 nRF24 Channel → Frequency Mapping
**nRF24 channel N = 2400 + N MHz**

| Protocol | Frequency | nRF24 Channel |
|----------|-----------|---------------|
| WiFi ch 1 | 2412 MHz | **12** |
| WiFi ch 6 | 2437 MHz | **37** |
| WiFi ch 11 | 2462 MHz | **62** |
| BLE adv 37 | 2402 MHz | **2** |
| BLE adv 38 | 2426 MHz | **26** |
| BLE adv 39 | 2480 MHz | **80** |
| BT Classic | 2402-2480 MHz | **2-80** |

## 🐛 Debugging Cheatsheet

| Symptom | Cause | Fix |
|---------|-------|-----|
| STATUS = 0x00 or 0xFF | SPI not communicating | Check wiring, power, CSN pin |
| RF_SETUP reads 0x62 not 0x0F | Write corruption during FIFO load | Use repair pass |
| FEATURE reads 0x00 | EN_DYN_ACK not set | Verify writeRegChecked in startShockBurst |
| Works on boot, drifts later | No periodic health check | Add 5s verify + repair loop |
| Radio C fails, A/B OK | High-R breadboard contact | Increase delayUs to 150µs |

## 🚀 Performance
- **Bit-bang rate**: ~6.6 kHz (150µs delay) on high-R; ~100 kHz (10µs) on healthy
- **Channel hop**: Single `setChannel()` = 1 register write = ~130µs PLL re-lock
- **ShockBurst throughput**: Continuous 32-byte packets at 2Mbps
- **Memory**: ~2KB flash, ~200 bytes RAM per radio instance

## ⚖️ Legal Notice
Taiwan Telecommunications Act Art 66/67: Manufacturing, possessing, or using 2.4GHz jammers is illegal (NCC confiscation + fines 100-700万; possession/use 3-30万). This driver is for **authorized research in Faraday cage environments only**.