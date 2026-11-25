---
name: ble-mqtt-wifi
description: "Use when writing robot communication code: BLE GATT control links, MQTT fleet telemetry, WiFi connection management, or provisioning on ESP32/Pico W/Raspberry Pi. Provides exact UUIDs, MTU/timing numbers, QoS selection rules, LWT offline detection, reconnect state machines, captive portal provisioning, and BLE+WiFi coexistence constraints so generated code works first try."
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


# Robot Comms: BLE GATT, MQTT Fleets, WiFi State Machines

Scope: ESP32 (Arduino C++ / ESP-IDF concepts), Raspberry Pi Pico W (MicroPython), Raspberry Pi / Linux (Python, paho-mqtt), with notes for ROS2 bridging. Everything here is battle-tested numbers and patterns — copy them, don't improvise.

---

## 1. Choosing the Link (decide BEFORE writing code)

| Requirement | Use | Why |
|---|---|---|
| Phone → single robot, <30 m, low latency teleop | BLE GATT (NUS pattern) | No infra needed, 15–50 ms latency, pairing-free possible |
| Many robots ↔ server, telemetry + commands | MQTT over WiFi | Broker fans out, LWT gives free offline detection |
| Robot ↔ robot on same LAN, high rate (>50 Hz) | UDP or ROS2/DDS | MQTT broker adds 5–20 ms hop; BLE caps ~20–100 Hz usable |
| Field provisioning (no keyboard/screen) | BLE provisioning or captive portal AP | See §6 |
| Video | Never BLE, never MQTT | BLE ~1.4 Mbps max practical; MQTT brokers choke on >256 KB payloads. Use RTSP/WebRTC over WiFi |

Hard numbers to design against:
- BLE 4.2/5 practical throughput with DLE + 247-byte MTU: ~700–1400 kbps. Without MTU negotiation (default MTU 23): **20 bytes usable per notification** — this is the #1 cause of "my BLE data is truncated".
- BLE connection interval: 7.5 ms min, 4 s max. iOS will NOT honor <15 ms; iOS typically grants 30 ms. Android grants 7.5–15 ms with `CONNECTION_PRIORITY_HIGH`.
- MQTT over WiFi round trip (LAN broker): 5–30 ms. Cloud broker: 50–300 ms. Do NOT close a control loop through a cloud broker.
- WiFi STA reconnect after AP reboot: 2–8 s typical on ESP32. Your robot must stay safe (motors stopped) during this window.

---

## 2. BLE GATT Robot Control — the NUS UART Pattern

Use the Nordic UART Service (NUS) UUIDs. Every BLE terminal app (nRF Connect, Serial Bluetooth Terminal, Adafruit Bluefruit) speaks it, so you get a free debug console.

```
Service: 6E400001-B5A3-F393-E0A9-E50E24DCCA9E
RX char (phone→robot, Write / Write-No-Response): 6E400002-B5A3-F393-E0A9-E50E24DCCA9E
TX char (robot→phone, Notify):                    6E400003-B5A3-F393-E0A9-E50E24DCCA9E
```

Direction naming trips everyone: RX/TX are from the ROBOT's perspective. Phone WRITES to RX. Robot NOTIFIES on TX.

### Protocol design rules
- One notification = one message. Don't stream a byte soup and parse for newlines unless MTU ≥ message size + 3 (ATT header is 3 bytes: usable = MTU − 3).
- Negotiate MTU first thing after connect. Request 247 (max single LL packet with DLE). iOS grants 185. Android grants up to 517.
- Use Write-No-Response for high-rate teleop commands (joystick at 20–50 Hz). Write-with-response throttles you to ~1 write per connection interval.
- Binary > JSON over BLE. A teleop packet should be ≤8 bytes: `[0xA5, cmd, vx_i8, vy_i8, wz_i8, flags, crc8, 0x5A]`.
- **Deadman timer is mandatory**: if no command received for 300–500 ms, stop motors. BLE supervision timeout (default 4–20 s) is far too slow to detect a dropped phone.

### ESP32 Arduino (NimBLE — use NimBLE-Arduino, NOT the Bluedroid `BLEDevice` library; Bluedroid eats ~30% more heap and conflicts with WiFi worse)

