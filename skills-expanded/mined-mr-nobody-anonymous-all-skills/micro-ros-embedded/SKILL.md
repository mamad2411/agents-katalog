---
name: micro-ros-embedded
description: "Use when integrating ESP32, Raspberry Pi Pico, or STM32 microcontrollers with ROS 2 via micro-ROS — agent/client setup, serial vs UDP transports, colcon.meta memory tuning, FreeRTOS executor patterns, custom messages, or deciding when a plain serial bridge is the better choice. Provides exact transport configs, memory budgets, working rclc code, reconnection patterns, and debugging checklists for the failure modes that consume days (agent handshake loops, middleware memory exhaustion, QoS mismatches, time-sync drift)."
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


# micro-ROS on Embedded Targets (ESP32 / Pico / STM32)

micro-ROS puts a real ROS 2 node (rclc + Micro XRCE-DDS client) on a microcontroller.
It talks to a **micro-ros-agent** on the host, which bridges XRCE-DDS to full DDS.
The MCU is a first-class graph participant: `ros2 topic list` shows its topics,
`ros2 node info` shows it, parameters and services work.

**Cost of that:** ~35–80 KB RAM, ~250 KB flash, a brittle session handshake, and
build complexity. Read "When NOT to use micro-ROS" before committing.

---

## 1. Architecture — what actually runs where

```
┌──────────── MCU ────────────┐      serial/UDP      ┌──────── Host (Linux) ────────┐
│ app task(s)                 │  XRCE-DDS protocol   │ micro-ros-agent              │
│   └─ rclc executor          │ <==================> │   └─ FastDDS participant     │
│       └─ rcl / rmw_microxrce│                      │         └─ ROS 2 graph (DDS) │
│            └─ uxr client    │                      │ other ROS 2 nodes            │
│ transport (UART/WiFi UDP)   │                      └──────────────────────────────┘
└─────────────────────────────┘
```

Key consequences everyone misses:

1. **No agent = no node.** The MCU cannot publish, subscribe, or even finish
   `rclc_node_init_default()` without a live agent session. Plan for this in
   your state machine (Section 7).
2. **All entity creation is static-by-default.** Publishers, subscribers,
   services are allocated from pools sized at *compile time* via `colcon.meta`
   (Section 5). Exceeding a pool returns `RCL_RET_ERROR` with zero useful detail.
3. **The agent does QoS translation.** XRCE "reliable" streams map to DDS
   reliable; "best-effort" maps to best-effort. A reliable micro-ROS publisher
   will NOT match a best-effort host subscriber unless you align QoS (Section 9).
