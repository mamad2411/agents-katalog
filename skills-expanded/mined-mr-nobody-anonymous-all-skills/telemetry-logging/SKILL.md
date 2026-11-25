---
name: telemetry-logging
description: "Use when implementing robot telemetry, structured logging, flight-recorder/black-box capture, MCAP/rosbag recording, Foxglove/PlotJuggler visualization, or fleet telemetry uplinks over MQTT. Provides exact logging-level discipline, ring-buffer fault capture patterns, rosbag2/MCAP record strategies with QoS and storage budgets, sim-vs-wall clock correlation, and bandwidth-budgeted MQTT downsampling code for MicroPython, Arduino C++, and ROS 2 Python."
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


# Robot Telemetry & Logging

Telemetry that can't answer "what happened in the 5 seconds before the fault?" is decoration.
This skill covers the full stack: structured levels → on-robot ring buffer → MCAP/rosbag record
→ offline analysis (Foxglove/PlotJuggler) → fleet uplink over MQTT.

---

## 1. Logging Levels — The Discipline That Actually Works

The universal mistake: everything logged at INFO, so logs are 99% noise and the one line that
mattered scrolled away. Use this contract and never deviate:

| Level  | Contract                                              | Rate ceiling        | Examples |
|--------|-------------------------------------------------------|---------------------|----------|
| FATAL  | Robot cannot continue; e-stop or reboot follows       | once per fault      | watchdog timeout, motor driver OVP latch |
| ERROR  | A subsystem failed but robot degrades gracefully      | < 1/s sustained     | sensor read NACK after retries, planner returned no path |
| WARN   | Out-of-nominal but handled                            | < 5/s, rate-limited | battery < 20%, IMU sample dropped, loop overrun |
| INFO   | State transitions ONLY                                | event-driven        | mode change IDLE→AUTO, mission start, calibration done |
| DEBUG  | Periodic numeric state (pose, currents, setpoints)    | bounded by topic Hz | per-loop PID terms |
| TRACE  | Per-message / per-byte (I2C transactions, CAN frames) | OFF in production   | raw register dumps |

**Hard rules:**
- INFO is for *transitions*, never for periodic data. "Loop running, battery=12.1V" every second
  at INFO is the #1 log-pollution antipattern. Periodic numerics go to DEBUG or, better, to a
  telemetry channel (MCAP/rosbag topic, CSV, MQTT) — *logs are for events, telemetry is for signals*.
- Every WARN+ message must carry enough context to act on: subsystem, numeric values, units.
  `WARN battery low` is useless. `WARN [pwr] vbat=10.9V (<11.1V cutoff in 0.2V), load=3.2A` is actionable.
- Rate-limit anything that can fire in a loop. A WARN inside a 1 kHz control loop will saturate
  UART (115200 baud ≈ 11.5 KB/s ≈ 140 short lines/s) and *the logging itself* causes loop overruns.

### Structured format

Always machine-parseable. One line = one JSON object (or key=value pairs on flash-tight MCUs):

```
{"t":1718041č023.481,"lvl":"WARN","src":"pwr","msg":"vbat_low","vbat":10.91,"load_a":3.2}
```

Fields: `t` (epoch seconds, float, see §6 on clocks), `lvl`, `src` (subsystem tag, ≤8 chars),
`msg` (snake_case event name — stable identifier, NOT prose), then numeric fields. Grep-able,
jq-able, ingestable. Prose goes in a `note` field if you must.

### MicroPython structured logger (ESP32 / RP2040 / Pico W)

```python
# tlog.py — structured logger, ~0.5 KB RAM, no allocation in hot path beyond the dict
import time, sys, json

LEVELS = {"TRACE":5,"DEBUG":10,"INFO":20,"WARN":30,"ERROR":40,"FATAL":50}
_threshold = LEVELS["INFO"]
_rate_state = {}   # msg -> (last_emit_ms, suppressed_count)

def set_level(name):                      # call once at boot, e.g. from config
    global _threshold
    _threshold = LEVELS[name]

def log(lvl, src, msg, rate_ms=0, **kv):
    if LEVELS[lvl] < _threshold:
        return
    now = time.ticks_ms()
    if rate_ms:                            # rate limiting per event name
        last, supp = _rate_state.get(msg, (None, 0))
        if last is not None and time.ticks_diff(now, last) < rate_ms:
            _rate_state[msg] = (last, supp + 1)
            return
        if supp:
            kv["suppressed"] = supp
        _rate_state[msg] = (now, 0)
    rec = {"t": time.time(), "lvl": lvl, "src": src, "msg": msg}
    rec.update(kv)
    line = json.dumps(rec)
    print(line)                            # UART/USB console
    _ring_push(line)                       # black box — see §2

# Usage in a control loop — rate-limited so it can NEVER flood:
# log("WARN", "ctl", "loop_overrun", rate_ms=1000, dt_ms=dt, budget_ms=10)
```