```cpp
#include <NimBLEDevice.h>

#define SVC_UUID "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
#define RX_UUID  "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
#define TX_UUID  "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

NimBLECharacteristic* txChar;
volatile uint32_t lastCmdMs = 0;
volatile int8_t cmdVx = 0, cmdWz = 0;

class RxCallback : public NimBLECharacteristicCallbacks {
  void onWrite(NimBLECharacteristic* c, NimBLEConnInfo&) override {
    NimBLEAttValue v = c->getValue();
    if (v.size() == 8 && v[0] == 0xA5 && v[7] == 0x5A) {
      cmdVx = (int8_t)v[2];
      cmdWz = (int8_t)v[4];
      lastCmdMs = millis();           // feed the deadman
    }
  }
};

class SrvCallback : public NimBLEServerCallbacks {
  void onConnect(NimBLEServer*, NimBLEConnInfo& info) override {
    // request fast connection params: min 15ms, max 30ms, latency 0, timeout 2s (units: 1.25ms / 10ms)
    NimBLEDevice::getServer()->updateConnParams(info.getConnHandle(), 12, 24, 0, 200);
  }
  void onDisconnect(NimBLEServer*, NimBLEConnInfo&, int) override {
    cmdVx = 0; cmdWz = 0;             // safety: zero commands
    NimBLEDevice::startAdvertising(); // CRITICAL: advertising does NOT restart automatically
  }
};

void setup() {
  NimBLEDevice::init("robot-01");
  NimBLEDevice::setMTU(247);
  NimBLEServer* srv = NimBLEDevice::createServer();
  srv->setCallbacks(new SrvCallback());
  NimBLEService* svc = srv->createService(SVC_UUID);
  txChar = svc->createCharacteristic(TX_UUID, NIMBLE_PROPERTY::NOTIFY);
  NimBLECharacteristic* rx = svc->createCharacteristic(RX_UUID,
      NIMBLE_PROPERTY::WRITE | NIMBLE_PROPERTY::WRITE_NR);
  rx->setCallbacks(new RxCallback());
  svc->start();
  NimBLEAdvertising* adv = NimBLEDevice::getAdvertising();
  adv->addServiceUUID(SVC_UUID);   // so scanners filter by service
  adv->start();
}

void loop() {
  // DEADMAN: 400 ms without a command -> stop
  bool alive = (millis() - lastCmdMs) < 400;
  driveMotors(alive ? cmdVx : 0, alive ? cmdWz : 0);

  // telemetry at 10 Hz, NEVER from a callback/ISR
  static uint32_t t = 0;
  if (millis() - t >= 100) {
    t = millis();
    uint8_t pkt[6] = {0xB5, batteryPct(), (uint8_t)(cmdVx), (uint8_t)(cmdWz), stateByte(), 0x5B};
    txChar->setValue(pkt, sizeof(pkt));
    txChar->notify();
  }
  delay(5);
}
```

### Pico W / generic MicroPython (aioble)

```python
import uasyncio as asyncio
import aioble, bluetooth, struct, time

_SVC = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_RX  = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
_TX  = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

svc = aioble.Service(_SVC)
rx = aioble.Characteristic(svc, _RX, write=True, write_no_response=True, capture=True)
tx = aioble.Characteristic(svc, _TX, notify=True)
aioble.register_services(svc)

last_cmd_ms = 0
cmd = (0, 0)

async def rx_task():
    global last_cmd_ms, cmd
    while True:
        conn, data = await rx.written()          # capture=True required for this API
        if len(data) == 8 and data[0] == 0xA5 and data[7] == 0x5A:
            cmd = (struct.unpack("b", data[2:3])[0], struct.unpack("b", data[4:5])[0])
            last_cmd_ms = time.ticks_ms()

async def motor_task():
    while True:
        alive = time.ticks_diff(time.ticks_ms(), last_cmd_ms) < 400
        drive(*(cmd if alive else (0, 0)))
        await asyncio.sleep_ms(20)

async def ble_task():
    while True:
        async with await aioble.advertise(250_000,  # 250 ms adv interval, in MICROseconds
                name="robot-01", services=[_SVC]) as conn:
            await conn.disconnected(timeout_ms=None)
        # loop re-advertises after disconnect

asyncio.run(asyncio.gather(rx_task(), motor_task(), ble_task()))
```

