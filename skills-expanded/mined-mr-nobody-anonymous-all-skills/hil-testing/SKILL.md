---
name: hil-testing
description: "Use when testing robot software before or during hardware deployment — unit tests with mocked HALs, headless simulation in CI, hardware-in-the-loop (HIL) rigs, clamped-motor bench tests, field test protocols, or scenario regression suites. Provides the full robot test pyramid: mock HAL design patterns (MicroPython + C++ + ROS2), HIL rig wiring and timing budgets, bench-test safety procedures, envelope-expansion field checklists, and the failure modes that only appear on real hardware."
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


# Robot Test Pyramid & Hardware-in-the-Loop Testing

The single most expensive mistake in robotics: testing only on the real robot. The second most expensive: trusting tests that never touch hardware. This skill defines the five-layer test pyramid and exactly how to build each layer so bugs are caught at the cheapest possible level.

## The Pyramid (cost per bug found, bottom = cheapest)

```
        Layer 5: FIELD TESTS          minutes per run, $$$, irreversible mistakes possible
        Layer 4: BENCH TESTS          real robot, clamped/jacked, safe to fail
        Layer 3: HIL RIG              real controller + simulated plant, runs 24/7
        Layer 2: SIM-IN-CI            headless physics sim, every PR
        Layer 1: UNIT + MOCKED HAL    milliseconds, every save
```

