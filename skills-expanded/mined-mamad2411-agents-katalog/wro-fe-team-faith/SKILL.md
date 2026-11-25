---
name: wro-fe-team-faith
description: >
  Use this skill for ALL tasks related to Team Faith's WRO Future Engineers 2026 project.
  Trigger whenever the user mentions WRO, robot, ESP32, ESP32-S3, OpenMV, Pixy2, PID, servo, FSM, odometry,
  obstacle challenge, open challenge, firmware, sensors, I2C, SPI, UART, camera, encoders, checklist,
  preflight, tuning, competition, AS5600, VL53L1X, ICM-20948, engineering journal, or anything related to
  their autonomous car. This skill contains full project context so Claude can help without re-explanation.
---

# WRO Future Engineers 2026 — Team Faith Skill

## Project Overview
**Team:** Faith
**Competition:** World Robot Olympiad (WRO) Future Engineers 2026
**Category:** Self-Driving Cars (Open Challenge + Obstacle Challenge)
**Repo:** `https://github.com/Disfyy/WRO-Faith-Future-Engineer-`
**Local path:** `/Users/nr_ulan/Desktop/WRO_Project_Pack/`
**Active firmware:** v13 (ESP32-S3 + 2× AS5600 dual-I2C + 2× VL53L1X XSHUT-remap, no I2C mux)
**Active camera (2026-06):** **Pixy2** on UART2 — interim after the OpenMV OV5640 module was damaged ~5 days before competition. OpenMV + ESP32-CAM remain selectable fallbacks; all backends fill the same `g_cam` struct so the FSM/failsafes are backend-agnostic.

> **Status:** bench-test phase. `wro_build_target.h` currently selects `WRO_TARGET_BENCH_TEST` (10); switch to `WRO_TARGET_V13_MAIN` (11) for an actual race build.

---

## Hardware Stack (v13 — current)

| Component | Model | Role |
|---|---|---|
| Main Controller | ESP32-S3-DevKitC-1 N8R8 | PID, odometry, FSM, sensor fusion (dual-core, native USB) |
| Vision (active) | **Pixy2 / 2.1** (UART2) | Color-block tracking: pillars, lines, parking marker |
| Vision (fallback) | OpenMV H7 Plus / ESP32-CAM | Same UART2 link, same `g_cam` output |
| IMU | ICM-20948 (9-DoF) | Heading/yaw, lap counting |
| Encoders | 2× AS5600 magnetic (12-bit, dual I2C) | Odometry (~277 ticks/cm), one per native I2C peripheral |
| Front distance | VL53L1X (I2C, ~3 m Medium mode) | Corner detection + pre-emptive braking |
| Side distance | VL53L1X (I2C) | Wall-follow trim on Open Challenge straights |
| Motor Driver | BTS7960 43A H-Bridge | Drive motor (LEDC PWM, signed) |
| Steering | JX PDI-6221MG Digital Servo | Steering (50 Hz, µs-calibrated) |
| Power | 2S/3S LiPo + 5V step-down | Power supply |

> v12 was a planned migration to AS5048A SPI + TFMini-S; parts never arrived and the v11 TCA9548A I2C mux burned out. **v13** keeps the ESP32-S3 brain and reverts to the v11 sensor stack — 0x36 AS5600 collision solved by the bus split (one per native I2C peripheral), 0x29 VL53L1X collision solved by a boot-time XSHUT address-remap dance in `vl53l1x_dual.h`.

### ESP32-S3 Pin Map (v13 — authoritative: `wro_hw_config_v13.h`)
- **I2C0 (Wire), GPIO 8 / 9:** ICM-20948 (0x68) + AS5600 Left (0x36) + VL53L1X Front (0x29 → 0x30)
- **I2C1 (Wire1), GPIO 3 / 4:** AS5600 Right (0x36) + VL53L1X Side (0x29 → 0x31) — *moved from GPIO 11/12 in 2026-06; GPIO3 is a strapping pin but works for I2C*
- **VL53L1X XSHUT:** GPIO 15 (Front), GPIO 16 (Side), GPIO 47 (reserved 3rd)
- **UART2 (camera, Pixy2/OpenMV/ESP-CAM):** RX = 17, TX = 18, 115200 8N1
- **BTS7960 motor:** R_EN = 38, L_EN = 39, R_PWM = 40 (fwd), L_PWM = 41 (rev)
- **Steering servo:** GPIO 42
- **E-Stop:** GPIO 21 (INPUT_PULLUP) · **Status LED:** GPIO 2 · **RGB WS2812:** GPIO 48

