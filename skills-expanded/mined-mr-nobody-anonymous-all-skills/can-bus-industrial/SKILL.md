---
name: can-bus-industrial
description: "Use when wiring, configuring, or debugging CAN bus on robots — actuator networks (ODrive, moteus, T-motor), SocketCAN on Linux, CANopen vs raw CAN, CAN-FD, DBC decoding, bitrate/cable-length limits, and termination failures. Provides field-proven setup values, decoding patterns, and the debugging methodology for bus-off, error frames, and intermittent dropouts."
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


# CAN Bus for Robotics — Industrial-Grade Setup, Decoding, and Debugging

CAN (Controller Area Network) is the de facto actuator bus in modern robotics: quadruped legs,
humanoid joints, AMR drive bases, robot arm joints. If you are putting more than two motor
controllers on one cable, you are almost certainly using CAN. This skill covers everything an
engineer (or an AI agent writing their firmware/host code) must get right the first time, because
CAN failures on real hardware are often silent, intermittent, and destructive (a missed torque
command on a balancing robot = the robot falls).

---

## 1. Why CAN beats serial (UART/RS-485) for actuators

| Property | UART point-to-point | RS-485 multi-drop | CAN 2.0B | CAN-FD |
|---|---|---|---|---|
| Topology | 1:1 only | multi-drop, master/slave | true multi-master | true multi-master |
| Arbitration | none (collisions = garbage) | software token/polling | hardware priority arbitration, non-destructive | same |
| Error detection | parity at best | CRC if you write it | 15-bit CRC, bit-stuffing check, ACK, form check — Hamming distance 6 | 17/21-bit CRC |
| Error handling | none | none | automatic retransmit, error confinement (error-passive, bus-off) | same |
| Max payload/frame | unlimited stream | unlimited stream | 8 bytes | 64 bytes |
| Typical robot use | debug console | legacy servos (Dynamixel) | actuator command/feedback | high-rate actuator buses |

The three properties that matter for robots:

1. **Priority arbitration is non-destructive and deterministic.** Every frame has an ID; lower
   numeric ID wins arbitration bit-by-bit with zero bus time lost. Put your e-stop / disable
   command at the lowest ID on the bus and it *will* get through even on a saturated bus. RS-485
   has no equivalent — a polling master that hangs takes the whole bus with it.
2. **Hardware error containment.** A node with a failing transceiver progressively silences
   itself (error-active → error-passive at TEC/REC ≥ 128 → bus-off at TEC ≥ 256) instead of
   jamming the bus. One dead motor controller does not take down the other 11 joints.
3. **Multi-drop with per-node addressing in hardware.** One twisted pair daisy-chained through
   12 joints, with hardware acceptance filters so each MCU only wakes for its own IDs.

When CAN is the wrong choice: payloads > 64 bytes at high rate (camera/lidar — use Ethernet),
or > ~70% sustained bus load (split into multiple buses; quadrupeds commonly run one CAN bus
per leg, 3 actuators each).

### Bus load math (do this before you commit to a topology)

A classic CAN 2.0 frame with 8 data bytes is ~111–135 bits on the wire (with worst-case bit
stuffing). At 1 Mbit/s that's ~130 µs/frame, so the bus carries **~7,400 max-size frames/s** at
100% load. Keep design load ≤ 50–70%.

Worked example — 6-DOF arm, 1 kHz command + 1 kHz feedback per joint, 8-byte frames:
- Frames/s = 6 joints × 2 directions × 1000 Hz = 12,000 frames/s
- Bus time = 12,000 × 130 µs = 1.56 s/s → **156% load. Impossible.**
- Fixes: drop to 500 Hz (78% — still too hot), split into 2 buses of 3 joints (78% → 39% each
  at 500 Hz, or 78% each at 1 kHz — borderline), or use CAN-FD at 5 Mbit/s data phase.

This calculation is the single most-skipped step. Do it every time.

---

## 2. Physical layer: the rules that prevent 90% of field failures

### Bitrate vs cable length

Arbitration requires the signal to propagate to the far end and back within one bit time.
Rule of thumb (ISO 11898-2, 5 ns/m propagation):

