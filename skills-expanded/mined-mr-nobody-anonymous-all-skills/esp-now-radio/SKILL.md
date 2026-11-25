---
name: esp-now-radio
description: "Use when building peer-to-peer wireless links between ESP32/ESP8266 boards (ESP-NOW) or between micro:bits (radio module) — robot remote controls, sensor swarms, telemetry without a router. Provides exact pairing/channel rules, payload limits, callback patterns, and the failure modes that silently break links."
category: robotics
domain: robotics
subdomain: general
version: 1.0.0
license: MIT
risk: low
source:
  repository: "rahulbachina/robotics-skills"
  commit: "e69d9828fb"
  imported_at: "2026-09-20"
  license: "MIT"
platforms:
  - claude-code
  - cursor
  - codex
  - gemini
  - antigravity
  - copilot
---


# ESP-NOW & micro:bit Radio — Router-less Peer-to-Peer Wireless

Two completely different protocols, same job: send small packets between boards with no Wi-Fi router, no pairing UI, no TCP stack. ESP-NOW runs on ESP32/ESP8266 (2.4 GHz Wi-Fi PHY, connectionless). micro:bit radio runs on the nRF51/nRF52 (proprietary 2.4 GHz, Nordic Gazell-like). They CANNOT talk to each other.

## Hard Numbers (memorize these)