### I2C Address Map (post-boot)
- **I2C0:** 0x68 (IMU), 0x36 (AS5600 L), 0x30 (VL53L1X F)
- **I2C1:** 0x36 (AS5600 R), 0x31 (VL53L1X S)
- AS5600 0x36 collision → sidestepped by the bus split. VL53L1X 0x29 collision → sidestepped by the boot-time XSHUT remap (front released, remapped to 0x30, then side released → 0x31). VL53L1X address is RAM-only, so the dance repeats every reset.

### Servo Calibration (bench-recal 2026-06-11, `wro_hw_config_v13.h`)
- `SERVO_CENTER_US = 1350`, `SERVO_LEFT_US = 1000`, `SERVO_RIGHT_US = 1700` (symmetric ±350 µs travel)
- `SERVO_MARGIN_US = 60` → safe limits `SERVO_LEFT_SAFE_US`/`SERVO_RIGHT_SAFE_US` keep the horn off the mechanical end-stops (end-stop stall = brownout). Re-measure with **target 7** (`diag_test_servo_calibrate_v13.cpp`).

---

## Software Architecture

### Two independent processors
1. **Vision (camera MCU):** `src/openmv/openmv_main.py` (OpenMV/ESP-CAM text path) and the on-ESP `wro_camera_pixy2.cpp` (Pixy2 binary block path). Both deliver: red/green pillars (X + distance), orange/blue line bits (lap direction), magenta parking block. Normalized into one `CameraData g_cam`. Protocol spec: `docs/guides/WRO_OpenMV_UART_Protocol.md`.
2. **Control (ESP32-S3, C++):** `src/esp32/wro_v13_main.cpp` — modular, layered. Race build = `WRO_TARGET_V13_MAIN` (11).

### Layered architecture (top-down only)
```
HAL          as5600_dual_i2c.h · vl53l1x_dual.h · ICM20948 lib · wro_i2c_buses.h
Estimation   wro_imu · wro_odometry · wro_sensors · wro_camera(+_pixy2)
Behavior     wro_corner · wro_behavior_open · wro_behavior_obstacle · wro_park
Control      wro_v13_main (steering mixer + speed ramp + steering-asymmetry trim)
FSM          wro_race_fsm (top) + wro_estop (parallel) + wro_telemetry(+_wifi)
```

### Camera data contract (`wro_camera.h`)
- `redX/greenX`: −80..79 px (cx−80 on a 160-px frame); "not seen" ⇒ `redDist/greenDist == 999`.
- `modeFlag` bits: `1`=orange line (CW), `2`=blue line (CCW), `4`=magenta parking. Bit 3 reserved (wall detection moved to VL53L1X in v13).
- `extraTag`: magenta block X (used to pick the parking-bay side).
- **Pixy2 signature order** (teach in PixyMon, this exact order): `1`=red pillar, `2`=green, `3`=orange line, `4`=blue line, `5`=magenta parking. **Set Data-out port = UART @ 115200** (factory default is 19200!).

---

## Round Logic — Top-Level Race FSM (`wro_race_fsm.cpp`)

Challenge is a **compile-time** flag only (Rule 9.9 — no physical switches): `OBSTACLE_MODE` in `wro_config_v13.h` (`0` = Open, `1` = Obstacle).

State enum order (also the telemetry `ST=` codes): `INIT(0) → WAIT(1) → RUN_O(2) | RUN_X(3) → [TURN(4) reserved] → PARK(5) → FIN(6)`, plus `STOP(7) = SAFE_STOP` (parallel).