| Bitrate | Max bus length (practical) |
|---|---|
| 1 Mbit/s | 25–40 m |
| 500 kbit/s | 100 m |
| 250 kbit/s | 250 m |
| 125 kbit/s | 500 m |

Robots are short (< 5 m), so run 1 Mbit/s for classic CAN. CAN-FD data phase can go 2–8 Mbit/s
because only the arbitration phase needs round-trip timing.

**Stub length matters more than people think.** Each unterminated stub (drop from the main line
to a node) should be < 0.3 m at 1 Mbit/s. Star topologies are out of spec — daisy-chain through
each actuator (most robot actuators expose two CAN connectors precisely for pass-through).

### Termination — the #1 setup failure

The bus must be terminated with **one 120 Ω resistor at each physical end** of the main line.
Total parallel resistance measured between CAN_H and CAN_L **with all power off** must be **60 Ω**.

Failure modes and their symptoms:

| Measured CANH–CANL resistance | Cause | Symptom |
|---|---|---|
| ~60 Ω | correct (2 × 120 Ω) | — |
| ~120 Ω | only one terminator | works on the bench (short cable), error frames and intermittent drops on the robot; gets worse with cable length and bitrate |
| ~40 Ω | three terminators (someone left a DIP switch on) | marginal differential voltage, error-passive nodes, random ACK errors |
| ~30 Ω or less | many devices shipped with termination enabled | bus barely works or transmits nothing |
| open/MΩ | no termination | reflections; may "work" at 125 kbit/s on 30 cm of wire, will absolutely fail at 1 Mbit/s |

**Always physically measure 60 Ω before first power-on.** ODrive, moteus dev kits, many T-motor
drivers, USB-CAN adapters (Canable, PCAN) ship with termination jumpers/switches in inconsistent
default states. On a 4-actuator leg bus: terminate at the host adapter and at the last actuator;
disable termination on the middle two.

Also non-negotiable:
- **Common ground.** CAN is differential but transceivers need CANH/CANL within their common-mode
  range (typically −2 to +7 V vs local GND). Run a ground wire alongside the pair. Battery-powered
  actuators with separate host power are the classic miss.
- **Twisted pair**, ~120 Ω characteristic impedance. Untwisted ribbon cable near brushless motor
  phase wires = EMI-induced error frames exactly when current spikes (i.e., exactly when you need
  torque). Route CAN away from phase wires; cross at 90° if you must cross.
- Shielding: connect shield to chassis ground at **one end only** to avoid ground loops.

---

## 3. Raw CAN vs CANopen vs vendor protocols

Three layers you'll meet in robotics:

1. **Raw CAN with a vendor frame layout** — moteus, T-motor/CubeMars (MIT mini-cheetah protocol),
   most research actuators. You pack bytes yourself per the datasheet. Simple, fast, no stack.
2. **CANopen (CiA 301 + CiA 402 motion profile)** — industrial drives (maxon EPOS, Elmo, Kinco,
   Festo, many AGV motors). Standardized object dictionary, SDO (config, request/response),
   PDO (cyclic realtime data), NMT (network state machine), heartbeat. Use a stack
   (`python-canopen`, CANopenNode in C, Lely in C++); do not hand-roll SDO segmented transfers.
3. **DroneCAN / Cyphal (formerly UAVCAN)** — drones and some mobile robots. Pub/sub over CAN.

How to tell what you have: CANopen nodes emit a **boot-up message** on ID `0x700 + node_id` with
one byte `0x00` at power-on, and respond to SDO requests on `0x600 + node_id`. Vendor-raw devices
just sit silent or stream telemetry on fixed IDs.

### CANopen survival kit (CiA 402 drives)

Predefined connection set (11-bit IDs):

| Function | COB-ID |
|---|---|
| NMT | 0x000 |
| SYNC | 0x080 |
| EMCY | 0x080 + node |
| TPDO1 / RPDO1 | 0x180 + node / 0x200 + node |
| TPDO2 / RPDO2 | 0x280 + node / 0x300 + node |
| SDO tx / rx (server) | 0x580 + node / 0x600 + node |
| Heartbeat / boot-up | 0x700 + node |