### BLE mistakes everyone makes
1. **Forgetting to restart advertising after disconnect.** ESP32 NimBLE and Bluedroid both stop advertising on disconnect. Symptom: "works once, then phone can't find robot until reboot."
2. **Sending >20 bytes without MTU negotiation.** Notification silently truncates to MTU−3. Always negotiate, or design packets ≤20 bytes.
3. **Calling `notify()` from the `onWrite` callback.** On ESP32 this runs on the BLE host task; blocking or re-entrant GATT ops there cause stack lockups. Set flags, do work in `loop()`.
4. **Trusting BLE supervision timeout as the deadman.** It's seconds. Robot drives into a wall. Use an application-level 300–500 ms timer.
5. **JSON over BLE for teleop.** `{"vx":0.5,"wz":-0.2}` is 22+ bytes — already over default MTU — and float parsing on-MCU wastes the connection interval. Binary structs.
6. **iOS connection-interval assumptions.** If your control loop needs 50 Hz commands, iOS at 30 ms interval gives you max ~33 notifications/s per interval slot. Batch two commands per packet or accept 30 Hz.
7. **Bonding/pairing left enabled when not needed.** Unbonded "Just Works" is fine for toy robots; half-completed bonds (phone deleted bond, robot kept it) cause connect-then-immediate-disconnect loops. If you don't need encryption, don't bond. If you do: on persistent disconnect loops, clear the bond store (`NimBLEDevice::deleteAllBonds()`).

---

## 3. MQTT for Robot Fleets

### Topic schema (use this, don't invent)
```
fleet/{fleet_id}/{robot_id}/status      retained, QoS1   "online"/"offline" — LWT lives here
fleet/{fleet_id}/{robot_id}/telemetry   not retained, QoS0  high-rate sensor data
fleet/{fleet_id}/{robot_id}/cmd         not retained, QoS1  commands TO robot
fleet/{fleet_id}/{robot_id}/cmd/ack     not retained, QoS1  command acknowledgements
fleet/{fleet_id}/{robot_id}/event       not retained, QoS1  low-rate state changes, errors
fleet/{fleet_id}/broadcast/cmd          not retained, QoS1  all-robots commands (e-stop!)
```
Robot subscribes: `fleet/F1/robot-07/cmd/#` and `fleet/F1/broadcast/#`.
Dashboard subscribes: `fleet/F1/+/status`, `fleet/F1/+/telemetry`.

### QoS selection — the actual rules
| Data | QoS | Why |
|---|---|---|
| Telemetry (pose, battery @ 1–20 Hz) | 0 | Next sample supersedes; QoS1 retransmits stale data and bloats the in-flight queue |
| Commands | 1 | Must arrive; dup possible → make handlers idempotent or carry a sequence number |
| Status / LWT | 1 + **retained** | Late subscribers must see current state instantly |
| E-stop | 1 (NOT 2) | QoS2's 4-way handshake adds latency; QoS1 dup of "STOP" is harmless |
| Anything | 2 | Almost never. Only for non-idempotent ops where a duplicate is costly (e.g. "dispense one item") |

QoS0 on a flaky link silently drops messages — that's correct for telemetry, wrong for everything else.

### LWT offline detection (the only reliable presence mechanism)
On CONNECT, register the will. After successful connect, publish the inverse:

```
Will:    topic=fleet/F1/robot-07/status  payload="offline"  QoS1 retain=true
Then:    publish fleet/F1/robot-07/status "online" QoS1 retain=true
```

Broker fires the will when keepalive expires (broker waits 1.5 × keepalive) or TCP drops. With keepalive=15 s, offline detection latency ≤ ~23 s. For faster detection, lower keepalive to 5 s (broker load: one PINGREQ per robot per ~4 s — fine for hundreds of robots, reconsider for 10k+).

**Graceful-shutdown gotcha**: a clean DISCONNECT packet suppresses the LWT. Publish `"offline"` explicitly before clean disconnects, or your robot stays "online" forever after a polite shutdown.