| State | Behavior |
|---|---|
| **RS_INIT** | Servo centered, motor off. Advances to WAIT_START only when IMU+encoders healthy **and** the front VL53L1X booted (no front ToF ⇒ corner FSM never commits ⇒ wall crash). |
| **RS_WAIT_START** | Idle; optionally pre-rolls camera direction detection. On E-Stop **start** press: reset odo, rebase gyro-lap baseline + heading grid to current yaw, then enter `RUN_OPEN` or `RUN_OBS` per `OBSTACLE_MODE`. |
| **RS_RUN_OPEN** | Open Challenge straights + corners. Finishes at `lap ≥ TARGET_LAPS_RACE` (3) → FINISH. |
| **RS_RUN_OBS** | Obstacle Challenge straights + pillar avoidance + corners. Camera-silent > `CAM_SILENT_STOP_MS` (3 s) → SAFE_STOP. After lap 3 + magenta confirmed → PARKING. |
| **RS_PARKING** | Parallel-park sub-FSM. `park_done()`/`park_aborted()` → FINISH. |
| **RS_FINISH** | Stop, clear race-active. |
| **RS_SAFE_STOP** | Motor off immediately (not through ramp). Resumes the prior running state on E-Stop release (PIDs/corner reset, timeout clocks re-anchored); pre-race trap escapes back to WAIT_START. |

**Lap counter (`updateLapCounter`):** primary = gyro accumulator `|g_yaw_total − raceStartYawTotal| / GYRO_LAP_DEG(360)` with `LAP_COOLDOWN_MS` (3 s) between credits and a monotonic high-water mark (a crossing inside cooldown is credited late, never lost). Camera orange/blue line bit is a **secondary sanity check** within `LAP_LINE_GRACE_MS`, never the primary trigger.

**Direction detection (`detectDirection`):** votes once per **camera frame** (not per FSM tick); requires an *exclusive* color — orange→CW(+1), blue→CCW(−1) — held `DIRECTION_CONFIRM_FRAMES` (4) in a row; ambiguous frames decay both votes. Until confirmed, falls back to `DEFAULT_RACE_DIRECTION` (−1, CCW) and prints a one-shot warning if a corner starts unconfirmed.

### Corner sub-FSM (`wro_corner.cpp`) — runs *inside* RUN_OPEN/RUN_OBS
Distance-sensor + IMU only — **camera is never a corner trigger or exit** (that was the v11 turn failure).
`CN_ARMED → CN_SLOWDOWN → CN_COMMIT → CN_BRAKE → CN_EXECUTE → CN_EXIT → CN_LOCKOUT` (+ `CN_FAIL`).
- **Arm/slowdown:** front `< TURN_SLOWDOWN_MM` (600).
- **Commit:** front `< TURN_COMMIT_MM` (420 — matte-black walls only return valid frames ~420 mm) for `TURN_FRAMES_DEBOUNCE` (3) frames → capture `turnStartYaw`.
- **Brake-straight:** `TURN_BRAKE_MS` (100) at PWM 0.
- **Execute:** full lock toward `turnDirection` at `TURN_SPEED_PWM` (70 — slip is what cost the v11 turn). Exit when `|yaw − turnStartYaw| ≥ TURN_TARGET_DEG` (80°; heading-hold cleans the last ~10°). **Panic → CN_FAIL** if wall `< TURN_PANIC_MM` (100) or `> TURN_MAX_MS` (2500). `CN_FAIL` → race FSM SAFE_STOP.
- **Lockout:** suppress re-detect for `TURN_LOCKOUT_MS` (800) after exit. On exit it raises `g_corner_just_exited` so the race FSM snaps the new heading target to the 90° grid (anchored to race-start yaw, not absolute 0/90).

### Open Challenge behavior (`wro_behavior_open.cpp`)
Gyro heading-hold PID (`HEADING_KP 12 µs/°`, `KD 2`, `KI 0` — drift over 3 min) toward the post-corner snapped target. Optional **side-wall trim** (`HAS_SIDE_TOF=1`): hold `WALL_TARGET_MM` (100) with `WALL_KP 0.40`, clamped ±`WALL_TERM_CLAMP_US` (150); ignore side reads > `WALL_MAX_VALID_MM` (400 — randomized inner walls show 1–3 m across gaps). Sign convention: +yaw = CCW/left, larger µs = right ⇒ the heading term carries a **minus**.