### Arduino C++ structured logger (AVR/ESP32/Teensy)

```cpp
// tlog.h — printf-style structured log. F() macros keep strings in flash on AVR.
#include <Arduino.h>
enum LogLevel { TRACE=5, DEBUG=10, INFO=20, WARN=30, ERROR_=40, FATAL=50 };
static LogLevel g_threshold = INFO;

// IMPORTANT: snprintf into a fixed buffer; never use String in logging paths
// (heap fragmentation on AVR/ESP8266 kills long-running robots).
#define TLOG(lvl, src, fmt, ...) do {                                  \
  if ((lvl) >= g_threshold) {                                          \
    char _b[160];                                                      \
    snprintf(_b, sizeof(_b),                                           \
      "{\"t\":%lu.%03lu,\"lvl\":\"%s\",\"src\":\"%s\"," fmt "}",       \
      millis()/1000UL, millis()%1000UL, #lvl, src, ##__VA_ARGS__);     \
    Serial.println(_b);                                                \
    ring_push(_b);                                                     \
  }                                                                    \
} while (0)

// Usage:
// TLOG(WARN, "pwr", "\"msg\":\"vbat_low\",\"vbat\":%d.%02d", v/100, v%100);
// Note: %f is NOT supported by AVR snprintf by default — print fixed-point as above,
// or on AVR link with -Wl,-u,vfprintf -lprintf_flt (costs ~1.5 KB flash).
```

**Serial budget math (do this before you ship):** at 115200 baud you get ~11,520 bytes/s.
A 120-byte JSON line = ~96 lines/s max — and writing it blocks once the 64-byte TX buffer fills.
A 100 Hz control loop logging one line per iteration *will* block and jitter the loop.
Either raise baud (ESP32/Teensy handle 921600+ fine over USB-CDC), log every Nth iteration,
or move periodic numerics to a binary telemetry channel.

---

## 2. Black-Box Ring Buffer — Flush on Fault

The pattern: keep the last N seconds of *everything* (including DEBUG/TRACE) in a RAM ring
buffer regardless of console threshold. On fault, dump it to flash/SD/uplink. You get
full-detail forensics without paying the runtime cost of always persisting full detail.

**Sizing:** decide "seconds of history" first, then derive bytes.
100 lines/s × 120 B × 10 s = 120 KB → fine on ESP32 (520 KB RAM), impossible on AVR (2 KB —
use a 4–8 entry ring of compact binary records instead, or skip to an external FRAM chip).

### MicroPython ring buffer + fault flush

```python
# blackbox.py — fixed-slot ring; no allocation per push after init
import os, time

_SLOTS = 512                       # tune: slots × 160 B ≈ 80 KB RAM on ESP32
_buf = [None] * _SLOTS
_idx = 0
_wrapped = False

def _ring_push(line):              # called by tlog.log for EVERY record >= TRACE
    global _idx, _wrapped
    _buf[_idx] = line
    _idx = (_idx + 1) % _SLOTS
    if _idx == 0:
        _wrapped = True

def flush_blackbox(reason):
    """Call from fault handlers. Writes chronological dump to flash.
    Keep last 5 dumps; LittleFS on ESP32 internal flash is fine for ~100 KB."""
    fname = "/bb_{}_{}.log".format(int(time.time()), reason)
    order = (_buf[_idx:] + _buf[:_idx]) if _wrapped else _buf[:_idx]
    with open(fname, "w") as f:
        f.write("# blackbox reason={} t={}\n".format(reason, time.time()))
        for line in order:
            if line:
                f.write(line + "\n")
    _prune_old(keep=5)

def _prune_old(keep):
    dumps = sorted(f for f in os.listdir("/") if f.startswith("bb_"))
    for f in dumps[:-keep]:
        os.remove("/" + f)
```

**Wire it to every fault path:**