CiA 402 state machine you must walk to enable a drive (via controlword 0x6040):
`Shutdown (0x06)` → `Switch On (0x07)` → `Enable Operation (0x0F)`. Read statusword 0x6041 and
verify each transition; drives that fault return to `Fault` state and need `Fault Reset (0x80)`
first. Skipping statusword verification is how people write code that enables on the bench and
deadlocks on the robot.

```python
# python-canopen: minimal CiA 402 enable + cyclic velocity
import canopen
net = canopen.Network()
net.connect(channel="can0", bustype="socketcan")
node = net.add_node(3, "drive.eds")   # EDS file from the vendor — always get it

node.nmt.state = "PRE-OPERATIONAL"
node.sdo[0x6060].raw = 9              # mode: cyclic synchronous velocity (CSV)
node.nmt.state = "OPERATIONAL"

for cw in (0x06, 0x07, 0x0F):         # walk the 402 state machine
    node.sdo[0x6040].raw = cw
    # verify statusword bits before proceeding (poll 0x6041)

node.sdo[0x60FF].raw = 100000         # target velocity, in drive units — check 0x6092 factors!
```

**Unit trap:** CiA 402 position/velocity are in *drive-internal units* (encoder counts,
counts/s) scaled by factor objects (0x6091/0x6092/0x608F). Always read the factors or compute
counts-per-rad explicitly. Sending "1.0" expecting rad/s and getting 1 count/s (or 1 full turn/s)
is a top-3 first-day bug.

When to choose what: raw vendor protocol for research/agile robots (lowest latency, simplest);
CANopen when you buy industrial drives or need multi-vendor interop; never write your own
"protocol on CAN" if a vendor one exists.

---

## 4. SocketCAN on Linux — the host-side standard

SocketCAN makes CAN interfaces look like network interfaces. It is the right answer on any Linux
host (Jetson, RPi, industrial PC). Avoid vendor character-device drivers when a SocketCAN driver
exists (PCAN, Kvaser, Canable/candleLight gs_usb, MCP2515/MCP251xFD SPI all have mainline drivers).

### Bring-up (classic CAN, 1 Mbit/s)

```bash
sudo ip link set can0 down
sudo ip link set can0 type can bitrate 1000000
sudo ip link set can0 up
ip -details -statistics link show can0   # check state, error counters, berr-counter
```

CAN-FD (1 M arbitration / 5 M data — the moteus standard):

```bash
sudo ip link set can0 type can bitrate 1000000 dbitrate 5000000 fd on
sudo ip link set can0 up
```

Production settings you should almost always add:

```bash
# Auto-recover from bus-off after 100 ms instead of staying dead forever:
sudo ip link set can0 type can bitrate 1000000 restart-ms 100
# Increase TX queue (default 10 frames is tiny for bursty senders):
sudo ip link set can0 txqueuelen 1000
```

Persist via systemd-networkd (`/etc/systemd/network/80-can.network`):

```ini
[Match]
Name=can0
[CAN]
BitRate=1M
DataBitRate=5M
FDMode=yes
RestartSec=100ms
```

### can-utils — your oscilloscope for frames

```bash
candump can0                       # watch everything
candump -td -e can0,123:7FF        # filter ID 0x123, show delta-time and error frames
cansend can0 123#DEADBEEF          # send 4 bytes
cansend can0 123##1DEADBEEF        # CAN-FD frame (## + flags nibble)
cangen can0 -g 1 -I 42 -L 8        # load generator — soak-test your wiring at target load
canbusload can0@1000000 -r -t      # live bus load %
```

### python-can patterns (correct, not just working)

```python
import can

bus = can.Bus(channel="can0", interface="socketcan", fd=True)

# Hardware/kernel-level filtering — do NOT filter in Python on a busy bus
bus.set_filters([{"can_id": 0x180, "can_mask": 0x700}])  # all TPDO1s

msg = can.Message(arbitration_id=0x123, data=b"\x01\x02", is_extended_id=False)
bus.send(msg, timeout=0.01)       # ALWAYS pass timeout; default blocks forever on full queue

m = bus.recv(timeout=0.01)        # ALWAYS pass timeout; check m is not None
if m is not None and m.is_error_frame:
    ...                            # count these; >0/s in steady state = wiring/termination issue
```