### Obstacle Challenge behavior (`wro_behavior_obstacle.cpp`)
Pillar-avoidance PID on camera X. **Pass-side rule:** RED → vehicle passes the pillar's RIGHT, so hold the pillar **left** of center (setpoint `−PILLAR_OFFSET_PX`, −30 px); GREEN → passes LEFT, hold pillar **right** (+30 px). Gains `PILLAR_KP 0.45 / KI 0.001 / KD 0.30` (EMA-filtered derivative, α 0.30); reset integral on color switch; pick the **closer** pillar, add a `PILLAR_FAR_GAIN` (0.40) pre-position term from the far pillar. No pillar → blend toward heading-hold over `PILLAR_BLEND_OUT_MS` (250). Hard brake if front `< PILLAR_SAFETY_FRONT_MM` (200).

### Parking sub-FSM (`wro_park.cpp`) — Obstacle only, after lap 3
Triggered when `lap ≥ 3` **and** magenta seen `PARK_MAGENTA_CONFIRM` (5) camera frames in a row **and not mid-corner**.
`PK_APPROACH → PK_ALIGN → PK_REV_A → PK_REV_B → PK_REV_C → PK_FINAL` (+ `PK_ABORT`).
- **APPROACH:** heading-hold creep forward; pick bay side from magenta X (`extraTag` sign); stop at back-wall (front < 250 mm). Timeout `PARK_APPROACH_MAX_MS` (6 s) → ABORT.
- **ALIGN:** wait until yaw-rate `< PARK_ALIGN_RATE_DPS` (2 °/s) for 200 ms; `PARK_ALIGN_MAX_MS` (4 s) timeout proceeds anyway (gyro bias may never settle after a 3-min run).
- **REV_A:** reverse + steer into bay `PARK_PHASE_A_CM` (25, encoder-measured).
- **REV_B:** counter-steer until heading aligns (or `PARK_PHASE_B_MS` 1500 cap).
- **REV_C:** straight back until `PARK_PHASE_C_CM` (45 total) **or** front clears > `PARK_FRONT_CLEAR_MM` (350). Steering sign **flips to +** here (reversing inverts the steer↔yaw relation).
- Phase completion is **encoder-distance** based; the `*_MS` values are failsafe caps that survive an E-Stop pause via `park_shift_clock()`.

---

## Key Tunables (`src/esp32/wro_config_v13.h`)
```cpp
OBSTACLE_MODE        0      // 0 = Open, 1 = Obstacle (the ONLY mode switch — Rule 9.9)
HAS_SIDE_TOF         1      // side VL53L1X wired by default in v13
DEFAULT_RACE_DIRECTION (-1) // fallback until camera locks orange/blue (-1=CCW, +1=CW)

TURN_SLOWDOWN_MM     600
TURN_COMMIT_MM       420    // was 350 — matte-black walls only return valid frames ~420 mm
TURN_TARGET_DEG      80
TURN_SPEED_PWM       70     // slip-limited
OPEN_MAX_PWM         65     // testing value for short black-wall range; raise toward 80 via S+
OBS_MAX_PWM          130
SPEED_RAMP_STEP      8      // PWM/10 ms · MIN_DRIVE_PWM 35 deadband floor
PILLAR_OFFSET_PX     30     // camera X is ±80, not ±160
PILLAR_KP 0.45 / KI 0.001 / KD 0.30 (EMA 0.30)
HEADING_KP 12.0 / KD 2.0 / KI 0.0
STEER_GAIN_LEFT/RIGHT 1.00  // steering asymmetry trim (live-tune L/R, clamp 0.5..1.5)
TARGET_LAPS_RACE     3      // GYRO_LAP_DEG 360, LAP_COOLDOWN_MS 3000
LOOP_INTERVAL_MS     10     // WDT_TIMEOUT_MS 200 (hardware task watchdog)
ESTOP_BYPASS_AUTOSTART 0    // BENCH-ONLY — MUST be 0 for any run that can move
WIFI_TELEMETRY       1      // TESTING-ONLY — MUST be 0 for competition (Rule 11.10)
CAMERA_BACKEND       PIXY2  // revert to OPENMV if the OpenMV module is revived
```

---

