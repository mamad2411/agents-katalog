---
version: '1.0'
description: Fast segmented sweep technique for Bluetooth Classic (BR/EDR) jamming
  using nRF24L01+ with ShockBurst. Overcomes AFH by sweeping all 79 channels continuously
  at ~350µs/hop, preventing adaptive frequency hopping from avoiding jammed channels.
name: bluetooth-jammer-sweep
license: MIT
metadata:
  hermes_origin: import
tags:
- bluetooth-classic
- nrf24
- afh
- frequency-hopping
- jammer
- shockburst
related_skills: []
---

# Bluetooth Classic Segmented Sweep Jamming

## 🎯 Trigger Conditions
- Jamming Bluetooth Classic (BR/EDR) devices (headphones, speakers, keyboards)
- Need to overcome Adaptive Frequency Hopping (AFH)
- Using nRF24L01+ with ShockBurst continuous packet mode
- Multiple nRF24 radios available (2-3) for parallel sweeping

## 📋 Problem: Why Standard Hopping Fails Against BT Classic

Bluetooth Classic hops at **1600 hops/sec** across 79 channels (1 MHz spacing, 2402-2480 MHz). AFH monitors channel quality and marks bad channels as "unused" — the hop sequence skips them.

| Approach | Hop Rate | AFH Reaction | Result |
|----------|----------|--------------|--------|
| 3ms/hop (333 hops/s) | Too slow | AFH maps bad channels in ~2s | ❌ AFH avoids you |
| 1ms/hop (1000 hops/s) | Marginal | AFH still adapts | ❌ |
| **Continuous sweep (~350µs/hop, ~2850 hops/s)** | **Faster than AFH eval** | **No time to classify** | ✅ **Overwhelms AFH** |

## ⚡ Solution: Segmented Parallel Sweep

Divide 79 channels across 3 radios, sweep continuously:

```
Radio A: channels  2-27  (26 ch)  →  ~350µs/ch = ~9ms full cycle
Radio B: channels 28-53  (26 ch)  →  ~350µs/ch = ~9ms full cycle
Radio C: channels 54-80  (27 ch)  →  ~1400µs/ch (bit-bang slow) = ~38ms, runs at 1/4 rate
```

**All channels covered every ~9ms** — AFH needs ~2000ms to build channel map. By the time it marks one channel bad, you've already moved to the next.

## 🔧 Implementation (Arduino/ESP32)

### Channel Sweep in Main Loop (no delay!)

```cpp
void jamLoop() {
  // WiFi + BLE use static carriers — no hopping
  if (current_Mode == WiFi_MODULE || current_Mode == BLE_MODULE) return;

  // *** BLUETOOTH CLASSIC: FAST SEGMENTED SWEEP ***
  if (current_Mode == Bluetooth_MODULE) {
    static uint8_t swA = 2, swB = 28, swC = 54, cDiv = 0;
    
    // Radio A: 2-27
    RadioA.setChannel(swA);
    swA = (swA >= 27) ? 2 : swA + 1;
    
    // Radio B: 28-53
    RadioB.setChannel(swB);
    swB = (swB >= 53) ? 28 : swB + 1;
    
    // Radio C: 54-80 at 1/4 rate (bit-bang 150µs = 3.2ms/write)
    if (++cDiv >= 4) {
      RadioC.setChannel(swC);
      swC = (swC >= 80) ? 54 : swC + 1;
      cDiv = 0;
    }
    return;
  }

  // Other modes: standard 3ms hop with ch+2/+4 offset
  if (millis() - lastHop < 3) return;
  lastHop = millis();
  // ... standard hop logic ...
}
```

### ShockBurst Configuration (in initAllRadios)
```cpp
case Bluetooth_MODULE:
  // ShockBurst continuous packets + fast segmented sweep
  chA = 2; chB = 28; chC = 78;  // Starting points
  useShockBurst = true;
  break;
```

### Timing Analysis

| Radio | Channels | Delay per write | Rate | Cycle time |
|-------|----------|-----------------|------|------------|
| A (10µs) | 26 | ~20µs (2 reg writes) | ~50 kHz | ~9ms |
| B (10µs) | 26 | ~20µs | ~50 kHz | ~9ms |
| C (150µs) | 27 | ~300µs | ~3.3 kHz | ~38ms (1/4 rate) |

**Effective coverage**: All 79 channels hit every ~9ms (A/B) or ~38ms (C). AFH evaluation window is typically 2000ms+. **You win by 200x speed advantage.**

## 📊 ShockBurst vs Pure CW for BT Classic

| Metric | Pure CW | ShockBurst |
|--------|---------|------------|
| Signal type | Single tone | 32-byte packets @ 2Mbps |
| BT receiver sees | Interferer | Valid-looking GFSK packets |
| AFH classification | "Bad channel" (energy) | "Bad channel" + **CRC errors on valid packets** |
| Link layer reaction | May reduce power | **Supervision timeout triggers** |

**Key insight**: BT Classic expects GFSK packets. ShockBurst packets look like valid traffic but with wrong access code → CRC failure → link quality drops → supervision timeout → disconnect.

## 🛡️ AFH Evasion Countermeasures

The segmented sweep inherently defeats AFH because:
1. **Speed**: Channel map updates can't keep up
2. **Breadth**: You hit ALL channels, not just a subset
3. **Persistence**: Even if AFH marks some channels "bad", the remaining "good" channels still get hit
4. **ShockBurst**: Forces CRC failures on "good" channels too

## 🔌 Hardware Requirements
- 3× nRF24L01+PA+LNA
- Shared SPI bus (SCK=18, MOSI=23, MISO=19)
- Independent CE/CSN per radio
- Radio C on high-R branch → 150µs bit-bang delay
- External 3.3V supply (AMS1117) for PA+LNA peak current

## 📡 Channel Mapping Reference

```
Bluetooth Classic channel N = 2402 + N MHz
nRF24 channel = Bluetooth channel (direct mapping: ch 2-80)

nRF24 channels 2-80 cover full BT Classic range
```

## ⚖️ Legal Notice
Taiwan Telecommunications Act Art 66/67: Manufacturing, possessing, or using 2.4GHz jammers is illegal (NCC confiscation + fines 100-700萬; possession/use 3-30萬). This technique is for **authorized research in Faraday cage environments only**.