**Reconnect gotcha**: if the robot reconnects after a network blip, the broker may fire the OLD connection's LWT *after* the new connection published "online" (race). Fix: include a timestamp or session-id in the status payload and have the dashboard ignore older ones; or use MQTT5 session takeover which closes the old connection first (most brokers handle same-client-id takeover correctly — which is why **every robot must use a unique client ID**; two robots sharing one client ID create an infinite mutual-disconnect loop, the classic "fleet flapping" bug).

### ESP32 Arduino (PubSubClient)
PubSubClient defaults: `MQTT_MAX_PACKET_SIZE 256` (silently drops bigger publishes — increase via `client.setBufferSize(1024)`), keepalive 15 s, QoS0-only for publish (it cannot publish QoS1!). For QoS1 publish on ESP32 use **ArduinoMqttClient** or **espMqttClient**; pattern below uses PubSubClient where QoS0 telemetry is the bulk and shows the limitation explicitly.

```cpp
#include <WiFi.h>
#include <PubSubClient.h>

WiFiClient net;
PubSubClient mqtt(net);
const char* ROBOT_ID = "robot-07";
char topicStatus[48], topicCmd[48], topicTele[48];

void onMsg(char* topic, byte* payload, unsigned int len) {
  // payload is NOT null-terminated. Copy before strcmp/atoi.
  char buf[128];
  len = min(len, (unsigned int)127);
  memcpy(buf, payload, len); buf[len] = 0;
  if (strstr(topic, "/cmd")) handleCommand(buf);
}

bool mqttConnect() {
  mqtt.setServer("192.168.1.10", 1883);
  mqtt.setCallback(onMsg);
  mqtt.setBufferSize(1024);
  mqtt.setKeepAlive(15);
  // connect(id, user, pass, willTopic, willQos, willRetain, willMsg, cleanSession)
  if (!mqtt.connect(ROBOT_ID, "fleetuser", "fleetpass",
                    topicStatus, 1, true, "offline", true)) return false;
  mqtt.publish(topicStatus, "online", true);          // retained
  mqtt.subscribe(topicCmd, 1);
  mqtt.subscribe("fleet/F1/broadcast/#", 1);
  return true;
}

void loop() {
  ensureWifi();                  // see §4 state machine
  if (WiFi.status() == WL_CONNECTED && !mqtt.connected()) {
    static uint32_t lastTry = 0;
    if (millis() - lastTry > 5000) { lastTry = millis(); mqttConnect(); }
  }
  mqtt.loop();                   // MUST be called every loop; >keepalive gap = disconnect

  static uint32_t t = 0;
  if (mqtt.connected() && millis() - t >= 200) {  // 5 Hz telemetry
    t = millis();
    char json[96];
    snprintf(json, sizeof(json), "{\"x\":%.2f,\"y\":%.2f,\"th\":%.2f,\"bat\":%d}",
             pose.x, pose.y, pose.th, batteryPct());
    mqtt.publish(topicTele, json);               // QoS0 — correct for telemetry
  }
}
```

`snprintf(topicStatus, 48, "fleet/F1/%s/status", ROBOT_ID);` etc. in setup.

### Python / Raspberry Pi (paho-mqtt v2)

```python
import paho.mqtt.client as mqtt
import json, time

ROBOT_ID = "robot-07"
BASE = f"fleet/F1/{ROBOT_ID}"

def on_connect(client, userdata, flags, reason_code, properties):
    # Subscriptions go HERE, not at top level — they survive reconnects this way.
    client.subscribe(f"{BASE}/cmd/#", qos=1)
    client.subscribe("fleet/F1/broadcast/#", qos=1)
    client.publish(f"{BASE}/status", "online", qos=1, retain=True)

def on_message(client, userdata, msg):
    cmd = json.loads(msg.payload)          # wrap in try/except in production
    if cmd.get("op") == "estop":
        stop_motors()                       # handle BEFORE queueing anything else

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=ROBOT_ID,
                     clean_session=False)   # persistent session: queued QoS1 cmds survive blips
client.will_set(f"{BASE}/status", "offline", qos=1, retain=True)
client.on_connect = on_connect
client.on_message = on_message
client.reconnect_delay_set(min_delay=1, max_delay=30)   # built-in backoff
client.connect("192.168.1.10", 1883, keepalive=15)
client.loop_start()                        # background thread; loop_forever() if main thread is free

try:
    while True:
        client.publish(f"{BASE}/telemetry", json.dumps(get_pose()), qos=0)
        time.sleep(0.2)
finally:
    client.publish(f"{BASE}/status", "offline", qos=1, retain=True)  # suppress-LWT fix
    client.disconnect()
```