## Repository Structure (v13)
```
src/esp32/
  wro_v13_main.cpp         # active main firmware (target 11): setup/loop, steering+motor write, ramp
  wro_race_fsm.{cpp,h}     # top-level race FSM + lap/direction logic
  wro_corner.{cpp,h}       # cornering sub-FSM (distance + IMU)
  wro_behavior_open.{cpp,h}     # Open Challenge heading-hold + wall trim
  wro_behavior_obstacle.{cpp,h} # Obstacle pillar-avoidance PID
  wro_park.{cpp,h}         # parallel-park sub-FSM
  wro_estop.{cpp,h}        # E-Stop / start-button logic (parallel)
  wro_imu.{cpp,h} wro_odometry.{cpp,h} wro_sensors.{cpp,h}  # estimation
  wro_camera.{cpp,h}       # OpenMV/ESP-CAM UART text parser → g_cam
  wro_camera_pixy2.cpp     # Pixy2 binary block parser → g_cam (active backend)
  wro_steering_comp.h      # steering asymmetry trim
  wro_telemetry.{cpp,h}    # 5 Hz telemetry + USB live-tune commands
  wro_telemetry_wifi.{cpp,h} # Wi-Fi UDP mirror (testing only; no-op when WIFI_TELEMETRY=0)
  wro_pid.h wro_i2c_buses.h
  wro_hw_config_v13.h      # pin map + addresses + servo cal + odometry
  wro_config_v13.h         # tunables + OBSTACLE_MODE + HAS_SIDE_TOF + CAMERA_BACKEND
  wro_build_target.h       # target selector
  as5600_dual_i2c.h vl53l1x_dual.h  # HAL drivers
  diag_*.cpp               # bench/test targets (see below)
  legacy/                  # v11 archived sources (targets 1,4,5,6)
src/openmv/openmv_main.py  # MicroPython vision (OpenMV/ESP-CAM path)
docs/  schemes/  models/   # guides+checklists+logs / wiring / CAD (+ models/Pixy2_mount/)
```

### Build Targets (`wro_build_target.h`)
| # | Target | Notes |
|---|--------|-------|
| 2 | SCAN_I2C | both buses — `diag_scan_i2c_v13.cpp` |
| 3 | TEST_MOTOR_SERVO_DRIVE | v11 code via root shim |
| 7 | TEST_SERVO_CAL | v13 — `diag_test_servo_calibrate_v13.cpp` |
| 8 | TEST_ENCODERS | AS5600 dual I2C |
| 9 | TEST_VL53L1X | front + side, XSHUT remap |
| 10 | BENCH_TEST | all sensors + actuators ← **currently active** |
| 11 | V13_MAIN | race firmware (Open + Obstacle) |
| 12 | TEST_CAMERA | UART2 link/frame/checksum verdict |
> Targets 1, 4, 5, 6 are archived v11 in `src/esp32/legacy/`.

---

## Live Tuning over USB Serial (115200, newline-terminated)
- `P0.45` / `I0.001` / `D0.30` — pillar PID gains
- `G12.0` — heading PID Kp
- `L1.15` / `R1.00` — steering asymmetry trim (clamped 0.5..1.5)
- `S+` / `S-` — bump both max speeds ±5 (clamped to [deadband, 255])
- `?` — full state dump · `!` — software E-Stop
- Telemetry line (5 Hz, mirrored to Wi-Fi UDP when enabled):
  `T=… ST=… CN=… LAP=… YAW=… DST=L±/R± TF=…mm CAM=R(x,d)/G(x,d) PWM=± ST=…us`

---