| Property | ESP-NOW (ESP32) | micro:bit radio |
|---|---|---|
| Max payload | **250 bytes** (v1), 1470 bytes (v2, ESP-IDF 5.4+/both peers v2) | **251 bytes** MicroPython (default 32 — must raise it), 19 bytes per `radio.send_value` string in MakeCode |
| Addressing | 6-byte MAC, unicast or broadcast `FF:FF:FF:FF:FF:FF` | Group number 0–255 (it's a filter, not security) |
| Range, line of sight | ~100 m (up to 220 m with long-range mode) | ~70 m at power 7, ~20 m at default power 6 |
| Max registered peers | 20 total; 17 if encrypted (6 encrypted max on ESP8266) | n/a — everyone in the same group hears everything |
| Latency | 1–4 ms typical unicast | ~10 ms |
| ACK | Unicast: link-layer ACK (you get delivery status). Broadcast: **no ACK ever, status always "success"** | None. Fire and forget. Always. |
| Encryption | Optional PMK+LMK (16 bytes each), unicast only — **broadcast frames are never encrypted** | None. Anything sent is public. |
| Coexistence with Wi-Fi | Yes, but channel must match the AP's channel | n/a (radio and BLE are mutually exclusive on micro:bit) |

## ESP-NOW: The Five Rules That Prevent 90% of Failures

1. **`WiFi.mode(WIFI_STA)` before anything.** ESP-NOW rides on the Wi-Fi driver. No mode set → `esp_now_init()` fails or sends go nowhere. Do NOT call `WiFi.begin()` unless you actually want an AP connection.
2. **Both peers must be on the same channel.** Two idle ESP32s default to channel 1, so demos work. The moment one of them also connects to a router, it hops to the router's channel and the link dies *silently* (sender even reports success on broadcast). Fix: pin the channel explicitly on the non-router peer with `esp_wifi_set_channel()`, or read the connected peer's channel and match it.
3. **Use the STA MAC, not the AP MAC.** `WiFi.macAddress()` in STA mode is the address peers must register. The ESP32 has multiple MACs (STA, AP, BT); registering the wrong one = packets ignored.
4. **Register the peer before sending unicast.** `esp_now_send()` to an unregistered address returns `ESP_ERR_ESPNOW_NOT_FOUND`. Broadcast also requires registering `FF:FF:FF:FF:FF:FF` as a peer on ESP32 Arduino core 2.x+ (older tutorials skip this and break on current cores).
5. **Never do real work in the receive callback.** It runs in the Wi-Fi task (ESP32) / interrupt context. Copy the data to a buffer, set a `volatile` flag (or push to a FreeRTOS queue), return immediately. `Serial.print`, `delay()`, or I2C inside the callback = watchdog resets and dropped frames.

### Getting the MAC (do this first on every board)

```cpp
// Arduino C++ — print STA MAC
#include <WiFi.h>
void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  Serial.println(WiFi.macAddress());   // e.g. 24:6F:28:AE:1C:5C
}
```

```python
# MicroPython
import network, ubinascii
sta = network.WLAN(network.STA_IF); sta.active(True)
print(ubinascii.hexlify(sta.config('mac'), ':').decode())
```

Hardcode the receiver's MAC in the sender. There is no discovery protocol — if you need dynamic pairing, broadcast a "hello" and have peers register whoever they hear (the receive callback gives you the sender MAC).

### Minimal Correct Sender + Receiver (Arduino C++, ESP32 core 3.x)

Core 3.x changed the callback signatures — this is the #1 reason old tutorial code fails to compile.

```cpp
#include <esp_now.h>
#include <WiFi.h>

// Struct must be IDENTICAL (order, types, packing) on both ends. Keep ≤250 bytes.
typedef struct __attribute__((packed)) {
  int16_t x;        // joystick -512..511
  int16_t y;
  uint8_t buttons;  // bitmask
  uint32_t seq;     // detect dropped/duplicate packets
} ControlPacket;

uint8_t peerMac[] = {0x24, 0x6F, 0x28, 0xAE, 0x1C, 0x5C};
ControlPacket pkt;

// CORE 3.x signature (esp_now_send_cb_t changed):
void onSent(const wifi_tx_info_t *info, esp_now_send_status_t status) {
  // status == ESP_NOW_SEND_SUCCESS means the link-layer ACK arrived (unicast only)
}
// Core 2.x signature was: void onSent(const uint8_t *mac, esp_now_send_status_t status)

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  if (esp_now_init() != ESP_OK) { Serial.println("ESP-NOW init failed"); ESP.restart(); }
  esp_now_register_send_cb(onSent);

  esp_now_peer_info_t peer = {};          // ZERO-INITIALIZE. Garbage fields = ESP_ERR_ESPNOW_ARG
  memcpy(peer.peer_addr, peerMac, 6);
  peer.channel = 0;                        // 0 = "use current channel". Safest default.
  peer.encrypt = false;
  if (esp_now_add_peer(&peer) != ESP_OK) { Serial.println("add_peer failed"); }
}

void loop() {
  pkt.x = analogRead(34) - 2048;  // scale as needed
  pkt.y = analogRead(35) - 2048;
  pkt.seq++;
  esp_now_send(peerMac, (uint8_t*)&pkt, sizeof(pkt));
  delay(20);                       // 50 Hz. Don't exceed ~100 Hz, you'll flood the channel.
}
```

```cpp
// Receiver
#include <esp_now.h>
#include <WiFi.h>

typedef struct __attribute__((packed)) {
  int16_t x; int16_t y; uint8_t buttons; uint32_t seq;
} ControlPacket;

volatile ControlPacket latest;
volatile bool fresh = false;
volatile uint32_t lastRxMs = 0;

// CORE 3.x signature (gives sender MAC via info->src_addr):
void onRecv(const esp_now_recv_info_t *info, const uint8_t *data, int len) {
  if (len != sizeof(ControlPacket)) return;          // version-mismatch guard — ALWAYS check len
  memcpy((void*)&latest, data, sizeof(ControlPacket));
  fresh = true;
  lastRxMs = millis();
  // Do NOTHING else here. No Serial, no motors, no delay.
}
// Core 2.x signature was: void onRecv(const uint8_t *mac, const uint8_t *data, int len)

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  esp_now_init();
  esp_now_register_recv_cb(onRecv);
}

void loop() {
  if (fresh) {
    fresh = false;
    ControlPacket p; memcpy(&p, (const void*)&latest, sizeof(p));  // snapshot, avoid torn read
    driveMotors(p.x, p.y);
  }
  // FAILSAFE — mandatory for any robot: stop if the radio goes quiet
  if (millis() - lastRxMs > 300) stopMotors();
}
```

`__attribute__((packed))` matters: without it, struct padding can differ and `len != sizeof` checks or field offsets break between compiler versions. Better yet, keep fields naturally aligned (largest first) AND packed.

### MicroPython ESP-NOW (firmware 1.20+, `espnow` built in)

MicroPython's API is polling-or-IRQ, not Arduino-style callbacks. `recv()` is simpler and safer for robots.

```python
# Sender
import network, espnow, struct, time

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()                      # ESP8266: required to leave any saved AP; also stops channel hopping

e = espnow.ESPNow()
e.active(True)
PEER = b'\x24\x6f\x28\xae\x1c\x5c'    # raw 6 bytes, NOT a hex string
e.add_peer(PEER)

seq = 0
while True:
    x, y, buttons = read_joystick()
    seq += 1
    # '<' = little-endian, no padding — matches the packed C struct above
    payload = struct.pack('<hhBI', x, y, buttons, seq)
    try:
        e.send(PEER, payload, True)   # True = wait for ACK; returns False if no ACK
    except OSError as err:
        pass                          # ETIMEDOUT if peer gone; don't crash the loop
    time.sleep_ms(20)
```

```python
# Receiver with failsafe
import network, espnow, struct, time

sta = network.WLAN(network.STA_IF); sta.active(True); sta.disconnect()
e = espnow.ESPNow(); e.active(True)

last_rx = time.ticks_ms()
while True:
    host, msg = e.recv(50)            # timeout ms; returns (None, None) on timeout
    if msg and len(msg) == struct.calcsize('<hhBI'):
        x, y, buttons, seq = struct.unpack('<hhBI', msg)
        drive_motors(x, y)
        last_rx = time.ticks_ms()
    if time.ticks_diff(time.ticks_ms(), last_rx) > 300:
        stop_motors()
```

MicroPython gotchas:
- `e.send()` blocks up to ~2 s waiting for ACK if the peer is dead. Pass `sync=False` (`e.send(PEER, msg, False)`) in time-critical loops and check delivery separately.
- Internal RX buffer is 526 bytes by default; a fast sender overflows it and **old packets get dropped silently**. For robot control you WANT the newest packet: drain the buffer (`while e.any(): host, msg = e.recv(0)`) and use the last one.
- Broadcast: `e.add_peer(b'\xff'*6)` then send to that address. Receiving broadcast needs no peer registration.

### Broadcast vs Unicast — choose deliberately

| | Unicast | Broadcast |
|---|---|---|
| Delivery confirmation | Yes (link ACK → send callback status) | No — status is ALWAYS success even with zero receivers |
| Retries | Driver retries automatically | None |
| Encryption | Possible | Impossible |
| Use for | Remote control, anything needing reliability | Discovery/pairing, one-to-many telemetry, sync pulses |

For one-controller-many-robots, broadcast the control packet and put a robot-ID field in the payload; each robot filters in software. Cheaper than 20 unicast sends.

### Channel pinning when one peer uses Wi-Fi

```cpp
// On the peer that does NOT connect to the router:
#include <esp_wifi.h>
WiFi.mode(WIFI_STA);
esp_wifi_set_channel(6, WIFI_SECOND_CHAN_NONE);  // match the router's channel exactly
```
If the router channel-hops (auto channel), this breaks again. Robust option: the Wi-Fi-connected peer broadcasts its channel on all channels at boot, or just disable auto-channel on the router. There is no in-protocol channel negotiation.

### ESP8266 differences (older tutorials mix these up)

- Header is `espnow.h` not `esp_now.h`; functions return `0` for success not `ESP_OK`.
- Must call `esp_now_set_self_role(ESP_NOW_ROLE_COMBO)` after init.
- Receive callback: `void onRecv(uint8_t *mac, uint8_t *data, uint8_t len)`.
- ESP8266↔ESP32 interop works fine (v1 frames) as long as payload ≤250 bytes.

## micro:bit Radio

Completely separate world. Group number = channel filter, all members hear all messages, no addressing, no ACK, no encryption. **Enabling radio disables BLE** (and vice versa) — you cannot use the radio and a Bluetooth phone connection simultaneously.

### MicroPython (micro:bit)

```python
# Transmitter (controller)
from microbit import *
import radio, struct

radio.config(
    group=42,        # 0-255. Pick a random-ish number; every classroom uses 0 and 1.
    power=7,         # 0-7. 7 = ~+4 dBm ≈ 70 m LoS. 6 is the default.
    length=32,       # max payload bytes, up to 251. Default 32. RAISE THIS if sending more.
    channel=7,       # 0-83 → 2400+ch MHz. Group AND channel must both match!
    queue=3,         # RX queue depth (packets)
    data_rate=radio.RATE_1MBIT,  # 1 MBIT is most reliable; 2 MBIT shorter range
)
radio.on()           # radio is OFF until you call this — forgetting it = silent failure

while True:
    x = accelerometer.get_x()   # -1024..1024 tilt control
    y = accelerometer.get_y()
    radio.send_bytes(struct.pack('<hh', x, y))   # binary beats str for size+parse speed
    sleep(50)
```

```python
# Receiver (robot)
from microbit import *
import radio, struct, utime

radio.config(group=42, length=32, channel=7)
radio.on()

last_rx = utime.ticks_ms()
while True:
    msg = radio.receive_bytes()        # None if queue empty — non-blocking
    if msg and len(msg) == 4:
        x, y = struct.unpack('<hh', msg)
        drive(x, y)
        last_rx = utime.ticks_ms()
    if utime.ticks_diff(utime.ticks_ms(), last_rx) > 500:
        stop()                         # failsafe, same rule as ESP-NOW
    sleep(10)
```

micro:bit gotchas:
- `radio.receive()` (string version) **raises ValueError** if the incoming packet isn't the string-flavored format (e.g. sent by `send_bytes` or MakeCode `send number`). Mixing MakeCode and MicroPython senders/receivers requires matching packet formats — safest is `send_bytes`/`receive_bytes` everywhere, or in MakeCode stick to `radio.sendNumber`/`onReceivedNumber` on both ends.
- Group AND channel must both match. MakeCode only exposes group (it derives the channel); MicroPython exposes both. A MicroPython board with non-default `channel=` will never hear a MakeCode board.
- Default `length=32` silently truncates longer payloads. Set `length=` on BOTH ends.
- The RX `queue` overflows fast at high send rates; like ESP-NOW, drain it and act on the newest packet for control applications.
- Power 7 + fresh batteries matters: a micro:bit on a weak battery pack drops TX power and range collapses to a few meters before anything else visibly fails.
- V1 micro:bit has 16 KB RAM — `length=251` plus big buffers can OOM. Keep payloads small on V1.

## Designing the Payload (both platforms)

- **Binary structs, not strings/JSON.** `struct.pack('<hhBI', ...)` is 9 bytes; the JSON equivalent is ~50 and needs parsing on a microcontroller.
- **Include a sequence number.** Lets the receiver detect drops (gap) and stale/duplicate delivery (ESP-NOW retries can duplicate broadcast frames).
- **Include a magic byte or protocol version** as the first field. Then `if data[0] != 0xA7: return` rejects packets from someone else's project on the same channel/group.
- **Always validate `len` before unpacking.** Mismatched struct versions between sender and receiver is the most common "values are garbage" bug.
- **Failsafe timeout on the robot side is non-negotiable.** 300–500 ms of radio silence → motors off. Every runaway-robot incident traces back to skipping this.

## Debugging Checklist (in order)

1. **No packets at all (ESP-NOW):** Both in `WIFI_STA` mode? Same channel (`WiFi.channel()` on both)? Sender using receiver's *STA* MAC? Peer added (incl. broadcast address on core 3.x)? Send callback status — `SUCCESS` on unicast proves RF works, so the bug is in the receiver's callback registration; `FAIL` means channel/MAC/peer.
2. **No packets at all (micro:bit):** `radio.on()` called? Same group AND channel AND data_rate? String vs bytes API mismatch (check for ValueError)? Battery fresh?
3. **Works on bench, dies in the field:** one ESP later joined Wi-Fi and channel-hopped (rule 2); or 2.4 GHz congestion — move ESP-NOW channel / micro:bit channel away from busy Wi-Fi (Wi-Fi ch 1/6/11 ≈ micro:bit radio channels 0-22 / 25-47 / 50-72; pick gaps like micro:bit channel 23-24 or 78+).
4. **Garbage values:** struct mismatch — compare `sizeof`/`struct.calcsize` on both ends; check packing/endianness (`__attribute__((packed))` + `'<'`).
5. **Receiver resets/WDT (ESP32):** heavy work in the RX callback. Move it out.
6. **Laggy/jerky control:** RX queue backlog — drain to newest; or sender flooding (>100 Hz); or `e.send(..., True)` blocking on a dead peer.
7. **Range terrible:** antenna orientation (PCB antennas are directional-ish — keep them parallel); metal chassis shadowing the antenna; micro:bit power level / battery; ESP32 boards with on-board antenna near ground planes. For ESP32 long range: `esp_wifi_set_protocol(WIFI_IF_STA, WIFI_PROTOCOL_LR)` on BOTH ends (ESP32-to-ESP32 only, drops rate to 250 kbps, roughly doubles range).
8. **Intermittent on USB power only:** brownout — Wi-Fi TX bursts pull 300+ mA spikes; weak USB cable/port causes resets logged as `Brownout detector was triggered`. Add a 470 µF cap across 3V3/5V or use a better supply.

## Security Reality Check

- micro:bit radio group numbers are NOT security — anyone can set the same group and inject packets. Fine for classrooms, never for anything that matters.
- ESP-NOW unencrypted frames can be sniffed and replayed by any ESP32 in promiscuous mode. If a student project controls anything with mass or heat, at minimum use the magic-byte + sequence check; for real protection use encrypted peers (set PMK with `esp_now_set_pmk()`, per-peer LMK, `peer.encrypt = true`) — but remember broadcast can never be encrypted and encrypted peers cap at 6 (ESP8266) / 17 (ESP32).