`clean_session=False` + QoS1 subscription means commands published while the robot was offline are delivered on reconnect. Decide if you WANT that: a 5-minute-old "move forward" replaying is dangerous. Either use clean sessions for cmd topics, or timestamp commands and reject ones older than ~2 s. **Always timestamp commands.**

### MQTT mistakes everyone makes
1. Shared client IDs → mutual-disconnect flapping (see above).
2. Retained telemetry. New dashboard subscriber gets a stale pose and renders a ghost robot. Retain status only.
3. Stale retained messages haunting topics. Clear with a retained zero-length publish: `client.publish(topic, "", retain=True)`.
4. Blocking inside `on_message` (paho runs it on the network thread — a 2 s handler stalls keepalive → broker drops you). Put commands on a queue.
5. PubSubClient publish silently failing on payloads > buffer size. Check the bool return.
6. Closing a control loop through the broker. Broker is for supervision; reflexes live on the robot.
7. No e-stop path that bypasses the command queue. Broadcast e-stop topic, handled first, always.
8. TLS on ESP32 without time sync — cert validation fails until NTP sets the clock. Sync NTP before `connect()` on port 8883, and budget ~50 KB extra heap for the TLS session.

---

## 4. WiFi Reconnect State Machine

Never write `while (WiFi.status() != WL_CONNECTED) delay(500);` in `loop()` — it freezes motor control. Non-blocking state machine, always:

```cpp
enum WifiState { W_IDLE, W_CONNECTING, W_CONNECTED, W_BACKOFF };
WifiState wstate = W_IDLE;
uint32_t wTimer = 0, wBackoffMs = 1000;
uint8_t wAttempts = 0;

void ensureWifi() {
  switch (wstate) {
    case W_IDLE:
      WiFi.mode(WIFI_STA);
      WiFi.setSleep(false);              // modem sleep adds 100-300ms latency spikes; robots want it OFF
      WiFi.begin(ssid, pass);
      wTimer = millis(); wstate = W_CONNECTING;
      break;
    case W_CONNECTING:
      if (WiFi.status() == WL_CONNECTED) {
        wstate = W_CONNECTED; wBackoffMs = 1000; wAttempts = 0;
      } else if (millis() - wTimer > 15000) {   // 15 s connect timeout
        WiFi.disconnect(true);
        wTimer = millis(); wstate = W_BACKOFF;
      }
      break;
    case W_CONNECTED:
      if (WiFi.status() != WL_CONNECTED) {      // AP rebooted / out of range
        wTimer = millis(); wstate = W_BACKOFF;
      }
      break;
    case W_BACKOFF:
      if (millis() - wTimer > wBackoffMs) {
        wBackoffMs = min(wBackoffMs * 2, (uint32_t)30000);  // 1,2,4,...30 s cap
        if (++wAttempts >= 10) { wAttempts = 0; /* optional: ESP.restart() or fall to provisioning §6 */ }
        wstate = W_IDLE;
      }
      break;
  }
}
```

Rules baked into that code, each learned the hard way:
- `WiFi.setSleep(false)` — ESP32 modem sleep (default ON) causes periodic 100–300 ms ping spikes that look like "random network lag" in teleop.
- Exponential backoff with cap. Hammering reconnects every 500 ms can keep some APs' auth state confused and drains battery.
- 15 s connect timeout, then full `disconnect(true)` to reset the supplicant — ESP32 sometimes wedges in `WL_DISCONNECTED` after auth failures and only a disconnect/begin cycle recovers it.
- Don't call `WiFi.begin()` repeatedly while already connecting — it restarts the handshake and you never converge.
- Static IP (`WiFi.config(...) ` BEFORE `begin()`) shaves 1–3 s of DHCP off every reconnect — worth it on fleets.
- ESP32 `WiFi.setAutoReconnect(true)` exists but gives you no backoff control and races with your own logic. Pick one owner — this state machine — and disable auto-reconnect.