```python
# Hardware watchdog + fault hooks (ESP32 MicroPython)
from machine import WDT, reset
import micropython
micropython.alloc_emergency_exception_buf(100)  # MUST — else ISR exceptions are silent

wdt = WDT(timeout=2000)            # 2 s; feed in main loop ONLY (never in a timer ISR —
                                   # that defeats the purpose: a hung main loop with a
                                   # live timer ISR would still feed the dog)
try:
    while True:
        control_step()
        wdt.feed()
except Exception as e:
    log("FATAL", "main", "unhandled", err=repr(e))
    flush_blackbox("exc")
    time.sleep_ms(200)             # let UART drain
    reset()
```

**Checking *why* you booted (distinguishes watchdog from brownout from power-cycle):**

```python
import machine
cause = machine.reset_cause()
# machine.PWRON_RESET / machine.HARD_RESET / machine.WDT_RESET /
# machine.DEEPSLEEP_RESET / machine.SOFT_RESET / machine.BROWN_OUT_RESET (port-dependent)
log("INFO", "boot", "reset", cause=cause)
if cause == machine.WDT_RESET:
    log("ERROR", "boot", "watchdog_reset_detected")
    # Previous blackbox dump on flash is the crime scene — upload it, see §7.
```

### Arduino C++ ring buffer (ESP32) with brownout-survivable flush

```cpp
// 64 KB ring in RAM; flush to LittleFS on fault. ESP32 has RTC_NOINIT_ATTR memory
// that survives soft resets — stash a fault flag there so the NEXT boot knows.
#include <LittleFS.h>
#include "esp_system.h"

static const size_t RING_BYTES = 64 * 1024;
static char ring[RING_BYTES];
static volatile size_t ring_head = 0;
static volatile bool ring_wrapped = false;
RTC_NOINIT_ATTR uint32_t g_fault_magic;        // survives esp_restart()
#define FAULT_MAGIC 0xDEADFA11

void ring_push(const char* line) {
  size_t len = strlen(line);
  for (size_t i = 0; i <= len; i++) {          // include '\0' as separator
    ring[ring_head] = (i < len) ? line[i] : '\n';
    ring_head = (ring_head + 1) % RING_BYTES;
    if (ring_head == 0) ring_wrapped = true;
  }
}

void flush_blackbox(const char* reason) {
  File f = LittleFS.open("/bb_latest.log", "w");   // overwrite; rotate offline
  if (!f) return;
  f.printf("# reason=%s millis=%lu\n", reason, millis());
  if (ring_wrapped) f.write((uint8_t*)ring + ring_head, RING_BYTES - ring_head);
  f.write((uint8_t*)ring, ring_head);
  f.close();                                       // close() flushes — do not skip
  g_fault_magic = FAULT_MAGIC;
}

void setup() {
  Serial.begin(921600);
  LittleFS.begin(true);
  esp_reset_reason_t rr = esp_reset_reason();
  // ESP_RST_TASK_WDT / ESP_RST_INT_WDT / ESP_RST_BROWNOUT / ESP_RST_PANIC ...
  if (rr != ESP_RST_POWERON || g_fault_magic == FAULT_MAGIC) {
    Serial.printf("{\"lvl\":\"ERROR\",\"src\":\"boot\",\"msg\":\"abnormal_reset\",\"rr\":%d}\n", rr);
    g_fault_magic = 0;
    // mark /bb_latest.log for upload before it gets overwritten
    LittleFS.rename("/bb_latest.log", "/bb_fault.log");
  }
}
```

**Mistakes everyone makes with black boxes:**
1. Flushing inside an ISR or hard-fault handler that needs heap/filesystem — it deadlocks.
   On hard fault, set a flag in noinit RAM and flush on next boot instead.
2. Forgetting the flush takes time: writing 64 KB to ESP32 internal flash ≈ 200–600 ms.
   If the fault is "battery at brownout threshold," you may not have 600 ms. Keep a *small*
   critical ring (last 2 s) for brownout, flush the big one only for software faults.
3. Not timestamping ring entries — after the fact you can't align with external video/rosbag.
4. Flushing to SD over SPI shared with another device without taking the bus mutex.
5. SD card corruption: never cut power mid-write. If your robot's e-stop kills logic power,
   the SD card WILL eventually corrupt. Use LittleFS on internal flash for the black box
   (power-fail safe by design); SD only for bulk recording with a supercap or orderly shutdown.

---

## 3. ROS 2: rosbag2 + MCAP Record Strategy