## Failsafes (v13)
- **Hardware task watchdog** 200 ms — loop hang (I2C lock-up, library stall) → panic reset instead of a motionless/runaway robot.
- **Front-ToF death** mid-race: silent > `TF_FRONT_DEAD_MS` (3 s) → SAFE_STOP (corner FSM can't commit without it).
- **Sensor health:** IMU or encoder failure → SAFE_STOP (outside INIT/FINISH).
- **Camera silence (Obstacle):** offline > 3 s → SAFE_STOP; during APPROACH > 500 ms → park ABORT.
- **Brownout proxy:** |PWM| > deadband but speed < 5 cm/s too long → warn.
- **E-Stop:** hardware GPIO 21 (debounced, 500 ms boot grace) **and** software `!`. Immediate motor cut, resumes on release.
- **Rule 11.10:** `WiFi.mode(OFF)` + `btStop()` at boot. `WIFI_TELEMETRY` must be 0 for competition; testing AP = `WRO-FAITH`.

---

## Pre-Flight Sequence (v13, always before run)
1. **Target 2** SCAN_I2C — I2C0 shows 0x68 + 0x36 + 0x30; I2C1 shows 0x36 + 0x31. (0x70 = old TCA9548A, must be GONE.)
2. **Target 8** TEST_ENCODERS — both AS5600 accumulate ticks (one per bus).
3. **Target 9** TEST_VL53L1X — front + side return real mm at remapped addresses.
4. **Target 12** TEST_CAMERA — UART2 frames/blocks flowing, checksum/decode OK (current backend = Pixy2).
5. **Target 10** BENCH_TEST — IMU + encoders + VL53L1X + motor + servo + camera + E-Stop all live.
6. **Target 11** V13_MAIN — wheels-up smoke: heading-hold rotates servo as the chassis is turned by hand.
7. Test E-Stop physically (immediate stop + clean resume); confirm steering centered + motor direction.
8. Wheels off ground first, then floor test. Confirm `ESTOP_BYPASS_AUTOSTART 0` and `WIFI_TELEMETRY 0` for competition.

---

## Common Failure Modes & Fixes (v13)
| Problem | Fix |
|---|---|
| I2C scan finds wrong devices | Expect 0x68+0x36+0x30 on I2C0, 0x36+0x31 on I2C1. 0x70 = dead mux. Check I2C1 is on GPIO 3/4 (moved from 11/12). |
| AS5600 reads −1 / 0 / 4095 | Wrong bus (Wire vs Wire1), magnet gap (0.5–3 mm), polarity, 3.3 V, 4.7 kΩ pull-ups. |
| VL53L1X stuck at 0x29 / never comes up | XSHUT order: front must boot + remap to 0x30 before side is released. Drive XSHUT HIGH only after `setBus()`, before `init()`. |
| Camera frame/decode fail | Backend = Pixy2: UART @ 115200 (not 19200), signature order 1–5, RX/TX crossed, common GND. Distance jump-defense rejects sudden jumps. |
| Robot under/over-rotates corners | Tune `TURN_TARGET_DEG` / `TURN_SPEED_PWM`. NEVER use encoder ticks or camera as the corner exit. |
| Corner aborts (CN_FAIL/panic) on black walls | Valid front frames start ~420 mm; keep `TURN_COMMIT_MM` ≈ 420 and approach slow (`OPEN_MAX_PWM` ~65). |
| Turns weaker one way | Move LiPo (corner-weight) first, then trim with `STEER_GAIN_LEFT/RIGHT` (L/R live). Expect 1.10–1.25, never 2.0. |
| Strong oscillation on straights | Lower `HEADING_KP`, raise `HEADING_KD`, reduce speed. |
| Heading drift over 3 min | ICM-20948 gyro Z drifts with motor heat; snap-to-90° after each corner mitigates. Re-cal on a still surface. |

---

## How Claude Should Help
- Always reference real paths in `/Users/nr_ulan/Desktop/WRO_Project_Pack/`; read `wro_hw_config_v13.h`, `wro_config_v13.h`, `wro_v13_main.cpp` before answering hardware/code questions.
- Treat **v13** as current. Treat `src/esp32/legacy/legacy_*.cpp` and any v11/v12 references in older docs as historical.
- Remember the active camera backend is **Pixy2** (`CAMERA_BACKEND_PIXY2`); OpenMV/ESP-CAM are fallbacks feeding the same `g_cam`.
- Remember I2C topology: AS5600 L + IMU + VL53L1X Front on Wire (I2C0, GPIO 8/9); AS5600 R + VL53L1X Side on Wire1 (I2C1, **GPIO 3/4**). VL53L1X addresses are remapped at boot (all start at 0x29).
- Cornering trigger/exit must stay **distance-sensor + IMU** based — do NOT regress to camera-gated triggers or encoder-distance exits.
- Use the v13 tunables above; follow the pre-flight target order (2 → 8 → 9 → 12 → 10 → 11).
- Keep WRO rule compliance in mind: Rule 9.9 (compile-time mode only), single start button, Rule 11.10 (no wireless during runs — `WIFI_TELEMETRY 0`).
- Suggest logging results to the CSV files in `docs/logs/`; push engineering-journal time (worth points) and practice runs.