MicroPython (Pico W) equivalent — key API facts: `wlan.status()` returns `STAT_CONNECTING(1) / STAT_GOT_IP(3) / STAT_WRONG_PASSWORD(-3) / STAT_NO_AP_FOUND(-2) / STAT_CONNECT_FAIL(-1)`. Negative = terminal, re-issue `wlan.connect()`. Pico W also needs `wlan.config(pm=0xa11140)` to disable power-save (same latency-spike issue as ESP32).

```python
import network, time
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm=0xa11140)   # power-save OFF

def wifi_tick(state):      # call from main loop; state is a dict
    s = wlan.status()
    if state["phase"] == "idle":
        wlan.connect(SSID, PASS)
        state.update(phase="connecting", t=time.ticks_ms())
    elif state["phase"] == "connecting":
        if s == 3: state["phase"] = "up"; state["backoff"] = 1000
        elif s < 0 or time.ticks_diff(time.ticks_ms(), state["t"]) > 15000:
            wlan.disconnect(); state.update(phase="backoff", t=time.ticks_ms())
    elif state["phase"] == "up":
        if s != 3: state.update(phase="backoff", t=time.ticks_ms())
    elif state["phase"] == "backoff":
        if time.ticks_diff(time.ticks_ms(), state["t"]) > state["backoff"]:
            state["backoff"] = min(state["backoff"] * 2, 30000)
            state["phase"] = "idle"
```

Safety rule that overrides everything: **motor outputs must not depend on WiFi state transitions happening.** The deadman timer (no command in N ms → stop) covers WiFi drops automatically; the state machine only handles getting back online.

---

## 5. ESP32 BLE + WiFi Coexistence

Both share ONE 2.4 GHz radio with time-division multiplexing. Facts:

- Throughput on each drops 30–70% when both are active. WiFi can stall for tens of ms during BLE connection events.
- BLE **scanning** while WiFi is active is the worst case — scan windows starve WiFi. Keep scan duty cycle low (window ≤ 30 ms of a 100 ms interval) or scan only when WiFi is idle.
- BLE advertising + connected WiFi STA is the *manageable* case and the normal robot pattern (BLE for phone config, WiFi/MQTT for fleet).
- Arduino core ships with coexistence (`CONFIG_SW_COEXIST_ENABLE`) on by default for recent versions; in ESP-IDF set `CONFIG_ESP_COEX_SW_COEXIST_ENABLE=y`. Without it, expect hard WiFi disconnects when BLE connects.
- RAM: WiFi + Bluedroid + TLS doesn't fit comfortably in 320 KB. NimBLE (~20 KB) instead of Bluedroid (~50 KB+) is mandatory for combined use. If you see `E (xxx) wifi: esf_buf: t=... alloc failed` or random `Guru Meditation` in `wifi` task → you're out of heap; check `ESP.getFreeHeap()` stays > 40 KB.
- BLE connection interval ≥ 30 ms when WiFi is active — 7.5 ms intervals leave no airtime for WiFi.
- Practical architecture: **don't run BLE and WiFi data planes simultaneously.** Use BLE for provisioning/diagnostics, then `NimBLEDevice::deinit(true)` once WiFi+MQTT is up (frees ~20 KB heap too). Re-init BLE only when entering config mode (button hold).
- ESP32-C3/S3 same story (single radio). If you genuinely need both at full rate, use two chips (e.g. ESP32 + nRF52) or ESP32 + a USB BT dongle on a Pi.

---

## 6. Captive Portal Provisioning (WiFi credentials without a screen)

Flow: no stored creds (or button held 3 s at boot) → robot starts AP `Robot-Setup-XXXX` → phone joins → captive portal pops → user picks SSID, enters password → robot stores in NVS → reboots into STA mode.