4. **Message memory is yours.** rclc does not allocate string/sequence storage
   for incoming messages. Unassigned `msg.data.data` pointer = hard fault on
   first message. (Section 8 — the #1 crash in the field.)

### Version pairing — non-negotiable

Agent and client must be the **same ROS 2 distro**. Humble client + Jazzy agent
fails the session handshake silently (agent logs show repeated
`session established` / `session re-established` or nothing at all).

| Distro | Status (2026) | Notes |
|--------|---------------|-------|
| Humble | LTS, most tested on ESP32/Pico | safest choice |
| Iron   | EOL | avoid |
| Jazzy  | LTS | fine, ensure component/lib version matches |
| Rolling| moving target | only if you rebuild firmware lib often |

Run the agent in Docker to guarantee pairing:

```bash
# Serial (adjust device + baud; -v6 gives per-message logging)
docker run -it --rm --device=/dev/ttyUSB0 microros/micro-ros-agent:humble \
  serial --dev /dev/ttyUSB0 -b 115200 -v6

# UDP (WiFi targets)
docker run -it --rm --net=host microros/micro-ros-agent:humble \
  udp4 --port 8888 -v6
```

`--net=host` is mandatory for UDP — port mapping (`-p 8888:8888/udp`) breaks the
return path because the agent replies to the source addr/port it saw.

---

## 2. Transport selection

| Transport | Targets | Throughput (practical) | Latency | Use when |
|-----------|---------|------------------------|---------|----------|
| Serial UART 115200 | all | ~8 KB/s usable | 2–10 ms | default, debugging |
| Serial UART 921600 | ESP32, STM32 | ~70 KB/s | 1–3 ms | IMU @ 200 Hz+, multiple topics |
| USB CDC | Pico, STM32 (USB FS) | ~500 KB/s | 1–2 ms | best wired option on Pico |
| UDP4 over WiFi | ESP32 | ~100+ KB/s | 5–50 ms (jitter!) | untethered robots |
| UDP4 over Ethernet | STM32 + LwIP | ~1 MB/s | <2 ms | industrial, deterministic |
| Custom (CAN, RS-485) | STM32 | varies | varies | you implement 4 callbacks |

Hard rules:

- **WiFi UDP jitter makes it unsuitable for control loops > 50 Hz.** Run the
  PID on the MCU; send setpoints/state over micro-ROS at 10–50 Hz.
- **Serial payload budget:** at 115200 baud you get ~11.5 KB/s raw. A 32-byte
  msg + ~20 bytes XRCE/framing overhead at 100 Hz = 5.2 KB/s — already 45% of
  the link. Budget before you pick rates. Bump to 921600 or 460800 early.
- **ESP32 UART0 is the boot/log UART.** Use it for micro-ROS only if you
  disable ESP-IDF console logging (`CONFIG_ESP_CONSOLE_NONE=y`), otherwise boot
  messages corrupt XRCE framing and the session never establishes. Prefer
  UART1/UART2 on spare pins, or UDP.

### Serial wiring (UART transport to a USB-UART adapter)

| MCU pin | Adapter | Notes |
|---------|---------|-------|
| TX | RX | cross over |
| RX | TX | cross over |
| GND | GND | ALWAYS — floating ground = garbage bytes |
| — | VCC | do NOT power MCU from adapter unless current budget checked (ESP32 WiFi peaks 500 mA; most CP2102 boards supply ≤100 mA on 3V3) |

All three chips are 3.3 V logic. 5 V adapter TX into ESP32/Pico RX will work
for a while, then kill the pin. Check the adapter jumper.

### Pico USB transport (platformio / pico-sdk)

The Pico has no WiFi (non-W) — USB CDC is the right transport. With
`micro_ros_platformio`:

```ini
; platformio.ini
[env:pico]
platform = raspberrypi
board = pico
framework = arduino
lib_deps = https://github.com/micro-ROS/micro_ros_platformio
board_microros_transport = serial      ; CDC shows up as Serial on Pico
board_microros_distro = humble
```

Then on the host: `serial --dev /dev/ttyACM0 -b 115200` (baud is ignored for
CDC but the flag is required).

### ESP32 UDP transport (micro_ros_platformio / Arduino)

```cpp
#include <micro_ros_platformio.h>
IPAddress agent_ip(192, 168, 1, 50);   // host running the agent
const uint16_t agent_port = 8888;

void setup() {
  set_microros_wifi_transports("SSID", "PASS", agent_ip, agent_port);
  // blocks until WiFi connects; does NOT block on agent — handle that yourself
}
```

ESP-IDF component equivalent: set `CONFIG_MICRO_ROS_AGENT_IP` /
`CONFIG_MICRO_ROS_AGENT_PORT` via menuconfig, transport `udp`.

### Custom transport (STM32 CAN/RS-485/anything)

Implement four functions and register them — this is the entire contract:

```c
bool my_open(struct uxrCustomTransport* t);
bool my_close(struct uxrCustomTransport* t);
size_t my_write(struct uxrCustomTransport* t, const uint8_t* buf, size_t len, uint8_t* err);
size_t my_read(struct uxrCustomTransport* t, uint8_t* buf, size_t len, int timeout_ms, uint8_t* err);

rmw_uros_set_custom_transport(
  true,            // framing: true for stream transports (UART), false for packet (UDP/CAN-FD)
  &my_args, my_open, my_close, my_write, my_read);
```

Framing flag gotcha: stream transports need `true` (enables HDLC-like framing
with 0x7E delimiters). Packet-oriented transports need `false`. Wrong flag =
agent sees garbage, no session, no error message.

---

## 3. When plain serial bridge beats micro-ROS — decide honestly

micro-ROS is the right tool when you need ≥2 of: parameters, services,
multiple topics, ROS time on the MCU, discovery in the graph, lifecycle.

A plain serial protocol + a tiny host-side ROS 2 Python node is better when:

| Situation | Why bridge wins |
|-----------|-----------------|
| 1–3 topics, fixed schema (e.g. cmd_vel in, odom + IMU out) | 200 lines total vs build system + agent + memory tuning |
| RAM < 100 KB free (small STM32F0/F1, ATmega — micro-ROS won't fit at all on AVR) | rclc+rmw needs ~35 KB minimum, realistically 50–80 KB |
| Hard-real-time control loop on the MCU | XRCE session servicing inside `rclc_executor_spin_some` adds jitter |
| Team can't maintain a colcon/ESP-IDF/pico-sdk firmware build | Arduino sketch + pyserial is maintainable by anyone |
| Flaky link (long RS-485 run, lossy radio) | you control retry/CRC policy; XRCE reliable streams stall hard on loss |
| You only need telemetry logging | rosbag the bridge node's output |

Reference bridge pattern (this is the whole thing — COBS-framed binary, CRC16):

```python
# host_bridge.py — ROS 2 node, ~60 lines, replaces micro-ROS for simple cases
import struct, serial, rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from cobs import cobs  # pip install cobs

PKT_IMU = 0x01   # mcu->host: <B 6f H> = id, ax ay az gx gy gz, crc16
PKT_CMD = 0x10   # host->mcu: <B 2f H> = id, lin_x ang_z, crc16

def crc16(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return crc

class Bridge(Node):
    def __init__(self):
        super().__init__('mcu_bridge')
        self.ser = serial.Serial('/dev/ttyUSB0', 921600, timeout=0.005)
        self.imu_pub = self.create_publisher(Imu, 'imu/data_raw', 10)
        self.create_subscription(Twist, 'cmd_vel', self.on_cmd, 10)
        self.buf = bytearray()
        self.create_timer(0.002, self.poll)         # 500 Hz poll

    def on_cmd(self, msg):
        body = struct.pack('<B2f', PKT_CMD, msg.linear.x, msg.angular.z)
        body += struct.pack('<H', crc16(body))
        self.ser.write(cobs.encode(body) + b'\x00')

    def poll(self):
        self.buf += self.ser.read(256)
        while b'\x00' in self.buf:
            frame, _, self.buf = self.buf.partition(b'\x00')
            try: pkt = cobs.decode(bytes(frame))
            except Exception: continue
            if len(pkt) < 3 or crc16(pkt[:-2]) != struct.unpack('<H', pkt[-2:])[0]:
                continue
            if pkt[0] == PKT_IMU and len(pkt) == 27:
                ax, ay, az, gx, gy, gz = struct.unpack('<6f', pkt[1:25])
                m = Imu()
                m.header.stamp = self.get_clock().now().to_msg()
                m.header.frame_id = 'imu_link'
                m.linear_acceleration.x, m.linear_acceleration.y, m.linear_acceleration.z = ax, ay, az
                m.angular_velocity.x, m.angular_velocity.y, m.angular_velocity.z = gx, gy, gz
                self.imu_pub.publish(m)

rclpy.init(); rclpy.spin(Bridge())
```

MCU side is a matching `struct.pack` in C plus the same CRC. Done. If the spec
later grows services/params, *then* migrate to micro-ROS.

---

## 4. Canonical client code (rclc, FreeRTOS / Arduino loop)

This is the reference skeleton — publisher + subscriber + timer, with the error
macro discipline and message memory done correctly.

```cpp
#include <micro_ros_platformio.h>      // or <micro_ros_arduino.h> / ESP-IDF component
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/int32.h>
#include <geometry_msgs/msg/twist.h>

rcl_publisher_t pub;
rcl_subscription_t sub;
rcl_timer_t timer;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;

std_msgs__msg__Int32 pub_msg;
geometry_msgs__msg__Twist cmd_msg;     // POD message: no extra memory needed

#define RCCHECK(fn) { rcl_ret_t rc = fn; if (rc != RCL_RET_OK) { error_loop(rc); } }
#define RCSOFTCHECK(fn) { rcl_ret_t rc = fn; (void)rc; }  // for periodic calls

void error_loop(rcl_ret_t rc) {
  // DON'T just while(1). Blink + reboot so a transient agent loss self-heals.
  for (int i = 0; i < 10; i++) { digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN)); delay(100); }
  ESP.restart();   // Pico: watchdog_reboot(0,0,0); STM32: NVIC_SystemReset();
}

void cmd_cb(const void* msgin) {
  const geometry_msgs__msg__Twist* m = (const geometry_msgs__msg__Twist*)msgin;
  set_motor_targets(m->linear.x, m->angular.z);   // keep callbacks SHORT
}

void timer_cb(rcl_timer_t* t, int64_t last_call_time) {
  (void)last_call_time;
  if (t == NULL) return;
  pub_msg.data++;
  RCSOFTCHECK(rcl_publish(&pub, &pub_msg, NULL));
}

void setup() {
  set_microros_serial_transports(Serial);  // or wifi transport, Section 2
  delay(2000);                              // let transport settle

  allocator = rcl_get_default_allocator();
  RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));
  RCCHECK(rclc_node_init_default(&node, "esp32_node", "", &support));

  RCCHECK(rclc_publisher_init_default(&pub, &node,
      ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32), "mcu/heartbeat"));

  RCCHECK(rclc_subscription_init_default(&sub, &node,
      ROSIDL_GET_MSG_TYPE_SUPPORT(geometry_msgs, msg, Twist), "cmd_vel"));

  RCCHECK(rclc_timer_init_default(&timer, &support,
      RCL_MS_TO_NS(50), timer_cb));          // 20 Hz publish

  // handles = subscriptions + timers + services + clients + guard_conditions
  // Count EXACTLY. Too few -> rclc_executor_add_* returns RCL_RET_ERROR.
  RCCHECK(rclc_executor_init(&executor, &support.context, 2, &allocator));
  RCCHECK(rclc_executor_add_subscription(&executor, &sub, &cmd_msg, &cmd_cb, ON_NEW_DATA));
  RCCHECK(rclc_executor_add_timer(&executor, &timer));
}

void loop() {
  // 10 ms budget: services transport+executor. Do NOT block elsewhere in loop().
  RCSOFTCHECK(rclc_executor_spin_some(&executor, RCL_MS_TO_NS(10)));
}
```

### FreeRTOS task layout (ESP-IDF / STM32+FreeRTOS)

One task owns ALL rclc/rcl calls. rclc is **not thread-safe**; calling
`rcl_publish` from a second task while the executor spins corrupts the XRCE
session stream.

```c
// Correct pattern: other tasks push to a queue; the micro-ROS task publishes.
void microros_task(void* arg) {            // stack: 4096 words ESP32 (16 KB) min
  // ... init as above ...
  sensor_sample_t s;
  while (1) {
    if (xQueueReceive(sensor_q, &s, 0) == pdTRUE) {
      imu_msg.linear_acceleration.x = s.ax; /* ... */
      rcl_publish(&imu_pub, &imu_msg, NULL);
    }
    rclc_executor_spin_some(&executor, RCL_MS_TO_NS(5));
    vTaskDelay(pdMS_TO_TICKS(1));           // yield; never starve IDLE task
  }
}
// Priority: above app tasks that feed it, below hard-RT control ISR/task.
// ESP32: pin to core 1 if WiFi (core 0) is busy: xTaskCreatePinnedToCore(..., 1);
```

Stack sizing: micro-ROS task needs ≥ 8 KB on STM32, ≥ 16 KB on ESP32 (printf +
WiFi stack frames). `uxTaskGetStackHighWaterMark` after 5 min of traffic; keep
≥ 1 KB headroom. Stack overflow here manifests as random hard faults during
`rcl_publish`, not at init.

---

## 5. Memory tuning — colcon.meta

micro-ROS statically pools all middleware entities. Defaults (varies by port,
roughly): 1 node, 5 publishers, 5 subscribers, 5 services, 5 clients,
512-byte streams. Exceed any pool → init returns `RCL_RET_ERROR`.

`colcon.meta` (ESP-IDF component: `app-colcon.meta` in project root;
micro_ros_setup firmware builds: edit then **full clean rebuild** — these are
compile-time constants, `pio run` alone will NOT pick them up; delete
`.pio/libdeps/*/micro_ros_platformio/libmicroros` or run
`ros2 run micro_ros_setup build_firmware.sh` after changes):

```json
{
  "names": {
    "rmw_microxrcedds": {
      "cmake-args": [
        "-DRMW_UXRCE_MAX_NODES=1",
        "-DRMW_UXRCE_MAX_PUBLISHERS=4",
        "-DRMW_UXRCE_MAX_SUBSCRIPTIONS=3",
        "-DRMW_UXRCE_MAX_SERVICES=1",
        "-DRMW_UXRCE_MAX_CLIENTS=1",
        "-DRMW_UXRCE_MAX_HISTORY=4",
        "-DRMW_UXRCE_TRANSPORT=custom",
        "-DRMW_UXRCE_STREAM_HISTORY=4",
        "-DRMW_UXRCE_MAX_TRANSPORT_MTU=512"
      ]
    },
    "microxrcedds_client": {
      "cmake-args": ["-DUCLIENT_PROFILE_MULTITHREAD=OFF"]
    }
  }
}
```

Sizing rules:

- **RAM per entity** ≈ MTU × STREAM_HISTORY for each reliable stream, plus
  ~1–2 KB bookkeeping per pub/sub. With MTU=512, HISTORY=4: ~2 KB per direction.
- **MAX_TRANSPORT_MTU must exceed your largest serialized message** + ~64 B
  overhead, OR the message gets fragmented across stream history slots. A
  message larger than `MTU × STREAM_HISTORY` can NEVER be sent — publish
  returns OK but nothing arrives (best-effort) or the stream stalls (reliable).
  E.g. `sensor_msgs/LaserScan` with 360 floats ≈ 1.5 KB serialized → needs
  MTU=512, HISTORY≥4, or MTU=2048.
- **MAX_HISTORY** is per-topic sample slots, separate from STREAM_HISTORY
  (transport buffers). Publishing faster than the link drains with HISTORY=1
  silently drops samples.
- Realistic budgets: minimal node (1 pub, 1 sub, int32s) ~35 KB RAM. Typical
  robot node (odom + imu pub, cmd_vel sub, 1 service) ~55–70 KB. LaserScan
  publisher ~85 KB+. Pico (264 KB RAM) is comfortable; STM32F4 (128–192 KB)
  needs the tuning above; STM32F1 (20 KB) cannot run micro-ROS — use a bridge.

---

## 6. QoS and rclc entity variants

| rclc init call | DDS QoS | Use for |
|---|---|---|
| `rclc_publisher_init_default` | reliable, keep-last | state, events, services-ish data |
| `rclc_publisher_init_best_effort` | best-effort | high-rate sensors (IMU, encoders) |
| `rclc_subscription_init_default` | reliable | cmd topics where loss matters |
| `rclc_subscription_init_best_effort` | best-effort | matching sensor streams |

Rules:

- **Best-effort pub on the MCU + `ros2 topic echo` works** (echo defaults
  compatible), but a host node subscribing reliable will get NOTHING — no
  error, no warning on the MCU side. Check with
  `ros2 topic info /topic -v` (shows QoS of every endpoint).
- High-rate sensor data: best-effort, always. Reliable streams over serial
  retry on every dropped byte and create multi-second backlogs; the symptom is
  "topic was fine for 2 minutes then latency grew unbounded".
- Reliable publishes **block** in `rcl_publish` until acked or session timeout
  when the stream is full. On a saturated 115200 link this freezes your loop
  for hundreds of ms. Another reason control loops stay local.

---

## 7. Agent reconnection — the state machine you must write

The default examples die permanently when the agent restarts. Production
firmware needs this (works on all three platforms):

```cpp
enum class AgentState { WAITING, AVAILABLE, CONNECTED, DISCONNECTED };
AgentState state = AgentState::WAITING;

#define EXECUTE_EVERY_N_MS(MS, X) do { \
  static int64_t t = -1; \
  if (t == -1) t = uxr_millis(); \
  if (uxr_millis() - t > MS) { X; t = uxr_millis(); } } while (0)

void loop() {
  switch (state) {
    case AgentState::WAITING:
      EXECUTE_EVERY_N_MS(500,
        state = (RMW_RET_OK == rmw_uros_ping_agent(100, 1))
                ? AgentState::AVAILABLE : AgentState::WAITING);
      break;
    case AgentState::AVAILABLE:
      state = create_entities() ? AgentState::CONNECTED : AgentState::WAITING;
      if (state == AgentState::WAITING) destroy_entities();
      break;
    case AgentState::CONNECTED:
      EXECUTE_EVERY_N_MS(2000,
        state = (RMW_RET_OK == rmw_uros_ping_agent(100, 3))
                ? AgentState::CONNECTED : AgentState::DISCONNECTED);
      if (state == AgentState::CONNECTED)
        rclc_executor_spin_some(&executor, RCL_MS_TO_NS(10));
      break;
    case AgentState::DISCONNECTED:
      stop_motors();                     // SAFETY: never coast on link loss
      destroy_entities();
      state = AgentState::WAITING;
      break;
  }
}

void destroy_entities() {
  rmw_context_t* ctx = rcl_context_get_rmw_context(&support.context);
  (void)rmw_uros_set_context_entity_destroy_session_timeout(ctx, 0); // don't wait for acks
  rcl_publisher_fini(&pub, &node);
  rcl_subscription_fini(&sub, &node);
  rcl_timer_fini(&timer);
  rclc_executor_fini(&executor);
  rcl_node_fini(&node);
  rclc_support_fini(&support);
}
```

Critical details:

- `rmw_uros_ping_agent(timeout_ms, attempts)` works **before** any session
  exists — it's the only safe pre-init probe.
- Setting destroy-session timeout to 0 prevents `destroy_entities()` from
  blocking ~10 s per entity when the agent is already gone.
- **Always stop actuators on DISCONNECTED.** Also run an independent cmd_vel
  watchdog: if no cmd received for 500 ms while CONNECTED, stop. Agent alive ≠
  teleop node alive.

---

## 8. Custom and string/sequence messages — the #1 crash source

rclc gives your subscription callback a message struct, but **you** own the
storage for any non-POD field (strings, dynamic arrays). Forgetting this is a
guaranteed hard fault / memory corruption on first message:

```cpp
// WRONG — msg.data.data is NULL, first incoming string faults
std_msgs__msg__String msg;
rclc_executor_add_subscription(&executor, &sub, &msg, &cb, ON_NEW_DATA);

// RIGHT — pre-assign capacity before adding to executor
std_msgs__msg__String msg;
static char buf[128];
msg.data.data = buf;
msg.data.size = 0;
msg.data.capacity = sizeof(buf);
```

Same for sequences (e.g. `sensor_msgs/JointState` on the publish side):

```cpp
sensor_msgs__msg__JointState js;
static double pos[4];
static rosidl_runtime_c__String name_storage[4];
static char name_buf[4][16];
js.position.data = pos; js.position.size = 4; js.position.capacity = 4;
js.name.data = name_storage; js.name.size = 4; js.name.capacity = 4;
for (int i = 0; i < 4; i++) {
  js.name.data[i].data = name_buf[i];
  js.name.data[i].capacity = 16;
  snprintf(name_buf[i], 16, "joint_%d", i);
  js.name.data[i].size = strlen(name_buf[i]);
}
// header.frame_id is ALSO a string — assign it or publishing faults:
static char frame[16] = "base_link";
js.header.frame_id.data = frame; js.header.frame_id.size = 9; js.header.frame_id.capacity = 16;
```

Alternative: `micro_ros_utilities_create_message_memory()` allocates per a
`micro_ros_utilities_memory_conf_t` (set `max_string_capacity`,
`max_ros2_type_sequence_capacity`). Convenient, but heap-based — prefer static
assignment on small targets.

### Adding a custom message package

1. Put your `my_msgs/` package (with `msg/*.msg`, `CMakeLists.txt`,
   `package.xml` — standard rosidl package, **C only**, no rosidl_python) in:
   - platformio: `extra_packages/` directory next to `platformio.ini`
   - ESP-IDF component: `components/micro_ros_espidf_component/extra_packages/`
   - micro_ros_setup: `firmware/mcu_ws/` then rebuild
2. **Full library rebuild required** — the message gets compiled into
   libmicroros. platformio: delete `.pio/libdeps/<env>/micro_ros_platformio/libmicroros`.
3. The SAME package must be built and sourced in the **agent's** workspace
   (or any host node using it). Mismatch symptom: agent prints
   `create_topic ... UNKNOWN topic type` or subscribers match but deserialize garbage.
4. Type hashes must match → build host package on the same distro. Never edit
   a .msg on one side only.

Pitfalls: field name `bool data` works; nested custom types must be in the same
or an extra_packages-included package; `string<=N` bounded strings save you
from the capacity dance above and are strongly preferred on MCUs.

---

## 9. Time sync

MCU epoch starts at 0 at boot. Host nodes doing TF or message_filters will
discard your data ("message too old") unless you sync:

```cpp
// After session established, then periodically (drift ~ppm of crystal):
rmw_uros_sync_session(1000);                 // timeout ms; do every ~60 s

// Stamping:
int64_t ns = rmw_uros_epoch_nanos();
msg.header.stamp.sec = ns / 1000000000LL;
msg.header.stamp.nanosec = ns % 1000000000LL;
```

`rmw_uros_epoch_nanos()` returns 0 if sync never ran — check
`rmw_uros_epoch_synchronized()` first. Sync accuracy over serial: ~1 ms; over
WiFi: ~5–20 ms (jitter). For tighter sensor fusion, timestamp at sample time
with MCU monotonic clock and apply the session offset, don't timestamp at
publish time.

---

## 10. Debugging checklist — run in this order

**Nothing in `ros2 topic list`:**
1. Agent running, same distro as client lib? (`docker ps`, image tag)
2. Agent `-v6`: do you see `session established`? If not → transport problem,
   go to step 4. If yes but no `create_*` lines → client init failing on MCU.
3. Repeated `session re-established` loops → MCU is rebooting (watch its
   serial console on ANOTHER uart) or `error_loop` reset cycle; usually an
   `RCCHECK` failure → check entity pool limits (Section 5) or executor handle
   count.
4. Serial: correct device? Baud matches both sides? `dmesg | tail` after
   replug. Nothing else holding the port (close PlatformIO monitor — the agent
   and a serial monitor cannot share `/dev/ttyUSB0`).
5. ESP32 serial: boot log garbage corrupting framing? Move off UART0 or
   silence console.
6. UDP: agent started with `--net=host`? MCU and host on same subnet? Firewall
   (`sudo ufw allow 8888/udp`)? Ping the MCU's IP.

**Topics listed but `ros2 topic echo` silent:**
7. QoS: `ros2 topic info /t -v` — best-effort pub vs reliable sub?
8. Message larger than MTU × STREAM_HISTORY? (Section 5)
9. ROS_DOMAIN_ID: agent inherits its environment's domain. MCU side doesn't
   set domain — the AGENT's `ROS_DOMAIN_ID` must match your other nodes.
   In Docker: `-e ROS_DOMAIN_ID=42`.

**Subscriber callback never fires:**
10. Executor handle count ≥ actual handles added?
11. Message memory assigned for strings/sequences? (May also crash, Section 8)
12. Publishing side QoS mismatch (reliable host pub → best-effort MCU sub is
    fine; check the reverse).

**Random hard faults / WDT resets:**
13. micro-ROS task stack high-water mark (Section 4).
14. rcl calls from multiple tasks? Consolidate.
15. ESP32: WiFi + flash writes + micro-ROS on core 0 → starvation; pin task to
    core 1, feed the task WDT or `vTaskDelay(1)` every loop.
16. Unassigned string capacity in a message you PUBLISH (incl. header.frame_id).

**Worked for minutes, then stalled:**
17. Reliable stream backlog on saturated link → switch sensor topics to
    best-effort, raise baud, or lower rate.
18. Agent restarted and firmware has no reconnection state machine (Section 7).

**Init returns RCL_RET_ERROR with no detail:**
19. Pool exhausted — count your entities vs colcon.meta, remember the clean
    rebuild requirement.
20. `rclc_support_init` specifically failing → no agent reachable; gate init
    behind `rmw_uros_ping_agent`.

---

## 11. Build system quick reference

| Stack | Best for | Library mechanism |
|---|---|---|
| `micro_ros_platformio` | ESP32 + Pico, fastest iteration | lib_deps; auto-builds libmicroros on first compile (needs ~5 min + python3) |
| `micro_ros_arduino` | Arduino IDE diehards | precompiled lib; custom messages require rebuilding the static lib in Docker — painful, prefer platformio |
| `micro_ros_espidf_component` | ESP-IDF projects, production ESP32 | git submodule in `components/`; menuconfig for transport/agent IP |
| pico-sdk + `micro_ros_raspberrypi_pico_sdk` | bare pico-sdk C | precompiled libmicroros.a + CMake |
| STM32CubeMX + `micro_ros_stm32cubemx_utils` | STM32 + FreeRTOS | Docker-built static lib; DMA UART transport templates included — use the DMA variant, the IT variant drops bytes above 115200 |
| `micro_ros_setup` | building agent + custom firmware in a ROS 2 ws | `ros2 run micro_ros_setup ...` scripts |

Host agent without Docker:
```bash
sudo apt install ros-humble-micro-ros-agent   # if available, else build via micro_ros_setup
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0 -b 921600 -v6
```

Smoke test once connected:
```bash
ros2 node list                      # expect /esp32_node
ros2 topic hz /mcu/heartbeat        # expect ~20 Hz, steady
ros2 topic pub -r 5 /cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.1}}'
```

---

## 12. Decision summary

```
Need params/services/many topics/ROS time on MCU?
 ├─ no  → plain serial bridge (Section 3). Stop here.
 └─ yes → micro-ROS:
     ├─ RAM ≥ 100 KB free?  no → bridge anyway.
     ├─ Wired & deterministic needed → UART 921600 / USB CDC / Ethernet
     ├─ Untethered ESP32 → WiFi UDP, control loops stay ON the MCU
     ├─ Write colcon.meta BEFORE first build (entity counts, MTU vs biggest msg)
     ├─ One task owns rclc; queues feed it
     ├─ Pre-assign string/sequence memory for every message both directions
     ├─ Implement the reconnection state machine + actuator failsafe
     └─ Sync time before stamping headers
```