The two `python-can` mistakes that bite robots:
1. **Blocking forever.** `bus.recv()` with no timeout hangs your control loop when a node dies.
   Every CAN call in a control loop needs a timeout shorter than your control period.
2. **Userspace filtering.** Receiving all frames and `if msg.arbitration_id == ...` in Python
   burns a CPU core at 70% bus load. Use `set_filters` (maps to kernel `CAN_RAW_FILTER`).

For C/C++ realtime loops, use raw `socket(PF_CAN, SOCK_RAW, CAN_RAW)` with `read()`/`write()`,
set `SO_RCVTIMEO`, and pin the thread. For ROS 2, `ros2_socketcan` provides
`socket_can_receiver/sender` nodes publishing `can_msgs/Frame`; for drives prefer `ros2_canopen`
(CiA 402 device profile → `ros2_control` hardware interface) over hand-rolling frames in a node.

### Latency reality check

USB-CAN adapters add 0.1–1 ms+ jitter per direction (USB polling). A 1 kHz torque loop through a
$30 USB adapter will have outliers. For hard 1 kHz control: use a PCIe/SPI CAN controller
(MCP251xFD on SPI, or SoC-native CAN like the Jetson's mttcan), an RT-PREEMPT kernel, or push the
tight loop onto an embedded bridge (e.g., moteus pi3hat: SPI from Pi to 5 independent CAN-FD buses
— this is *why* it exists).

---

## 5. DBC files and decoding

A DBC file is the industry-standard machine-readable description of frame layouts: which signal
lives at which bit, scale, offset, unit, endianness. Write one for every bus you build — it turns
`candump` hex soup into named engineering units and makes logs analyzable forever.

```dbc
VERSION "robot_leg_v1"
BO_ 256 JOINT1_CMD: 8 HOST
 SG_ torque_cmd : 0|16@1- (0.001,0) [-30|30] "Nm" JOINT1
 SG_ kp : 16|12@1+ (0.1,0) [0|409] "Nm/rad" JOINT1
BO_ 384 JOINT1_STATE: 8 JOINT1
 SG_ position : 0|16@1- (0.0001,0) [-3.2|3.2] "rad" HOST
 SG_ velocity : 16|16@1- (0.001,0) [-32|32] "rad/s" HOST
 SG_ temp_fet : 48|8@1+ (1,-40) [-40|215] "degC" HOST
```

Syntax decoder: `start_bit|length@endianness sign (scale,offset) [min|max] "unit"`.
`@1` = little-endian (Intel), `@0` = big-endian (Motorola). **Motorola start-bit numbering is the
classic foot-gun** — the start bit counts down across bytes in MSB-first sawtooth order. Don't
hand-compute it; let `cantools` or Vector CANdb++ do it, then verify with a known frame.

```python
import cantools, can
db = cantools.database.load_file("robot.dbc")
bus = can.Bus(channel="can0", interface="socketcan")
m = bus.recv(1.0)
print(db.decode_message(m.arbitration_id, m.data))
# {'position': 1.5708, 'velocity': -0.25, 'temp_fet': 42}

data = db.encode_message("JOINT1_CMD", {"torque_cmd": 2.5, "kp": 50.0})
bus.send(can.Message(arbitration_id=0x100, data=data, is_extended_id=False))
```

Decode verification ritual (do this once per new DBC/device): command a known small value, read it
back, check sign and magnitude. Sign-extension and endianness errors produce values that are
*plausible but wrong* — a torque of −0.012 instead of +0.012 will be discovered by your robot's
mechanics, expensively.

Logging: `candump -l can0` writes `.log` files; replay with `canplayer -I file.log`; analyze with
`cantools decode` or load into Python/pandas. Log raw frames, decode offline — never log decoded
values only, or you can't re-decode after a DBC fix.

---

## 6. CAN-FD

CAN-FD changes two things: payload up to **64 bytes**, and a **bit-rate switch (BRS)** so the data
phase runs faster (2–8 Mbit/s) than arbitration (1 Mbit/s). Effective throughput ≈ 6–8× classic CAN.

Robotics implications:
- One 64-byte frame can carry full state (position, velocity, torque, temps, fault bits) or a full
  command set for a multi-DOF device — fewer frames, less arbitration overhead, lower jitter.
- moteus is CAN-FD native (5 Mbit/s data). T-motor/CubeMars and ODrive v3.6 are classic CAN.
  **CAN-FD frames poison classic-CAN nodes**: a classic controller treats FD frames as errors and
  will error-flag every one. You cannot mix FD traffic and classic-only nodes on one bus unless
  every classic node has an FD-tolerant ("FD-passive") transceiver+controller — most don't.
  Plan separate buses.
- CRC is stronger (17/21-bit) but FD is *more* sensitive to bad termination because of the fast
  data phase: a bus that limps along at 1 Mbit/s classic with one terminator will hard-fail at
  5 Mbit/s FD. Also set the **transceiver delay compensation (TDC)** on; SocketCAN does this via
  `tdc-mode auto` on recent kernels if the driver supports it — symptoms of missing TDC are CRC
  errors only at high data bitrates.
- Sample point: keep arbitration phase ~87.5%, data phase ~75% as starting values. Mismatched
  sample points between nodes cause errors that appear only above certain bus loads.

---

## 7. Motor drivers that speak CAN — field notes

### ODrive (v3.6 / S1 / Pro)
- Protocol: "CANSimple" — 11-bit ID = `(axis_node_id << 5) | cmd_id`. So node 0 commands live at
  0x00–0x1F, node 1 at 0x20–0x3F. **Max ~63 nodes, and a node-id collision shows up as two boards
  answering interleaved garbage.** Set `axis.config.can.node_id` uniquely and save config.
- Classic CAN only on v3.6 (250k default — change it; S1/Pro support FD). Set
  `odrv0.can.config.baud_rate = 1000000` and reboot.
- Key frames: `0x00C` Set_Input_Pos, `0x00D` Set_Input_Vel, `0x00E` Set_Input_Torque (cmd_id part),
  heartbeat `0x001` carries axis error + state — **watch the heartbeat; its error field is your
  only async fault notification.**
- Gotcha: ODrive requires entering `CLOSED_LOOP_CONTROL` (state 8) via Set_Axis_State and will
  silently ignore torque commands in IDLE. Always confirm state from the heartbeat before
  streaming commands.

### moteus (mjbots)
- CAN-FD only (1 M/5 M default), multiplex register protocol over FD frames; use the `moteus`
  Python library — don't hand-pack.
- **Watchdog: position-mode commands time out after 100 ms by default** (`servo.default_timeout_s`)
  and the controller faults (mode 11 / timeout). This is a safety feature: your host loop must
  stream commands faster than the watchdog, or explicitly set the timeout. Never set it to NaN
  (infinite) on a robot that can hurt someone.
- Use `pi3hat` for multi-bus 1 kHz hosts; `tview` for live tuning/telemetry.
- IDs: `id.id` register sets node id; bus runs query/reply (host polls), which makes bus-load
  math easy: one round-trip per servo per cycle.

### T-motor / CubeMars AK-series (MIT mini-cheetah protocol)
- Raw classic CAN, 1 Mbit/s, 8-byte frames. Command packs 5 values into 8 bytes with **fixed-point
  ranges hard-coded per motor model** (e.g., AK80-6: position ±12.5 rad, velocity ±45 rad/s
  (model-specific — check the datasheet for yours), torque ±12 Nm, Kp 0–500, Kd 0–5). Using AK80-9
  constants on an AK70-10 gives silently wrong torques — keep a per-model constants table.
- Enter/exit motor mode with magic frames: `FF FF FF FF FF FF FF FC` (enter), `...FD` (exit),
  `...FE` (zero position). The motor is *torque-live the instant you send FC* — send a zero-torque
  command in the same millisecond and have the e-stop wired first.
- Reply frame packs position/velocity/current in the same fixed-point scheme; position wraps —
  unwrap on the host if you need multi-turn.

```python
# MIT-protocol pack/unpack (host side) — AK80-6 constants
P_MIN,P_MAX,V_MIN,V_MAX,T_MIN,T_MAX = -12.5,12.5,-45.0,45.0,-12.0,12.0  # AK80-6 example; verify per model
KP_MAX, KD_MAX = 500.0, 5.0

def f2u(x, lo, hi, bits):
    x = min(max(x, lo), hi)                      # ALWAYS clamp — overflow wraps to opposite extreme
    return int((x - lo) * ((1 << bits) - 1) / (hi - lo))

def pack_cmd(p, v, kp, kd, t):
    pi, vi = f2u(p,P_MIN,P_MAX,16), f2u(v,V_MIN,V_MAX,12)
    kpi, kdi, ti = f2u(kp,0,KP_MAX,12), f2u(kd,0,KD_MAX,12), f2u(t,T_MIN,T_MAX,12)
    return bytes([pi>>8, pi&0xFF, vi>>4, ((vi&0xF)<<4)|(kpi>>8), kpi&0xFF,
                  kdi>>4, ((kdi&0xF)<<4)|(ti>>8), ti&0xFF])
```

The clamp in `f2u` is load-bearing: an unclamped command of 12.6 rad on a ±12.5 range wraps to
−12.5 rad — a full-authority position slam. This exact bug has broken real robots.

### General multi-vendor rules
- Assign node IDs so **safety-critical broadcast frames have the lowest IDs** (highest priority).
- Document the bitrate of every device in one table; a single 250 kbit/s straggler on a 1 Mbit/s
  bus error-flags continuously and can drag the whole bus to bus-off.
- Power sequencing: actuators that boot while the host floods the bus may miss their own ID
  config; bring the bus up quiet, enumerate (poll each expected node), then start streaming.

---

## 8. Debugging methodology — in order, no skipping

CAN bugs are layered. Debug bottom-up; never tune software while the physical layer is broken.

**Step 0 — Power off, multimeter:** CANH–CANL resistance = 60 Ω (±5). CANH–GND and CANL–GND not
shorted. Continuity end-to-end on both lines and ground.

**Step 1 — Power on, idle voltages:** Recessive bus: CANH ≈ CANL ≈ 2.5 V. Dominant (during
traffic): CANH ≈ 3.5 V, CANL ≈ 1.5 V, differential ≥ 1.5 V at the far end. A differential under
~1.2 V at the far node means over-termination, bad cable, or a weak transceiver.

**Step 2 — Interface state:**
```bash
ip -details -statistics link show can0
```
Read three things: `state` (ERROR-ACTIVE = healthy; ERROR-PASSIVE/BUS-OFF = problem),
`berr-counter` (TEC/REC — nonzero and climbing = active fault), and RX/TX `errors`/`dropped`.

**Step 3 — Listen before you talk:**
```bash
candump -e -td any
```
- *Nothing, ever* → wrong bitrate, dead transceiver, or no other node is transmitting (remember:
  a lone CAN node cannot even ACK itself — `cansend` from a single connected node reports success
  but TEC climbs and the frame repeats forever; you need ≥ 2 nodes for any traffic to complete).
- *Error frames* (`ERRORFRAME`) → decode the class: `bus-error` with `{{{tx}}}` ack-slot errors =
  nobody ACKing (bitrate mismatch or you're alone); stuff/form/CRC errors = physical layer
  (termination, EMI, FD/classic mix).
- *Frames but wrong/garbage IDs* → bitrate is close but wrong (e.g., 500k vs 1M sometimes
  partially decodes), or extended vs standard ID confusion.

**Step 4 — Bisect the bus.** Unplug half the nodes (keep termination valid — carry a 120 Ω plug).
Binary-search for the node that kills the bus. A single device with a wrong bitrate or a damaged
transceiver (common after a phase-wire short) error-flags every frame.

**Step 5 — Load test before integration.** `cangen` at expected load + 20% for 10 minutes while
wiggling the harness. Zero error frames is the pass criterion. EMI faults only appear under motor
load, so repeat with motors spinning under current.

**Step 6 — Only now debug software:** node IDs, DBC bit layouts, state machines, watchdogs.

### Symptom → cause quick table

| Symptom | Most likely cause |
|---|---|
| Works on bench, fails on robot | one terminator missing (longer cable), EMI from phase wires, or ground offset between battery domains |
| Periodic dropout every few seconds | a node hitting bus-off and auto-restarting (`restart-ms`) — find *why* it bus-offs |
| `cansend` "works", nothing received | single node, no ACK — connect a second node or enable loopback to confirm |
| TX queue full / `ENOBUFS` from python-can | bus-off or no ACK; frames never leave; also raise `txqueuelen` |
| Errors only at high motor current | EMI coupling — reroute/twist/shield, check ground |
| Errors only on CAN-FD data phase | termination marginal, TDC off, or sample-point mismatch |
| Two nodes answer the same poll | node-ID collision |
| Values decode plausibly but wrong sign/scale | DBC endianness/sign error, or wrong per-model fixed-point constants |
| Drive accepts config, won't move | CiA 402 state machine not walked / ODrive not in CLOSED_LOOP / moteus watchdog faulted |

Tools worth owning: a USB-CAN adapter with error-frame reporting (candleLight/Canable FD, PCAN,
Kvaser), a 120 Ω terminator plug, and for the hard cases a scope (check rise times, ringing at
the far end) or a CAN-aware analyzer (PCAN-View, SavvyCAN, Vector if budget allows).

---

## 9. Safety patterns for actuator buses (non-negotiable on real robots)

1. **Command watchdog at the actuator.** Every actuator must stop/damp if commands cease for
   N ms (moteus has it default-on; ODrive: enable `axis.config.watchdog_timeout`; MIT-protocol
   motors mostly do NOT have one — your host crash leaves the last torque latched. Mitigate with
   a hardware e-stop on motor power, not just software).
2. **Heartbeat from host, monitored by a supervisor.** Detect host loop stalls independent of CAN.
3. **Lowest-ID disable frame.** Reserve ID 0x000–0x00F for a broadcast disable; it wins every
   arbitration. Send it from the e-stop path.
4. **Bus-off policy.** `restart-ms 100` on the host, but treat any bus-off as a fault to surface,
   not to hide — log and alert.
5. **Startup is the dangerous moment.** Enumerate, verify firmware/protocol versions and node IDs,
   command zero torque, *then* enable. Never enable-and-pray.
6. **Clamp every value at pack time** (see `f2u` above) and validate every value at unpack time
   (range-check before feeding a state estimator — a corrupted frame that passes CRC is rare, a
   software bug that packs garbage is not).

---

## 10. Reference architecture — quadruped leg bus (copy this)

```
Host (Jetson/Pi, RT kernel)
  └─ pi3hat / PCIe-CAN / SPI MCP2518FD     ← not USB for 1 kHz
       ├─ can0: leg FL — hip(id1), thigh(id2), knee(id3)   [120Ω at host + at knee]
       ├─ can1: leg FR — ids 1-3
       ├─ can2: leg RL — ids 1-3
       └─ can3: leg RR — ids 1-3
Bitrate: CAN-FD 1M/5M (moteus) or classic 1M (T-motor)
Loop: 1 kHz query-reply per bus, all 4 buses in parallel threads/DMA
Load per bus (classic, 3 motors, cmd+reply @1kHz): 6,000 × 130µs = 78% — acceptable
  because it's polled (no arbitration contention), but FD drops it to ~20%.
Safety: HW e-stop cuts motor power; SW disable broadcast on ID 0x000; per-motor watchdog.
DBC checked into the repo; candump -l logging on every test run.
```

The decisions encoded here — one bus per leg, no USB, terminators at physical ends, IDs reused
per-bus (1–3) rather than globally unique (simplifies code, valid because buses are independent),
FD where the actuators allow — are the consensus design of every production quadruped team.
Deviate knowingly or not at all.