The captive-portal "pop" works by answering **all** DNS queries with the AP's own IP, then serving the config page on HTTP. OS-specific probe URLs you must answer with a non-204/redirect: Android hits `connectivitycheck.gstatic.com/generate_204`, iOS hits `captive.apple.com/hotspot-detect.html`, Windows hits `msftconnecttest.com/connecttest.txt`.

Don't hand-roll it on ESP32 — use **WiFiManager** (tzapu):

```cpp
#include <WiFiManager.h>

void provisionIfNeeded() {
  WiFiManager wm;
  wm.setConfigPortalTimeout(180);        // 3 min then give up & reboot — REQUIRED, else robot
                                         // sits in AP mode forever after a transient AP outage
  wm.setConnectTimeout(15);
  // optional custom field, e.g. fleet id:
  WiFiManagerParameter fleetParam("fleet", "Fleet ID", "F1", 8);
  wm.addParameter(&fleetParam);

  bool ok;
  if (digitalRead(BTN_PIN) == LOW) ok = wm.startConfigPortal("Robot-Setup");  // forced
  else                             ok = wm.autoConnect("Robot-Setup");        // only if no creds
  if (!ok) ESP.restart();
  // creds are now in NVS; WiFi.begin() with no args reuses them forever
}
```

Hand-rolled MicroPython core (Pico W) — the two essential pieces are the DNS catch-all and the form handler:

```python
# AP mode
ap = network.WLAN(network.AP_IF)
ap.config(essid="Robot-Setup", password="configure")  # WPA2 needs >=8 chars; open AP: security=0
ap.active(True)                                        # AP IP is 192.168.4.1

# DNS server: answer EVERY query with 192.168.4.1 (this is what triggers the portal popup)
import socket
dns = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dns.bind(("0.0.0.0", 53)); dns.setblocking(False)

def dns_tick():
    try: req, addr = dns.recvfrom(256)
    except OSError: return
    # minimal DNS response: copy ID, set response flags, answer A 192.168.4.1
    resp = req[:2] + b"\x81\x80" + req[4:6]*2 + b"\x00\x00\x00\x00" + req[12:] \
         + b"\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04" + bytes([192,168,4,1])
    dns.sendto(resp, addr)
```

Then a tiny HTTP server on port 80 serving a form (`GET /` → page with SSID scan results from `sta.scan()`; `POST /save` → parse, write `wifi.json`, reboot). Store creds in a file (Pico) or NVS/Preferences (ESP32) — never hardcode.

Provisioning mistakes:
- No portal timeout → robot stranded in AP mode forever (most common field failure).
- Password field with autocorrect/capitalization on phone → add `autocapitalize="none" autocorrect="off"` to the input.
- Testing creds by rebooting blind. Better: attempt STA connect *while keeping AP up* (ESP32 `WIFI_AP_STA` mode), report success/failure on the portal page, only then reboot.
- BLE provisioning alternative: Espressif's `WiFiProv` library + ESP BLE Provisioning app works out of the box and avoids the AP-switching dance — prefer it when users will install your app anyway; captive portal wins when they won't.

---

## 7. ROS2 Bridging (when the fleet meets ROS)

- micro-ROS on ESP32 speaks DDS-XRCE over WiFi/serial to an agent — use it when you want the MCU to be a first-class ROS2 node. Heavier than MQTT (~100 KB flash, needs the agent running).
- Simpler and robust: `mqtt_client` ROS2 package (ika-rwth-aachen) bridges MQTT topics ↔ ROS2 topics declaratively in YAML. Robots stay plain-MQTT; ROS sees native topics.
- Map: `fleet/F1/+/telemetry` → `/fleet/robot_x/pose` (`geometry_msgs/PoseStamped`), `/fleet/robot_x/cmd_vel` → `fleet/F1/robot-x/cmd` (serialize Twist → your 8-byte struct or JSON).
- DDS over WiFi multicast discovery is flaky on consumer APs (IGMP snooping eats multicast). If ROS2 nodes can't see each other over WiFi: set `ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET`, or switch to unicast discovery via Fast-DDS discovery server (`ROS_DISCOVERY_SERVER=ip:11811`). This single fact resolves 90% of "ROS2 works on ethernet but not WiFi" reports.

---

## 8. Debugging Checklists