**Use MCAP, not sqlite3.** MCAP is the default storage in Iron+; on Humble install
`ros-humble-rosbag2-storage-mcap` and pass `-s mcap`. MCAP advantages: self-contained schemas
(file is readable without your workspace's message definitions — critical 6 months later),
chunked + indexed (Foxglove seeks instantly), optional CRC, append-recovery after crash.

### Record commands that actually work

```bash
# Everything, MCAP, zstd-chunk-compressed, split files, bounded disk:
ros2 bag record -a -s mcap \
  --compression-mode file --compression-format zstd \
  --max-bag-size 2000000000 \
  --max-cache-size 268435456 \
  -o /data/bags/run_$(date +%Y%m%d_%H%M%S)

# Production: explicit topic list — '-a' on a robot with cameras will eat the disk.
ros2 bag record -s mcap -o /data/bags/mission_001 \
  /tf /tf_static /odom /imu/data /joint_states \
  /cmd_vel /battery_state /diagnostics /rosout \
  /scan \
  /camera/image_raw/compressed          # ALWAYS the /compressed transport, never raw
```

**Disk budget table (know these numbers cold):**

| Topic                          | Typical rate | Bandwidth        |
|--------------------------------|--------------|------------------|
| 640×480 RGB raw image          | 30 Hz        | 26 MB/s (!!)     |
| same, /compressed (JPEG q=80)  | 30 Hz        | ~1.5 MB/s        |
| 1080p raw                      | 30 Hz        | 178 MB/s — never |
| sensor_msgs/PointCloud2 (VLP16)| 10 Hz        | ~3 MB/s          |
| /scan (720-pt LaserScan)       | 40 Hz        | ~120 KB/s        |
| /imu/data                      | 200 Hz       | ~65 KB/s         |
| /tf + /odom + /joint_states    | 50–100 Hz    | ~100 KB/s        |

Rule of thumb: a nav robot logging everything-but-raw-images runs 5–15 GB/hour with
compressed camera, < 0.5 GB/hour without cameras.

**QoS gotcha #1:** `ros2 bag record` subscribes with default QoS adaptivity, but sensors
publishing BEST_EFFORT (most camera/lidar drivers) need the recorder to match. Modern rosbag2
auto-detects, but if a topic records 0 messages, this is why. Force overrides:

```yaml
# qos_overrides.yaml  →  ros2 bag record ... --qos-profile-overrides-path qos_overrides.yaml
/camera/image_raw/compressed:
  reliability: best_effort
  durability: volatile
  history: keep_last
  depth: 10
```

**QoS gotcha #2:** record `/tf_static` with TRANSIENT_LOCAL durability or your bag has no
static transforms and RViz/Foxglove shows a broken TF tree. rosbag2 handles this if the
recorder starts *after* the publisher; if you start recording first, latched messages
published before any subscription can still be missed on some distro/DDS combos — start
recording after bringup, or rely on `--include-hidden-topics` + transient_local override.

**Cache gotcha:** default `--max-cache-size` is small; high-rate topics drop messages with
`Dropped X messages` warnings. 256 MB cache (as above) handles bursts; watch the recorder's
own log output during a test run before trusting it on a real mission.

### Snapshot mode = ROS-level black box

rosbag2 (Humble+) supports snapshot mode: record into a RAM ring, write to disk only on trigger.

```bash
ros2 bag record -a -s mcap --snapshot-mode --max-cache-size 536870912 \
  -o /data/bags/snapshot
# ... ring fills in RAM (here: last ~512 MB of traffic) ...
ros2 service call /rosbag2_recorder/snapshot rosbag2_interfaces/srv/Snapshot
```

Wire the snapshot service call into your fault monitor: on `/diagnostics` ERROR or e-stop
edge, call the service. This is the ROS equivalent of §2 and the single highest-value
debugging tool on a ROS robot.

```python
# fault_snapshot.py — minimal fault-triggered snapshot node
import rclpy
from rclpy.node import Node
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus
from rosbag2_interfaces.srv import Snapshot

class FaultSnapshot(Node):
    def __init__(self):
        super().__init__("fault_snapshot")
        self.cli = self.create_client(Snapshot, "/rosbag2_recorder/snapshot")
        self.sub = self.create_subscription(DiagnosticArray, "/diagnostics", self.cb, 10)
        self.cooldown_until = self.get_clock().now()

    def cb(self, msg):
        now = self.get_clock().now()
        if now < self.cooldown_until:
            return
        for s in msg.status:
            if s.level >= DiagnosticStatus.ERROR:
                self.get_logger().error(f"fault from {s.name}: {s.message} -> snapshot")
                self.cli.call_async(Snapshot.Request())
                # 30 s cooldown so a flapping diagnostic doesn't write 50 bags
                self.cooldown_until = now + rclpy.duration.Duration(seconds=30)
                break

def main():
    rclpy.init()
    rclpy.spin(FaultSnapshot())
```

### Writing MCAP directly (non-ROS robots — Python on a Pi/Jetson)

```python
# pip install mcap mcap-protobuf-support   (or use JSON schema for zero deps)
from mcap.writer import Writer
import json, time

f = open("run.mcap", "wb")
w = Writer(f)
w.start()
schema = w.register_schema(
    name="robot.Telemetry", encoding="jsonschema",
    data=json.dumps({"type": "object", "properties": {
        "vbat": {"type": "number"}, "rpm_l": {"type": "number"},
        "rpm_r": {"type": "number"}, "mode": {"type": "string"}}}).encode())
chan = w.register_channel(topic="/telemetry", message_encoding="json", schema_id=schema)

def emit(rec: dict):
    ns = time.time_ns()
    w.add_message(channel_id=chan, log_time=ns, publish_time=ns,
                  data=json.dumps(rec).encode())

emit({"vbat": 12.4, "rpm_l": 1450, "rpm_r": 1455, "mode": "AUTO"})
w.finish(); f.close()
```

This file opens directly in Foxglove with zero ROS installed. For MCU-class devices, log
JSON-lines (§1) and convert to MCAP offline with the same pattern.

---

## 4. Foxglove Workflows

- **Offline:** open the `.mcap` directly in Foxglove (desktop app or studio web). Instant
  seek thanks to MCAP chunk index. Sqlite3 bags need conversion: `ros2 bag convert` with an
  output storage of mcap, or the `mcap` CLI (`mcap convert old.db3 out.mcap`).
- **Live (ROS 2):** `ros2 launch foxglove_bridge foxglove_bridge_launch.xml port:=8765`
  then connect Foxglove → "Foxglove WebSocket" → `ws://<robot-ip>:8765`. Prefer
  foxglove_bridge over the old rosbridge — it's binary CDR, ~10× less CPU and no JSON
  conversion losses.
- **Live (non-ROS):** the `foxglove` Python SDK (`pip install foxglove-sdk`) starts a
  WebSocket server speaking the same protocol; log dicts against a JSON schema like §3.
- **Panels that earn their keep:** Plot (drag any numeric field), 3D (TF + meshes + point
  clouds), Diagnostics (renders `/diagnostics` tree natively), State Transitions (perfect
  for your INFO-level mode-change events), Log panel on `/rosout` (filter ≥ WARN).
- **Layout discipline:** save a per-robot layout JSON in the repo (`tools/foxglove_layout.json`).
  "Open bag, import layout, look" beats 10 minutes of panel-dragging per incident.

## 5. PlotJuggler Workflows

PlotJuggler is the better tool for control-loop tuning (PID traces, step response):

```bash
sudo apt install ros-$ROS_DISTRO-plotjuggler-ros
ros2 run plotjuggler plotjuggler          # File→Load: bag; or Streaming→ROS2 topics
```

- Loads MCAP and sqlite3 bags, plus CSV and JSON-lines (your MCU logs from §1 load directly —
  configure the timestamp field as `t` when prompted).
- Killer feature — **derived series**: right-click → "Custom transforms", e.g.
  `sqrt(odom.twist.linear.x^2 + odom.twist.linear.y^2)` for speed, or error = setpoint − measured.
- Second killer feature — **XY plots**: plot `/odom x` vs `y` for the actual path driven.
- For live streaming over flaky Wi-Fi, PlotJuggler's WebSocket/UDP server input + your robot
  sending JSON-lines over UDP is far more robust than full DDS discovery across subnets.

---

## 6. Time Correlation — Sim vs Wall, MCU vs Host

The class of bug this section prevents: "the bag says the obstacle appeared at t=1718041023
but the controller log says it reacted at t=43.7" — uncorrelatable garbage.

**The three clocks:**
1. **Wall clock** — epoch time. Right answer for everything fleet/multi-device, but only after NTP sync.
2. **ROS time** — equals wall clock unless `use_sim_time:=true`, in which case it follows `/clock`.
3. **MCU monotonic** — `millis()`/`time.ticks_ms()`; starts at 0 at boot, drifts ~±50 ppm
   (≈ ±4 s/day on a typical crystal; ESP32 RC-slow-clock variants are far worse).

**Rules:**
- In every ROS node, take time from `node.get_clock().now()` — NEVER `time.time()` and never
  `rclpy.time.Time()` (which is t=0, a classic TF "extrapolation into the past" bug source).
  With `use_sim_time` the node clock follows sim `/clock`; `time.time()` doesn't, and the two
  diverge the moment sim runs ≠ 1× real-time.
- Set `use_sim_time` on ALL nodes or none. One node on wall clock in a sim system causes TF
  extrapolation errors that look like sensor bugs:
  `ros2 launch foo bar.launch.py use_sim_time:=true` must propagate to every node.
- **Bag playback = sim time problem too.** `ros2 bag play --clock 100` publishes `/clock`;
  run your offline stack with `use_sim_time:=true` against it. Forgetting this is the #1
  "works live, breaks in replay" cause.
- MCAP records `log_time` (when recorded) and `publish_time` (header stamp) separately.
  Latency analysis = `log_time − header.stamp`. If header.stamp comes from a sensor's own
  clock (many lidars, cameras with PTP), validate offset before trusting it.

**MCU↔host correlation — the handshake pattern.** Don't NTP the MCU; just measure the offset:

```python
# Host side: estimate offset host_epoch = mcu_ticks_ms/1000 + offset, bounding error by RTT.
import serial, time, json
ser = serial.Serial("/dev/ttyUSB0", 921600, timeout=1)

def sync_offset(n=10):
    best_rtt, best_off = 1e9, 0.0
    for _ in range(n):
        t0 = time.time()
        ser.write(b'{"cmd":"ping"}\n')
        resp = json.loads(ser.readline())        # MCU replies {"pong": ticks_ms}
        t1 = time.time()
        rtt = t1 - t0
        if rtt < best_rtt:                       # keep the tightest sample
            best_rtt = rtt
            best_off = (t0 + t1) / 2 - resp["pong"] / 1000.0
    return best_off, best_rtt                    # offset valid to ±rtt/2

offset, rtt = sync_offset()
# Re-sync every ~60 s and on every reconnect; log the offset itself so post-hoc
# correction is possible. 50 ppm drift = 3 ms/min — re-sync interval sets your error bar.
```

Apply `t_epoch = mcu_ms/1000 + offset` at *ingest* time, store both raw and corrected.
On Wi-Fi MCUs (ESP32), `ntptime.settime()` in MicroPython once at boot + the handshake for
fine alignment is the practical optimum (NTP gets you ±50 ms over Wi-Fi; handshake over
serial gets ±1–2 ms).

**Robot host clock:** install `chrony`, not `ntpd` (chrony handles intermittent connectivity
and steps the clock sanely at boot). For multi-sensor rigs needing < 1 ms (lidar+camera
fusion), use PTP (`linuxptp`) on a wired segment; Wi-Fi cannot do PTP meaningfully.
**Log a marker event when the clock steps** — chrony stepping the clock 30 s forward
mid-mission otherwise looks like a 30 s sensor dropout in the bag.

---

## 7. Fleet Uplink — MQTT with a Bandwidth Budget

Architecture that works: **full-rate logging stays on the robot** (MCAP/flash, §2–3);
the uplink carries *downsampled state + events + fault dumps on demand*. Never stream
full-rate telemetry over a cell link — you'll blow the data cap in a day:

Budget math: 50 topics × 10 Hz × 100 B = 50 KB/s = 4.3 GB/day per robot. Downsampled to
the table below: ~200 B/s sustained = 17 MB/day. That's the difference between viable
and not on a $5/mo cell plan.

| Uplink class       | Content                                   | Rate              |
|--------------------|-------------------------------------------|-------------------|
| heartbeat          | mode, vbat, pose (coarse), error_count    | 0.2 Hz (every 5 s)|
| events             | INFO+ state transitions, WARN+ logs       | event-driven, rate-capped 1/s |
| fault dump         | black-box file (§2) / snapshot bag pointer| on fault only     |
| full telemetry     | everything                                | NEVER over WAN — pull bags over Wi-Fi/dock |

### Topic scheme + QoS

```
fleet/<robot_id>/hb            QoS 0, retained=false   (loss is fine; next one comes in 5 s)
fleet/<robot_id>/evt           QoS 1, retained=false   (must arrive; dup-tolerant consumers)
fleet/<robot_id>/fault         QoS 1, retained=true    (dashboard sees last fault on connect)
fleet/<robot_id>/status        QoS 1, retained=true    ← LWT target, see below
fleet/<robot_id>/cmd/#         QoS 1                   (downlink)
```

- **QoS 2 is almost never worth it** (4-way handshake per message; design consumers to be
  idempotent and use QoS 1).
- **Always set a Last Will:** broker publishes `{"online":false}` to `status` when the robot
  drops without DISCONNECT. This is your fleet-wide liveness for free.
- **Retained + QoS 1 on `status`/`fault`** means a dashboard connecting at 3am immediately
  sees current state without waiting for the next publish.

### MicroPython MQTT uplink with downsampling + change-detection

```python
# uplink.py — ESP32 MicroPython, umqtt.simple
from umqtt.simple import MQTTClient
import json, time

ROBOT = "rbt_007"
last_hb_ms = 0
last_sent = {}

c = MQTTClient(ROBOT, "broker.example.com", port=8883, keepalive=30,
               ssl=True, ssl_params={"server_hostname": "broker.example.com"})
c.set_last_will(b"fleet/%s/status" % ROBOT,
                json.dumps({"online": False}).encode(), retain=True, qos=1)
c.connect()
c.publish(b"fleet/%s/status" % ROBOT,
          json.dumps({"online": True, "fw": "1.4.2"}).encode(), retain=True, qos=1)

def deadband_changed(key, val, band):
    """Send only if changed beyond deadband — cuts steady-state traffic ~90%."""
    prev = last_sent.get(key)
    if prev is None or abs(val - prev) >= band:
        last_sent[key] = val
        return True
    return False

def uplink_tick(state):                      # call from main loop; cheap when nothing to send
    global last_hb_ms
    now = time.ticks_ms()
    if time.ticks_diff(now, last_hb_ms) >= 5000:           # 0.2 Hz heartbeat
        last_hb_ms = now
        hb = {"t": time.time(), "mode": state["mode"],
              "vbat": round(state["vbat"], 2),
              "x": round(state["x"], 1), "y": round(state["y"], 1),   # coarse pose
              "err": state["err_count"]}
        c.publish(b"fleet/%s/hb" % ROBOT, json.dumps(hb).encode(), qos=0)
    if deadband_changed("vbat", state["vbat"], 0.2):       # event on 0.2 V change
        c.publish(b"fleet/%s/evt" % ROBOT,
                  json.dumps({"t": time.time(), "msg": "vbat", "v": round(state["vbat"],2)}).encode(),
                  qos=1)

def uplink_fault(blackbox_path):
    # Small dumps (<100 KB): publish directly, chunked 16 KB (broker max packet limits!).
    # Large dumps: publish a *pointer*, upload the file over HTTPS when on Wi-Fi/dock.
    c.publish(b"fleet/%s/fault" % ROBOT,
              json.dumps({"t": time.time(), "file": blackbox_path,
                          "upload": "pending"}).encode(), qos=1, retain=True)
```

**MQTT mistakes everyone makes:**
1. `keepalive=30` set but main loop blocks > 30 s during, say, motor calibration → broker
   drops you, LWT fires, dashboard shows robot "offline" while it's fine. Call
   `c.ping()`/`check_msg()` from a place that runs during long operations, or keep keepalive ≥ 2× your worst block.
2. Publishing from an ISR/callback context. `umqtt` is not thread/ISR safe — queue and
   publish from the main loop.
3. No reconnect logic. Wrap connect/publish in try/except, back off exponentially
   (1, 2, 4, … 60 s cap), and *buffer events to flash while offline* — replay with original
   timestamps on reconnect (this is why every record carries `t` rather than relying on
   broker receive time).
4. Retained heartbeats. A retained `hb` makes a dead robot look alive. Retain only
   `status` and `fault`.
5. Per-message TLS reconnects on cell links: a TLS handshake costs ~5–6 KB. Keep the
   connection up; with persistent sessions (`clean_session=False`) QoS 1 messages queue
   broker-side across drops.
6. Forgetting broker max packet size (often 1 MB default on Mosquitto, much lower on
   managed brokers) when pushing fault dumps — chunk or use HTTPS for files.

### ROS 2 side: bridge selectively, never wholesale

Use the `mqtt_client` ROS package or a 30-line custom node. Bridge ONLY the downsampled
summary topic — never `ros2 topic` traffic wholesale (DDS-over-WAN is its own circle of hell;
if you truly need ROS-native remote access, that's a zenoh/DDS-router design problem, not MQTT).

```python
# summary_uplink.py — subscribe high-rate, publish low-rate summary
class SummaryUplink(Node):
    def __init__(self):
        super().__init__("summary_uplink")
        self.state = {}
        self.create_subscription(BatteryState, "/battery_state",
            lambda m: self.state.update(vbat=m.voltage), 10)
        self.create_subscription(Odometry, "/odom",
            lambda m: self.state.update(x=m.pose.pose.position.x,
                                        y=m.pose.pose.position.y), 10)
        self.create_timer(5.0, self.tick)          # downsample: publish at 0.2 Hz
        self.mqtt = self._connect_mqtt()           # paho, LWT + reconnect as above

    def tick(self):
        if self.state:
            self.mqtt.publish(f"fleet/{ROBOT}/hb", json.dumps(
                {"t": self.get_clock().now().nanoseconds / 1e9, **self.state}), qos=0)
```

---

## 8. Debugging Checklists

### "My bag is missing messages"
1. `ros2 bag info file.mcap` — is the topic listed with count 0? → QoS mismatch (§3), add overrides.
2. Recorder stderr for `Dropped messages` → raise `--max-cache-size`, use zstd not lz4-none, faster disk.
3. Topic publishing at all during record? `ros2 topic hz /topic` *while recording* (recording adds a subscriber — BEST_EFFORT publishers under load shed to the newest subscriber first).
4. `/tf_static` empty → durability (§3 gotcha #2).
5. Bag ends early/corrupt → disk full (`df -h`), or recorder SIGKILLed (always SIGINT and wait; MCAP recovers partially via `mcap recover`, sqlite3 usually doesn't).

### "Timestamps don't line up"
1. Mixed `use_sim_time` across nodes — `ros2 param get /node use_sim_time` for every node.
2. `header.stamp` zero or boot-relative → driver bug; check whether it stamps from device clock or host.
3. MCU log offset drifting → re-sync interval too long (§6), log offsets and correct post-hoc.
4. 30 s jump in logs → chrony stepped the clock; check `chronyc tracking` / journal.
5. Replay reacts instantly to old data → forgot `--clock` on `ros2 bag play` + `use_sim_time` on consumers.

### "Robot rebooted and I don't know why"
1. Read reset cause FIRST (`machine.reset_cause()` / `esp_reset_reason()`), log it at boot, uplink it.
2. WDT_RESET → pull black-box dump; look at last 2 s for the blocking call.
3. BROWNOUT → power, not software: motor inrush sagging VCC. Scope VCC during motor start; add bulk capacitance (470–1000 µF low-ESR at the driver), separate logic/motor supplies, common ground.
4. No dump on flash → fault path didn't run (hard fault before handler) → noinit-RAM flag pattern (§2), flush on next boot.
5. Random + correlated with Wi-Fi/TLS → heap exhaustion; log free heap in heartbeat (`gc.mem_free()` / `esp_get_free_heap_size()`) and watch the trend.

### "Logging is breaking the robot" (yes, this happens)
1. Loop jitter appears when logging enabled → serial blocking (§1 budget math). Raise baud, log every Nth, or buffer + drain in idle.
2. Heap fragmentation crash after hours → `String` concat in Arduino log path, or per-call dict churn in MicroPython. Fixed buffers / preallocated.
3. SD writes stalling control loop 50–200 ms → never write SD from the control thread; queue to a writer task/second core (ESP32 `xTaskCreatePinnedToCore` on core 0, control on core 1).
4. rosbag recorder eating CPU the nav stack needs → record on a separate machine via network, or `nice -n 10` the recorder and pin nav stack with `taskset`.

---

## 9. Decision Quick-Reference

| Need | Use |
|------|-----|
| MCU event log | JSON-lines over serial (§1) + RAM ring black box (§2) |
| MCU fault forensics | ring flush to LittleFS on fault + reset-cause at boot |
| ROS recording | rosbag2 + MCAP + zstd, explicit topic list, QoS overrides |
| ROS fault forensics | snapshot-mode recorder + diagnostics-triggered service call |
| Non-ROS host recording | `mcap` Python writer, JSON schema |
| Visual debugging | Foxglove (3D/TF/state), PlotJuggler (PID tuning, XY paths, custom transforms) |
| Sim + replay | `use_sim_time` everywhere + `--clock` on play |
| MCU↔host time | ping/pong offset handshake, re-sync ≤ 60 s |
| Host clock | chrony; PTP only on wired |
| Fleet uplink | MQTT: 0.2 Hz heartbeat QoS 0, events QoS 1, LWT + retained status, deadband filters |
| Big files off robot | HTTPS upload on dock/Wi-Fi; MQTT carries the pointer only |