**Rule of thumb for coverage allocation:** 70% of test code at Layer 1, 20% at Layers 2–3, 10% at Layers 4–5. A bug found at Layer 5 costs ~100x one found at Layer 1 (travel, setup, battery cycles, broken hardware, and you can't bisect in the field).

**What each layer can and cannot catch:**

| Layer | Catches | CANNOT catch |
|---|---|---|
| 1 Unit/mock | Logic errors, state machines, unit conversions, sign errors | Timing, electrical noise, sensor quirks, race conditions with real ISRs |
| 2 Sim CI | Control instability, planner bugs, integration regressions | Real sensor noise spectra, actuator deadband, comms latency jitter |
| 3 HIL | Driver bugs, timing violations, bus errors, watchdog behavior | Mechanical effects (backlash, flex, slip), thermal drift |
| 4 Bench | Motor direction, encoder polarity, current limits, EMI | Ground interaction, payload dynamics, GPS multipath |
| 5 Field | Everything else | Nothing — but each run costs real time and risk |

---

## Layer 1: Unit Tests with a Mocked HAL

### The HAL seam — design it FIRST

Every testable robot codebase has exactly one seam: a thin Hardware Abstraction Layer interface that all application code talks through. If application code calls `machine.Pin` or `digitalWrite()` directly, you cannot test it. The HAL must be injected, not imported globally.

**MicroPython pattern (works on-device and on desktop CPython):**

```python
# hal.py — the interface. Keep it BORING: raw values, no logic.
class HAL:
    def read_encoder(self, ch: int) -> int: ...          # raw ticks, int32 wrap
    def set_motor_pwm(self, ch: int, duty: float): ...   # -1.0..+1.0
    def read_adc_mv(self, ch: int) -> int: ...           # millivolts
    def ticks_us(self) -> int: ...                       # monotonic, wraps at 2^30 on MP!
    def read_imu(self) -> tuple: ...                     # (ax,ay,az,gx,gy,gz) SI units

# hal_real.py — only file allowed to import `machine`
from machine import Pin, PWM, ADC, I2C
import time
class RealHAL(HAL):
    def ticks_us(self): return time.ticks_us()
    # ... pin bindings live HERE and nowhere else

# hal_mock.py — runs under CPython + pytest
class MockHAL(HAL):
    def __init__(self):
        self.t_us = 0
        self.encoder = [0, 0]
        self.pwm_log = []          # record every command for assertions
        self.adc = [0]*8
    def ticks_us(self): return self.t_us
    def advance(self, us):         # test controls time explicitly
        self.t_us = (self.t_us + us) & 0x3FFFFFFF   # mimic MP 30-bit wrap!
    def set_motor_pwm(self, ch, duty):
        assert -1.0 <= duty <= 1.0, f"duty out of range: {duty}"
        self.pwm_log.append((self.t_us, ch, duty))
    def read_encoder(self, ch): return self.encoder[ch]
```

**Critical detail everyone misses:** MicroPython `time.ticks_us()` wraps at `2**30` (about 17.9 minutes), not `2**32`. Your mock MUST replicate the wrap, and application code MUST use `time.ticks_diff(a, b)` — never `a - b`. A test that advances mock time past 17.9 min catches the entire class of "robot freezes after 18 minutes" bugs:

```python
def test_pid_survives_tick_wrap():
    hal = MockHAL()
    pid = PID(kp=1.0, ki=0.1, kd=0.0, hal=hal)
    hal.t_us = (1 << 30) - 500          # 500 us before wrap
    pid.update(setpoint=100, measured=90)
    hal.advance(1000)                    # crosses the wrap boundary
    out = pid.update(setpoint=100, measured=90)
    assert 0 < out < 10                  # not NaN, not huge — dt computed correctly
```

**Arduino C++ pattern (test on host with plain g++, no Arduino IDE):**

```cpp
// hal.h
struct HAL {
  virtual int32_t  readEncoder(uint8_t ch) = 0;
  virtual void     setMotorPWM(uint8_t ch, float duty) = 0;  // -1..+1
  virtual uint32_t micros() = 0;
  virtual ~HAL() = default;
};

// mock_hal.h — compiled only in tests
struct MockHAL : HAL {
  uint32_t t = 0;
  int32_t enc[2] = {0, 0};
  std::vector<std::tuple<uint32_t,uint8_t,float>> pwmLog;
  uint32_t micros() override { return t; }
  void advance(uint32_t us) { t += us; }   // uint32 wraps naturally at 2^32 — same as AVR/ARM
  void setMotorPWM(uint8_t ch, float d) override { pwmLog.push_back({t, ch, d}); }
  int32_t readEncoder(uint8_t ch) override { return enc[ch]; }
};
```

Build tests with `g++ -std=c++17 test_main.cpp -o tests && ./tests` or platformio: `pio test -e native`. In `platformio.ini`:

```ini
[env:native]
platform = native
test_framework = unity
build_flags = -std=c++17 -DUNIT_TEST
```

`-DUNIT_TEST` guards any `#include <Arduino.h>` so host builds compile clean.

### What to unit test (the high-yield list)

1. **Sign/polarity logic** — "positive PWM = forward" assumptions, encoder direction vs motor direction. #1 source of robots driving backwards.
2. **Unit conversions** — ticks→radians, rad/s→PWM, mV→amps via shunt. Assert with hand-computed numbers: `4096 ticks/rev, gear 30:1 → 1 output rev = 122880 ticks`.
3. **PID anti-windup** — saturate output, verify integrator stops growing. Then release saturation, verify no overshoot spike.
4. **State machines** — every transition, including illegal ones (ESTOP from every state must reach SAFE in one step).
5. **Timer wrap** (see above).
6. **Watchdog/timeout logic** — feed mock time forward past comms timeout, assert motors commanded to zero.
7. **Encoder wrap** — int32 encoder count crossing ±2^31 (happens after ~4.8 hours at 120k ticks/s).
8. **Saturation and clamping** — feed NaN, inf, out-of-range setpoints. Controller must clamp, never propagate NaN to PWM.

```python
def test_estop_zeroes_motors_from_every_state():
    for state in [State.IDLE, State.DRIVING, State.TURNING, State.DOCKING]:
        hal = MockHAL()
        fsm = RobotFSM(hal); fsm.state = state
        fsm.handle(Event.ESTOP)
        assert fsm.state == State.SAFE
        assert hal.pwm_log[-1][2] == 0.0   # last command was zero
```

### ROS 2 unit testing (rclpy / launch_testing)

Mock at the node boundary — never spin a real node graph in unit tests:

```python
# Test the LOGIC class, not the node. Node is a thin shell around it.
class CmdVelMuxLogic:
    def __init__(self, timeout_s=0.5): ...
    def select(self, sources: dict, now_s: float) -> Twist: ...

def test_mux_falls_back_when_teleop_stale():
    mux = CmdVelMuxLogic(timeout_s=0.5)
    out = mux.select({"teleop": (twist(1.0), 0.0), "auto": (twist(0.2), 0.9)}, now_s=1.0)
    assert out.linear.x == 0.2   # teleop is 1.0s old > 0.5s timeout
```

If the node class contains an `if` statement, extract it into a plain class. Nodes should only do: subscribe → call logic → publish.

---

## Layer 2: Headless Simulation in CI

### Architecture rules

- Sim must run **headless** (no GPU, no display) and **faster than real time** where possible. Gazebo: `gz sim -s -r world.sdf` (server only). PyBullet: `p.connect(p.DIRECT)`. Webots: `webots --no-rendering --batch --mode=fast`.
- Pin the physics step and the random seed. Non-deterministic CI sim = useless sim.
- Sim tests assert on **trajectories and invariants**, not pixel-perfect states: "reached goal within 10 cm in <30 s", "max roll never exceeded 15°", "no self-collision events".

```python
# PyBullet headless regression test — runs in plain GitHub Actions, no GPU
import pybullet as p

def run_scenario(seed=42, sim_hz=240, duration_s=20):
    cid = p.connect(p.DIRECT)
    p.setTimeStep(1.0 / sim_hz)
    p.setGravity(0, 0, -9.81)
    p.setPhysicsEngineParameter(deterministicOverlappingPairs=1)
    robot = load_robot(); controller = Controller(seed=seed)
    max_tilt = 0.0
    for i in range(duration_s * sim_hz):
        obs = read_sim_sensors(robot)
        cmd = controller.step(obs, dt=1.0/sim_hz)
        apply_cmd(robot, cmd)
        p.stepSimulation()
        max_tilt = max(max_tilt, tilt_of(robot))
    pose = base_pose(robot); p.disconnect(cid)
    return pose, max_tilt

def test_waypoint_regression():
    pose, max_tilt = run_scenario()
    assert dist(pose, GOAL) < 0.10, f"missed goal by {dist(pose, GOAL):.3f} m"
    assert max_tilt < math.radians(15), f"tilted {math.degrees(max_tilt):.1f}°"
```

### Sensor realism — minimum viable noise model

A sim with perfect sensors validates nothing about your filters. Add at minimum:

| Sensor | Noise to inject | Typical magnitude |
|---|---|---|
| Encoder | quantization to real tick resolution | round to 2π/CPR |
| IMU gyro | white noise + constant bias | σ = 0.005 rad/s, bias = 0.01 rad/s |
| IMU accel | white noise + gravity misalignment | σ = 0.05 m/s², 1° mount error |
| Lidar | range noise + dropout | σ = 1 cm, 2% rays return inf |
| GPS | random walk + 1–5 Hz update | σ = 0.5–2.5 m, 200 ms latency |
| Camera | latency above all else | 50–120 ms pipeline delay |

**Latency matters more than noise.** Inject realistic sensor→controller latency (one or two control periods) in sim. Controllers tuned with zero-latency sim oscillate on hardware. Implement as a deque:

```python
class LatencyBuffer:
    def __init__(self, delay_steps): self.q = collections.deque(maxlen=delay_steps+1)
    def push_pop(self, sample):
        self.q.append(sample)
        return self.q[0]   # returns sample from delay_steps ago
```

### CI wiring (GitHub Actions)

```yaml
jobs:
  sim-regression:
    runs-on: ubuntu-24.04
    timeout-minutes: 20          # ALWAYS set — hung sims eat your minutes
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements-sim.txt
      - run: pytest tests/sim/ -x -q --timeout=120   # per-test timeout via pytest-timeout
      - uses: actions/upload-artifact@v4
        if: failure()
        with: { name: sim-traces, path: traces/*.csv }   # save trajectories for post-mortem
```

Always dump trajectory CSVs on failure. "Test failed, no data" wastes a day; "test failed, here's the trace" takes 10 minutes.

---

## Layer 3: HIL Rig — Real Controller, Simulated Plant

### What a HIL rig is

The actual flight/drive controller (real STM32/RP2040/ESP32/Jetson, real firmware) wired to a PC that simulates the physical plant and synthesizes sensor signals in real time. Firmware cannot tell it's not on a robot. This is where you catch driver bugs, ISR timing violations, bus contention, and watchdog behavior — without ever risking hardware.

### Minimal HIL rig bill of materials (~$50 plus the DUT)

| Item | Purpose | Notes |
|---|---|---|
| Raspberry Pi Pico (RP2040) ×1–2 | sensor emulator: synthesizes quadrature, PWM-in capture, I2C slave | PIO makes it ideal for quadrature generation up to MHz rates |
| USB logic analyzer (fx2lafw, 24 MHz, 8ch) | verify bus timing, PWM duty | $12; sigrok/PulseView |
| USB-UART adapters ×2 | telemetry tap + injection | 3.3 V only — check DUT logic level |
| Programmable load or resistor bank | fake motor load on driver outputs | OR loop PWM back electronically (below) |
| Relay/MOSFET on DUT power | automated power-cycle tests | test brownout recovery! |

### Signal-level HIL wiring (closed loop without motors)

The trick: the controller's **PWM output** is captured by the emulator, fed into the plant model, and the model's resulting position is output as **synthetic quadrature** back into the controller's encoder pins.

```
DUT (controller under test)              Emulator (Pico) + PC
─────────────────────────              ─────────────────────
PWM_A (GPIO out)  ──────────────────▶  PWM capture (PIO in)
DIR   (GPIO out)  ──────────────────▶  GPIO in
ENC_A (GPIO in)   ◀──────────────────  Quadrature gen (PIO out)
ENC_B (GPIO in)   ◀──────────────────  Quadrature gen (PIO out)
GND               ◀─────────────────▶  GND  (COMMON GROUND — non-negotiable)
UART TX           ──────────────────▶  USB-UART → PC logging
                                        Pico ◀─USB─▶ PC running plant model
```

**Plant model on the PC (or directly on the Pico for tight loops):**

```python
# First-order DC motor model — good enough for 95% of HIL work
# omega_dot = (Kt/J)*i - (b/J)*omega ;  i ≈ (V*duty - Ke*omega)/R
class DCMotorPlant:
    def __init__(self, R=1.2, Kt=0.05, Ke=0.05, J=2e-5, b=1e-5, V=12.0, cpr=4096):
        self.omega = 0.0; self.theta = 0.0
        self.R, self.Kt, self.Ke, self.J, self.b, self.V, self.cpr = R, Kt, Ke, J, b, V, cpr
    def step(self, duty, dt):
        i = (self.V * duty - self.Ke * self.omega) / self.R
        i = max(-20.0, min(20.0, i))                     # driver current limit
        self.omega += dt * (self.Kt * i - self.b * self.omega) / self.J
        self.theta += dt * self.omega
        return int(self.theta * self.cpr / (2 * math.pi))  # tick count for quad gen
```

**Quadrature synthesis on RP2040 PIO** — do NOT bit-bang quadrature from Python/IRQ; jitter will alias. PIO program clocks out A/B edges at a rate set by the plant velocity. At 4096 CPR and 3000 RPM you need 4096×50 = ~205 kHz edge rate — trivial for PIO, impossible for a Python loop.

### HIL timing budget — the numbers that matter

| Path | Budget | Why |
|---|---|---|
| PWM capture → plant step → quad rate update | < 1 ms | must be ≪ controller period (typ. 1 kHz loop) |
| Plant model dt | ≤ 0.5 × controller period | avoid discretization artifacts in the loop |
| USB round trip (Pico↔PC) | 1–4 ms typical, 10 ms+ spikes | run the plant ON the Pico if controller loop is ≥ 500 Hz |
| Logic analyzer sample rate | ≥ 10× highest PWM freq | 20 kHz PWM → sample ≥ 200 kHz |

If the controller loop is 1 kHz, the full HIL loop must close in well under 1 ms — which means **the plant model runs on the Pico**, and the PC only changes parameters and logs. USB-in-the-loop HIL only works for ≤ 100 Hz control loops.

### HIL test cases that pay for the rig

1. **Watchdog test:** stop sending heartbeats; verify motors PWM→0 within the specified timeout (measure with logic analyzer, assert < spec).
2. **Brownout/power-cycle:** cut DUT power mid-motion via relay; on reboot, assert outputs stay zero until armed. Catches "PWM pin floats high during boot" — a real and dangerous bug class (e.g., a GPIO that strapping pulls high will twitch the motor every boot).
3. **Encoder fault injection:** freeze quadrature while PWM nonzero → firmware must detect stall (current/expected-motion mismatch) and fault within N ms.
4. **Bus error injection:** emulator NAKs I2C reads or returns 0xFF; firmware must not crash, must mark sensor stale.
5. **Saturation soak:** command max velocity for hours; check for integrator drift, counter overflow (this is your 4.8-hour encoder wrap test on real firmware).
6. **Boot-time race:** power up DUT 1000 times overnight (relay + script); count failed boots. Intermittent boot failures (SD card init, I2C device not ready) only show up statistically.

```python
# PC-side HIL test (pytest drives the rig over serial)
def test_watchdog_kills_pwm(rig):
    rig.arm(); rig.send_velocity(2.0)
    assert rig.measured_pwm_duty() > 0.3
    rig.stop_heartbeat()
    t0 = time.monotonic()
    rig.wait_for(lambda: rig.measured_pwm_duty() == 0.0, timeout=1.0)
    elapsed = time.monotonic() - t0
    assert elapsed < 0.25, f"watchdog took {elapsed*1000:.0f} ms (spec: 200 ms)"
```

---

## Layer 4: Bench Tests — Real Robot, Clamped

### Setup rules (read before powering anything)

1. **Drive wheels off the ground.** Jack stands / foam blocks under the chassis, wheels free-spinning. For arms: clamp the base, clear the swept volume, remove the end-effector payload.
2. **Current-limited bench supply, NOT the battery, for first power-up.** Set the limit to ~1.5× expected idle current (e.g., 0.5 A for a logic-only check, 3 A for single-motor tests). A current-limited supply turns a short into a measurement instead of a fire.
3. **Physical E-stop in reach** of the person at the keyboard, wired to cut MOTOR power (not logic power — you want logs to survive the stop). E-stop in series with the motor supply via a contactor/relay rated for the stall current.
4. **First motor command at 10% duty, 2-second pulse.** Verify direction matches convention BEFORE closed loop. Wrong encoder polarity + closed loop = motor slams to full speed instantly (positive feedback). This is the most common first-bench-test failure.

### The bench checklist (in order — do not reorder)

```
[ ] Visual: no loose strands at screw terminals, no reversed connectors
[ ] Continuity: motor+ to motor- NOT shorted; VBAT to GND > 1 kΩ
[ ] Power logic only (motors disconnected): correct rails? 3.3 V ± 0.1, 5 V ± 0.25
[ ] Idle current sane? (note it down — it's your baseline forever)
[ ] Sensors stream: encoder counts change when wheel turned BY HAND
    → turn wheel "forward" by hand: count must INCREASE. If not, fix in
      ONE place (HAL channel config), never by negating downstream.
[ ] IMU: flat on bench → az ≈ +9.81 m/s² (or -9.81 — KNOW your convention),
    gyro |ω| < 0.02 rad/s after bias calibration
[ ] Open-loop motor pulse 10% duty: correct direction, current < expected
[ ] Open-loop ramp 0→50%: current vs duty roughly linear; listen for grinding
[ ] Closed-loop velocity step at LOW gain: no oscillation, settles
[ ] Closed-loop at target gains: log step response, save as golden trace
[ ] Stall test (hold wheel with gloved hand at 20% duty): current limit
    engages? firmware stall fault fires? NOTE: < 3 s, motors heat fast
[ ] Battery swap: repeat closed-loop step on battery power — supplies hide
    voltage sag; battery internal resistance changes loop behavior
```

### Numbers to write down at the bench (your future debugging gold)

- Idle current at logic rail, per-motor free-run current at 50% duty, stall current at 20% duty.
- Encoder ticks per output revolution (turn wheel exactly 1 rev by hand against a tape mark, read count). Verify against datasheet math — gearbox ratios on datasheets are sometimes nominal (e.g., "30:1" is actually 29.86:1 — at 10 m this is a 5 cm odometry error).
- Step-response trace (CSV) at final gains. Every future "the robot feels sluggish" gets compared to this golden trace.
- Deadband: minimum duty that produces motion (typ. 5–15% for brushed gearmotors). Feed this into the controller as feedforward offset.

### Clamped-test gotchas

- **Free-spinning ≠ loaded.** Gains tuned on a jacked robot will be ~2–5× too hot on the ground (no load → less damping needed). Tune conservative on the bench, finish on the floor.
- **Vibration walks the robot off jack stands.** Strap it down.
- **Stalling a motor by hand:** brushed motors tolerate ~3 s at 2× rated current; coreless and small brushless tolerate far less. If you smell anything, you're already late.
- **USB tether ground loops:** laptop on charger + robot on bench supply can put amps through the USB shield. Use a battery-powered laptop or a USB isolator (ADUM3160/4160-based, $10) for bench sessions.

---

## Layer 5: Field Tests

### The field protocol — non-negotiable structure

Every field session has: a **written test card**, a **safety observer**, and an **envelope**. No exceptions, even for "just a quick check."

**Test card template (fill before leaving the bench):**

```
TEST CARD #2026-06-10-A
Objective:    Validate new pure-pursuit lookahead (0.8 m → 0.5 m) on gravel
Pass criteria: cross-track error < 15 cm RMS over course B; zero interventions
Abort criteria: any tilt > 12°, cross-track > 50 cm, comms loss > 2 s
Envelope:     max speed 0.6 m/s (NOT full 1.2), course B only, dry surface
Config hash:  git 7f3a2c1, params/field_b.yaml sha256:90ab...
Roles:        Operator: R.  Safety observer: S. (holds remote E-stop)
Battery plan: 2 packs, abort at 3.55 V/cell
Data:         rosbag all topics, autostart on arm; offload before pack swap
```

**Roles.** The operator drives the test. The **safety observer does nothing but watch the robot** with a remote E-stop in hand — they do not look at screens, do not answer questions, do not hold the clipboard. One person cannot watch telemetry and the robot simultaneously; every team learns this by near-miss.

### Envelope expansion — how to ramp risk

Never test a change at full operating envelope. Standard expansion ladder:

1. **Static:** powered, armed, zero velocity. Verify telemetry, E-stop (test the E-stop EVERY session, first thing, at zero speed — it is itself a system that fails).
2. **Creep:** 25% speed, simplest course, operator within 3 m.
3. **Half envelope:** 50% speed, representative course.
4. **Full envelope:** only after two consecutive clean half-envelope runs.
5. **Degraded modes last:** GPS-denied, low battery, payload — one degradation at a time, back at 50% speed.

**One variable per run.** If you change lookahead AND speed AND course, a failure tells you nothing. The discipline feels slow; it is the fastest path that exists.

### Field debugging kit (what you'll wish you brought)

Multimeter, spare fuses (every rating used on the robot), spare props/wheels, hex drivers, zip ties, electrical tape, a USB-serial adapter, a known-good battery, sunshade for the laptop screen, and **a printed copy of pinouts and the test card** — phones die, sun glares.

### After every session

- Offload ALL logs before leaving the site (SD cards fail in transit more than you'd think).
- 10-minute hot debrief: what surprised us? Append to a running `field-log.md` — date, config hash, weather/surface, anomalies. Six months later this file is the only memory the team has.
- Any intervention or abort gets a ticket the same day with the rosbag/CSV attached.

---

## Scenario Regression Suite

Every field failure becomes a permanent regression scenario. The pipeline:

```
Field failure → extract sensor log slice → replay test (Layer 1-2) → fix → scenario locked in CI
```

### Log replay testing (the highest-ROI testing technique in robotics)

Record raw sensor inputs on the robot. Replay them through the (pure, HAL-mocked) pipeline on the desktop. The pipeline output must match — and after a fix, must improve — deterministically.

```python
# Replay harness: feed recorded sensor rows through the real estimator code
def replay(csv_path, estimator_factory):
    est = estimator_factory()
    out = []
    for row in load_rows(csv_path):       # t_us, ax..gz, enc_l, enc_r
        est.update(row)                    # SAME code that runs on the robot
        out.append((row.t_us, est.x, est.y, est.theta))
    return out

def test_regression_2026_05_14_heading_jump():
    """Robot spun 180° entering the metal doorway (magnetometer anomaly).
    Fix: mag innovation gate at 3-sigma. This log must never regress."""
    traj = replay("logs/2026-05-14-doorway.csv", make_ekf)
    max_jump = max(abs(angdiff(a[3], b[3])) for a, b in zip(traj, traj[1:]))
    assert max_jump < math.radians(5), "heading jump regression — mag gate broken?"
```

**Requirements for replayability** (design these in from day one):

- Log **raw** sensor values pre-filtering, with timestamps from one monotonic clock.
- Estimators/controllers consume time from the data, never from `time.now()`. Any `now()` call inside the pipeline destroys replay determinism.
- Seed every RNG; log the seed.
- Log the config/params hash with every session so replays use matching parameters.

### Scenario library structure

```
tests/scenarios/
  ├── nominal/            # happy paths: straight line, square, figure-8
  ├── regressions/        # one file per field incident, named by date+symptom
  │     ├── 2026-05-14-doorway-heading-jump/
  │     │     ├── sensors.csv
  │     │     ├── README.md        # what happened, what fixed it
  │     │     └── test_replay.py
  └── stress/             # synthetic: sensor dropout, max-rate spins, wheel slip
```

Run `nominal/ + regressions/` on every PR (they're fast — replay is faster than real time). Run `stress/` nightly.

---

## Cross-Layer Debugging Checklist

When a test passes at layer N but fails at layer N+1, the bug lives in what layer N doesn't model. Use this table to localize:

| Symptom | Passes in | Fails on | Look at |
|---|---|---|---|
| Oscillation | sim | bench | unmodeled latency, deadband, encoder quantization, loop rate not actually what you think (measure it!) |
| Drives backwards / spins | unit | bench | polarity convention split across files; fix at ONE HAL point |
| Works 17 min then freezes | bench | field | MicroPython tick wrap (2^30 µs ≈ 17.9 min) |
| Works on USB, fails on battery | bench | field | voltage sag, brownout reset, ground via USB was masking a missing ground wire |
| Random resets under load | HIL | bench | motor inrush → rail dip; add bulk capacitance (470–1000 µF at driver), separate logic supply or buck with ≥ 6 V headroom |
| I2C sensor "stale" intermittently | unit | bench/field | bus capacitance from long wires (keep I2C < 30 cm, pull-ups 2.2–4.7 kΩ at 3.3 V), or EMI from motor leads — twist motor pairs, separate from signal harness |
| Sim-tuned gains too hot | sim | bench | sim friction/damping too low; inject latency + deadband into sim, retune |
| Bench-tuned gains too hot | bench | field | free-spinning vs loaded dynamics; reduce kp 30–50%, re-expand envelope |
| GPS great in tests, jumps in field | all | field site | multipath near buildings; add innovation gating, test AT the failure site, log raw NMEA |
| Fails only after hours | HIL soak | — | counter/heap exhaustion; HIL soak tests exist precisely for this — run them |

## The Mistakes Everyone Makes (final pass)

1. **No HAL seam** → nothing below Layer 4 is possible. Retrofit cost grows daily; do it first.
2. **Mock that's nicer than reality** — mock returns clean floats, real ADC returns noisy ints with occasional 0xFFF glitches. Make mocks at least as hostile as hardware.
3. **Closed-loop before open-loop on the bench** — verify polarity open-loop first, always.
4. **Testing the fix only at the layer where the bug was found** — push the reproduction DOWN the pyramid (field bug → replay test) so it's guarded forever at CI cost.
5. **Skipping the E-stop check** at session start.
6. **`a - b` on tick counters** instead of wrap-safe diff — on both MicroPython (2^30) and Arduino (2^32 `micros()` wraps at ~71.6 min).
7. **No timeout on CI sim jobs** — one hung physics step burns 6 hours of runner time.
8. **Tuning on the bench supply, deploying on battery** — different source impedance, different sag, different behavior.
9. **One person field-testing alone** — no safety observer means no one is watching the robot when the screen has your attention.
10. **Logs not offloaded before the battery swap** — the session you lose will be the one with the bug.