### BLE
1. Robot not visible in scan → advertising actually started? (check restart-after-disconnect, §2 mistake #1). Scanner filtering by service UUID you forgot to put in the adv packet?
2. Connects then drops in ~30–40 s → supervision timeout with bad conn params, or stale bond (clear bonds both sides).
3. Data truncated at 20 bytes → MTU never negotiated.
4. Notifications not arriving → client never wrote the CCCD (enable notifications); nRF Connect: tap the triple-down-arrow icon. Code: subscribed before service discovery completed?
5. Works with Android, not iOS → conn interval request <15 ms (iOS rejects), or relying on adv name caching (iOS caches aggressively — toggle phone BT).
6. Random ESP32 reboots during BLE traffic → heap exhaustion (Bluedroid + WiFi) or GATT ops in callbacks. `ESP.getFreeHeap()` every second to the log.

### MQTT
1. Robot flaps online/offline → duplicate client ID somewhere (check broker log: "already connected").
2. Commands never arrive → subscribed inside `on_connect`? Topic case/typo (`Fleet/` ≠ `fleet/`)? QoS0 sub on lossy link?
3. LWT never fires → keepalive too long, or client library auto-reconnects and you never notice; check broker log for keepalive value actually negotiated.
4. "offline" shows while robot is clearly running → LWT race after reconnect (§3), or robot publishes status without retain so late subscribers miss "online".
5. Big publishes vanish on ESP32 → PubSubClient buffer (default 256). `setBufferSize()` and check publish() return value.
6. Broker test commands: `mosquitto_sub -h HOST -t 'fleet/#' -v` (watch everything), `mosquitto_pub -h HOST -t fleet/F1/robot-07/cmd -q 1 -m '{"op":"estop"}'`.

### WiFi
1. `WL_NO_SSID_AVAIL` → 2.4 GHz disabled on AP (ESP32/Pico W cannot do 5 GHz), or SSID hidden + library can't do hidden scan (pass `bssid`/channel to `begin()`).
2. Auth fails with correct password → WPA3-only AP (ESP32 classic needs WPA2 or WPA3-transition mode); or password has space/smart-quote from a phone paste.
3. Periodic 100–300 ms latency spikes → modem power save still on (§4).
4. Connects, then no traffic → AP client isolation enabled (robot and laptop can both reach the AP but not each other — very common on guest networks). Test: ping the gateway (works) vs ping peer (fails).
5. mDNS name (`robot.local`) unreachable from Android → Android <12 lacks mDNS resolution in most apps; use IPs or DNS.
6. Reconnect storms after power outage → all robots + AP boot simultaneously; AP not ready when robots first try. Your backoff (§4) handles it; fixed-delay retry loops don't.

### Coexistence
1. WiFi drops exactly when phone connects via BLE → conn interval too aggressive; force ≥30 ms (§5).
2. Heap crash after enabling both stacks → switch Bluedroid→NimBLE; deinit BLE when not provisioning.

---

## 9. Quick Reference Card

| Constant | Value |
|---|---|
| BLE default ATT MTU / usable payload | 23 / 20 bytes |
| BLE max useful MTU request (ESP32) | 247 (iOS grants 185, Android up to 517) |
| BLE conn interval floor: spec / iOS-honored | 7.5 ms / ~15 ms (typically granted 30 ms) |
| Teleop deadman timeout | 300–500 ms |
| MQTT keepalive for robots | 15 s (5 s if fast offline detection needed) |
| Broker LWT fires after | 1.5 × keepalive |
| MQTT reconnect backoff | 1 s → ×2 → cap 30 s |
| WiFi connect timeout before reset | 15 s |
| PubSubClient default max packet | 256 B (`setBufferSize` to raise) |
| ESP32 free-heap red line (WiFi+BLE+TLS) | < 40 KB = trouble |
| Pico W disable power save | `wlan.config(pm=0xa11140)` |
| ESP32 disable power save | `WiFi.setSleep(false)` |
| MQTT port / TLS port | 1883 / 8883 (8883 needs NTP first on MCUs) |
| Captive portal probe URLs | `generate_204` (Android), `hotspot-detect.html` (iOS), `connecttest.txt` (Win) |
