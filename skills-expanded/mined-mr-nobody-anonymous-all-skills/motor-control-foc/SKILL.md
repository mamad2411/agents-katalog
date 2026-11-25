---
name: motor-control-foc
description: "Use when selecting, wiring, tuning, or debugging motor drives for robots — BLDC/stepper/DC selection, field-oriented control (FOC), ODrive/VESC/moteus/SimpleFOC controllers, encoder integration (incremental/absolute/magnetic), current limits, thermal management, and regenerative braking. Provides the math, exact starting parameters, and the production failure modes that destroy hardware."
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


# Motor Control & Field-Oriented Control (FOC)

Expert knowledge for actuator selection and closed-loop motor control on real robots.
Everything here is written so that code generated from it is safe on hardware the first time:
current limits before tuning, brake resistors before regen, encoder verification before closed loop.

---

## 1. Motor Selection Matrix

| Criterion | Brushed DC | Stepper (open loop) | Stepper (closed loop) | BLDC + FOC | BLDC hub/gimbal |
|---|---|---|---|---|---|
| Cost (motor+drive) | $ | $ | $$ | $$$ | $$ |
| Torque density | Low | High at low RPM | High at low RPM | Highest | Medium |
| Top speed | Medium | Low (~600-1500 RPM useful) | Low-Medium | High (10k+ RPM) | Low-Medium |
| Positioning w/o encoder | No | Yes (if never stalls) | n/a | No | No |
| Efficiency | ~70% | 30-60% (full current at standstill) | 50-80% | 85-95% | 80-90% |
| Audible noise | Brush noise | Resonance whine | Quiet w/ FOC | Near silent | Near silent |
| Holding torque, unpowered | No (unless worm gear) | Detent only (weak) | Detent only | No (cogging only) | No |
| Failure mode when overloaded | Slows down gracefully | **Silently loses steps** | Faults / follows | Current-limits, keeps trying | Same |
| Smooth low-speed motion | Poor | Poor (resonance) | Good | Excellent | Excellent |
| Backdrivability (direct drive) | OK | Poor (detent + gearing) | Poor | Excellent | Excellent |

**Decision rules (use these, in order):**

1. **Need proprioceptive force control / legged robot / impedance control** → BLDC + FOC with low gear ratio (≤10:1). Nothing else works; steppers and high-ratio gearboxes destroy backdrivability and torque transparency.
2. **3D-printer-class positioning, loads well-characterized, cost-critical** → open-loop stepper is fine. Add a closed-loop stepper driver (e.g. with magnetic encoder) if missed steps are unacceptable.
3. **Cheap continuous rotation, speed control only, lifetime < ~3000 h** → brushed DC + H-bridge + encoder.
4. **High speed + high efficiency + battery powered** → BLDC, always.
5. **Need torque > ~2 Nm directly** → you need a gearbox regardless of motor type. Planetary for precision (backlash 5-15 arcmin), cycloidal/harmonic for robot joints (near-zero backlash, expensive), belt reduction for backdrivable legged joints (quiet, compliant, cheap).

**The stepper trap:** a NEMA 23 stepper has impressive holding torque (e.g. 1.9 Nm) but torque falls off a cliff with speed — at 1000 RPM it may produce <20% of holding torque. Always check the manufacturer's **torque-speed curve at your actual bus voltage** (torque-speed improves with voltage; a 24 V curve is useless if you run 12 V). Size for ≤50% of available torque at max speed.

**Kv / Kt fundamentals (BLDC):**

```
Kt [Nm/A] = 8.27 / Kv [RPM/V]        (for sinusoidal/FOC drive, peak-of-sine convention used by ODrive)
torque    = Kt × Iq                   (Iq = quadrature current, see §2)
no-load speed ≈ Kv × V_bus (×0.95 modulation limit)
```

Worked example: a 5008 gimbal motor, Kv = 335 RPM/V on a 24 V bus:
- Kt = 8.27/335 = 0.0247 Nm/A
- At 20 A peak: torque ≈ 0.49 Nm
- Max speed ≈ 335 × 24 × 0.95 ≈ 7600 RPM (mechanical, before field weakening)

Low-Kv ("gimbal") motors = high Kt, high winding resistance, low current → good torque control with cheap drivers but poor efficiency at speed. High-Kv drone motors = the opposite; need high current capability and good current sensing.

---

## 2. FOC — What It Actually Does

A BLDC produces torque only from current that is **90 electrical degrees ahead of the rotor flux**. FOC measures rotor angle, transforms the three phase currents into a rotating reference frame fixed to the rotor, and runs two independent PI current loops:

- **Id** (direct axis): current aligned with rotor magnets. Produces no torque. Setpoint = 0 (or negative for field weakening above base speed).
- **Iq** (quadrature axis): torque-producing current. `torque = Kt × Iq`. This is the knob every outer loop turns.

The transform chain per PWM cycle (typically 10-50 kHz):

```
Ia, Ib, Ic  --Clarke-->  Iα, Iβ  --Park(θe)-->  Id, Iq
                                                  │ PI loops
Vd, Vq  --InvPark(θe)-->  Vα, Vβ  --SVPWM-->  3 phase duty cycles
```

Key facts that matter in practice:

- **θe is electrical angle** = mechanical angle × pole pairs. A "24N28P" motor has 14 pole pairs: one mechanical revolution = 14 electrical revolutions. Pole-pair count wrong by one → motor spins erratically or vibrates in place. If unsure: drive a fixed voltage vector, rotate shaft by hand one full mech rev, count electrical cycles — or trust the calibration routine (ODrive/VESC/moteus all measure it).
- **Encoder-to-rotor offset** must be calibrated: the drive locks the rotor to a known electrical angle (applies Id with θe=0) and records the encoder reading. This offset is invalid if the encoder is remounted or slips. Symptom of a stale offset: weak torque, high current draw, motor runs away in one direction.
- **Current loop bandwidth** is the foundation; everything above it (velocity, position) must be ≥5-10× slower. Typical current loop bandwidth: 1-2 kHz. Velocity loop: 100-200 Hz. Position loop: 20-50 Hz.

**Control cascade (standard structure on every serious drive):**

```
pos_ref → [P] → vel_ref → [PI + ff] → Iq_ref → [PI] → Vq → SVPWM
            position loop      velocity loop      current loop
```

**Six-step (trapezoidal) vs FOC:** six-step commutation (cheap ESCs, hall-only) switches phases in 60° blocks → ~13% torque ripple, noise, poor low-speed behavior. Use it only for fans/pumps/drone props. Any robot joint, wheel, or gripper gets FOC.

**Sensorless FOC** (back-EMF observers, e.g. VESC default) works above ~5-10% of rated speed and fails at standstill/low speed. Never use sensorless for position control or low-speed torque (robot joints). Hall sensors give 60°-resolution commutation — acceptable for wheels, not for joints. Use a real encoder.

---

## 3. Controller Ecosystem — What to Pick

| Controller | Power class | Best for | Interface | Notes |
|---|---|---|---|---|
| **ODrive S1/Pro** | ~40 A / 58 V (S1), 120 A/58 V (Pro) | Robot arms, AMR wheels, legged | CAN (CANSimple), USB, UART | Excellent tuning UI (`odrivetool`/GUI), anticogging, good docs |
| **moteus (mjbots) r4/c1/n1** | 100 A/44 V (r4.11), smaller for c1 | Legged robots, high-rate torque control | CAN-FD (5 Mbps) | Integrated magnetic encoder, position/velocity/torque at up to ~2 kHz command rate, `tview` tuning |
| **VESC 6 / clones** | 80-100 A / 60 V | E-skate, wheels, traction | CAN, UART, PPM | Mature sensorless, weaker as position servo; VESC Tool wizards |
| **SimpleFOC** (library) | Whatever your driver board does (typ. ≤30 A) | Custom/learning/gimbal-class, haptics | You write the firmware (Arduino/STM32/ESP32) | Full control, but YOU own safety: no built-in thermal model, you must implement faults |
| **Industrial servo drives** (Kinco, Leadshine, Kollmorgen…) | kW class | CNC, industrial arms | EtherCAT/CANopen (CiA 402) | Use when certification/24-7 duty matters |

**Default recommendations:** wheeled robot or arm joint → ODrive. Legged/dynamic robot needing kHz torque commands → moteus. Traction/e-mobility → VESC. Haptic knob or teaching → SimpleFOC.

**Always use CAN, not USB, on a robot.** USB enumeration drops under EMI from the motor itself; CAN with 120 Ω termination at both ends survives. Command rate guidance: torque mode needs ≥ 100 Hz refresh (most drives have a watchdog that faults if commands stop — *enable that watchdog*; an arm that keeps executing its last torque command after the host crashes is how robots punch holes in tables).

### ODrive minimal bring-up (Python, odrivetool)

```python
import odrive
from odrive.enums import *

odrv = odrive.find_any()
ax = odrv.axis0

# --- LIMITS FIRST. Never calibrate or close a loop before these. ---
ax.config.motor.current_soft_max = 20          # [A] continuous-ish ceiling
ax.config.motor.current_hard_max = 35          # [A] instant fault above this
ax.config.motor.calibration_current = 5        # [A] enough to lock rotor, no more
odrv.config.dc_max_positive_current = 25       # [A] from supply
odrv.config.dc_max_negative_current = -1       # [A] CRITICAL with PSU: near zero regen
                                               #     (see §6; set to -inf ONLY on battery)
ax.config.motor.pole_pairs = 7
ax.config.motor.torque_constant = 8.27 / 270   # 8.27 / Kv

# Encoder (e.g. onboard magnetic, or configure SPI/incremental as fitted)
ax.config.load_encoder = EncoderId.ONBOARD_ENCODER0
ax.config.commutation_encoder = EncoderId.ONBOARD_ENCODER0

odrv.save_configuration()                       # reboots

# Calibration: motor MUST be free to spin, mechanically unloaded
ax.requested_state = AxisState.FULL_CALIBRATION_SEQUENCE
# wait until ax.current_state == AxisState.IDLE, then check:
assert ax.active_errors == 0, hex(ax.active_errors)

ax.controller.config.control_mode = ControlMode.VELOCITY_CONTROL
ax.controller.config.vel_limit = 10            # [turn/s]
ax.requested_state = AxisState.CLOSED_LOOP_CONTROL
ax.controller.input_vel = 2
```

### moteus minimal bring-up (CAN-FD)

```python
import asyncio, moteus

async def main():
    c = moteus.Controller(id=1)
    await c.set_stop()                       # clear faults
    # Torque command with safety bounds — ALWAYS set maximum_torque
    state = await c.set_position(
        position=float('nan'),               # nan = don't servo position
        velocity=0.0,
        feedforward_torque=0.0,
        kp_scale=0.0, kd_scale=1.0,          # pure damping example
        maximum_torque=1.0,                  # [Nm] hard clamp — never omit
        query=True)
    print(state.values[moteus.Register.POSITION])

asyncio.run(main())
```

Calibrate first with `python -m moteus.moteus_tool --target 1 --calibrate` (motor unloaded), then set `servo.max_current_A`, `servo.pid_position` gains via `tview`.

### SimpleFOC skeleton (you own the safety code)

```cpp
#include <SimpleFOC.h>

BLDCMotor motor(7);                          // pole pairs
BLDCDriver3PWM driver(9, 5, 6, 8);
MagneticSensorI2C sensor(AS5600_I2C);        // see §4 AS5600 caveats

void setup() {
  sensor.init();
  motor.linkSensor(&sensor);
  driver.voltage_power_supply = 12;
  driver.init();
  motor.linkDriver(&driver);

  motor.voltage_limit  = 6;     // [V]  start at half bus voltage
  motor.current_limit  = 2;     // [A]  REQUIRED — without current sense this is
                                //      enforced via voltage_limit/phase_resistance:
  motor.phase_resistance = 5.6; // [Ohm] measure it; enables current estimation
  motor.velocity_limit = 20;    // [rad/s]

  motor.controller = MotionControlType::velocity;
  motor.PID_velocity.P = 0.2;  motor.PID_velocity.I = 2.0;  motor.PID_velocity.D = 0;
  motor.LPF_velocity.Tf = 0.01;

  motor.init();
  motor.initFOC();              // runs align calibration — shaft must be free
}

void loop() {
  motor.loopFOC();              // current/commutation — run as fast as possible
  motor.move(5.0);              // target [rad/s]
}
```

SimpleFOC has **no thermal protection, no watchdog, no overcurrent fault** unless you add them. For anything beyond a desk demo, add: shaft-stall detection (velocity ≈ 0 while current at limit for >500 ms → disable), supply undervoltage check, and an NTC on the driver MOSFETs.

---

## 4. Encoders

| Type | Resolution | Absolute? | Failure modes | Use for |
|---|---|---|---|---|
| Incremental optical (quadrature ABZ) | 1000-10000 PPR common | No (needs index/homing) | Dust on disk, miscounts under EMI, lost counts on power glitch | High-resolution velocity, wheels |
| Magnetic on-axis (AS5600, AS5047P, MA702, MT6701) | 12-14 bit/rev | Per-revolution | Magnet misalignment, off-axis distortion, temperature drift | Joint commutation + position |
| Absolute multi-turn (SSI/BiSS, battery or gear backed) | 17-23 bit | Fully | Cost; battery-backed types lose turns when battery dies | Industrial joints, no-homing startup |
| Hall sensors (in-motor) | 6 states/elec rev | Commutation only | Solder fatigue from vibration | Cheap wheel commutation only |

**CPR vs PPR — the #1 configuration bug.** PPR (pulses per revolution) is what the encoder datasheet says: pulses per channel per mechanical revolution. CPR (counts per revolution) is what a quadrature decoder produces: **CPR = 4 × PPR**, because both edges of both channels are counted.

- Encoder labeled "2500 PPR" → configure CPR = 10000.
- Encoder labeled "8192 CPR" (already counts) → CPR = 8192.
- Symptom of 4× error: velocity reads 4× wrong, position loop unstable or sluggish, calibration fails with "CPR mismatch"-type errors (ODrive checks measured vs configured CPR during calibration and will tell you).
- Verify empirically: rotate the shaft exactly one revolution by hand, read the count delta. Do this before ever closing a loop.

**AS5600 specifics (ubiquitous and frequently misused):**

- It is a 12-bit (4096 count) **I2C** sensor designed as a knob replacement, not a servo encoder. I2C max ~1 MHz → full angle read takes ~100-200 µs → caps your FOC loop around 2-5 kHz and adds latency that limits velocity-loop bandwidth. For real servo work use SPI parts: **AS5047P, MA702, MT6701-SPI** (≤ a few µs per read).
- It has only one I2C address (0x36). Two AS5600s on one bus requires a mux (TCA9548A) or one-per-bus.
- Magnet matters: diametrically magnetized, 6 mm typical, **air gap 0.5-3 mm**, centered within ~0.25 mm of the IC center. Off-center magnet → angle nonlinearity → torque ripple that no amount of PID tuning fixes. The chip's AGC/status registers (MD/ML/MH bits) tell you if the field is too weak/strong — read them during bring-up.
- Mount the magnet on a **non-ferrous** shaft end (or use a plastic spacer); a steel shaft shunts the field.
- Output wraps 4095→0 once per mech revolution: your software must unwrap, and absolute position is lost across power cycles unless the joint can't move >½ rev or you home.

**Encoder mounting rules:** the commutation encoder must be on the **motor shaft**, not the gearbox output (backlash between rotor and encoder makes FOC commutation wrong). For precise joint position with a gearbox, the gold standard is dual encoders: one on rotor (commutation) + one absolute on output (position), with the drive or host fusing them.

**Wiring:** differential (RS-422) signals for incremental encoders on cables >30 cm near motor phases. Single-ended encoder lines next to phase wires = corrupted counts that look exactly like mechanical problems. Twist encoder pairs, route away from phase wires, shield grounded at one end.

---

## 5. Current Limiting & Thermal Management

Three different limits — confuse them and you burn something:

1. **Phase current limit** (motor protection): heating ∝ I²R in the windings. Continuous rating from datasheet; peak 2-3× continuous for seconds.
2. **DC bus current limit** (supply protection): `I_bus ≈ I_phase × duty × power_factor`. At low speed, phase current can be far above bus current — a motor stalled at 40 A phase might draw only 4 A from the bus. Your PSU sees bus current; your motor dies from phase current. Limit both.
3. **Drive (MOSFET) current limit**: from the controller datasheet; usually thermal, derate with poor cooling.

**Thermal math (worked example):**

Copper loss in a stalled motor: `P = 1.5 × I² × R_phase` (3-phase, line-to-neutral R).
Motor with R = 0.15 Ω/phase holding 15 A: P = 1.5 × 225 × 0.15 = **50.6 W** of pure heat at zero output power. With a thermal resistance of ~2 °C/W (small frameless motor, poor heatsinking), steady-state ΔT ≈ 100 °C → winding insulation (class B = 130 °C, class F = 155 °C) is at its limit from ambient 25-55 °C. Thermal time constant of small motors: 1-5 min — it will work fine in a 30-second demo and cook in deployment.

Rules:
- Robots that **hold position against gravity** (arms, grippers) are stall-duty machines. Size motors for continuous stall current at worst-case pose, or add a brake / counterbalance / non-backdrivable gearing.
- Fit an **NTC thermistor in the windings** (many motors have one; if not, epoxy a 10k NTC against the stator) and wire it to the drive's motor-thermistor input. Set: derate start ~100 °C, hard cutoff ~120 °C (class F windings). ODrive: `motor_thermistor` config; moteus: `servo.motor_thermistor_ohm` + fault temp.
- Magnets demagnetize: standard neodymium grades start losing magnetism permanently above 80-150 °C depending on grade (N35 ≈ 80 °C, N35SH ≈ 150 °C). A demagnetized motor has permanently higher Kv/lower Kt — it "got weaker after that one incident" is real.
- MOSFET thermal: drive specs assume airflow or heatsink. A "100 A" VESC without a heatsink is a 30-40 A VESC.
- **I²t protection** (software thermal model) is the right tool for allowing short peaks: allow `I_peak` for `t ≤ (I_cont/I_peak)² × τ_thermal`. Most good drives implement this; configure it rather than setting one conservative flat limit.

---

## 6. Regenerative Braking — The PSU Killer

When a motor decelerates (or is backdriven, e.g. lowering a load or someone pushes the robot), it becomes a generator and pumps current **back into the DC bus**.

**Why this kills things:** lab/server power supplies cannot sink current. The regenerated energy has nowhere to go, so it charges the bus capacitors and **bus voltage rises until something fails** — typically: PSU overvoltage protection trips (robot loses power mid-motion — itself dangerous), or the drive's FETs/caps exceed rating and die, or the drive faults with `DC_BUS_OVER_VOLTAGE`.

Energy magnitude check: a 10 kg mobile robot braking from 2 m/s has E = ½mv² = 20 J. Dumped into a 48 V bus with 1000 µF total capacitance: ΔV from `½C(V₂²−V₁²) = E` → V₂ = √(48² + 2×20/0.001) ≈ **208 V**. The capacitors are rated 63 V. This is why drives explode on the first hard stop.

**Mitigations, in order of preference:**

1. **Battery bus.** Batteries absorb regen naturally. (Caveat: a *fully charged* lithium pack must not be charged further — BMS may disconnect on overvoltage, which then floats the bus and you're back to the failure case. Some robots add a small regen headroom by never charging above ~95%.)
2. **Brake/dump resistor.** A chopper circuit dumps regen into a power resistor above a voltage threshold. ODrive (legacy/Pro with brake resistor support): set `config.brake_resistor0.enable = True`, `resistance = 2.0` (use the 50 W 2 Ω aluminum-shell type, mounted to metal). Threshold sits a few volts above nominal bus.
3. **Drive-side regen current clamp.** ODrive: `dc_max_negative_current` — with a non-sinking PSU and no brake resistor this must be ≈ 0 (e.g. `-0.5` A to tolerate measurement noise; exactly `0` can cause nuisance faults). The drive then limits braking torque so regen never exceeds the cap. Consequence: **your robot brakes more weakly than commanded** — account for this in stopping-distance safety calcs.
4. **Bus clamp module** (e.g. ODrive PSU clamp boards, industrial "braking units") between PSU and drives — same idea as #2, standalone.
5. **A diode in series with the PSU** prevents current flowing back into the PSU, but the bus still pumps up — only valid combined with #2 or large bus capacitance and modest energy.

**Checklist before the first hard deceleration test:** what absorbs regen? what is the bus overvoltage fault threshold? is the e-stop a power cut (then where does the moving robot's kinetic energy go)? Note: cutting power to a spinning BLDC whose phase leads remain connected through the (now unpowered) drive's body diodes can still rectify back-EMF into the bus — high-speed motors can keep the bus alive for seconds.

---

## 7. Tuning Methodology & Starting Values

Always tune in this order, inner loop first. Never tune position gains with a sloppy velocity loop.

**0. Current loop:** modern drives auto-tune it from measured R and L during calibration (PI gains: `Kp = L × bandwidth`, `Ki = R × bandwidth`, bandwidth ≈ 1-2 kHz). Verify with a current step: Iq should settle in <2 ms, overshoot <20%. If R/L measurement failed (very low resistance motors), measure R with a milliohm meter and set manually.

**1. Velocity loop** (motor mounted with real load if possible):
- Start: `vel_gain` small, `vel_integrator_gain = 0`.
- Increase P until you hear/see oscillation at a velocity step, back off to ~50-60%.
- Add integrator: `Ki ≈ 0.5 × bandwidth × Kp` (ODrive heuristic: `vel_integrator_gain = 0.5 × vel_gain × (loop bandwidth in rad/s)`... practical version: increase until steady-state error gone, reduce if you see slow oscillation/hunting).
- Filter the velocity estimate (encoder differentiation is noisy): LPF time constant 5-20 ms for low-res encoders; too much filtering = phase lag = instability ceiling.

**2. Position loop:** pure P. Increase until overshoot appears, back off 30%. Add velocity feedforward (= derivative of trajectory) to kill following error during motion without raising gains.

**ODrive starting points (units: ODrive uses turns):**
```
pos_gain            = 20        [(turn/s)/turn]
vel_gain            = 0.16      [Nm/(turn/s)]  — scale with inertia
vel_integrator_gain = 0.32      [Nm/turn]      — ≈ 2 × vel_gain as a start
vel_limit           = sane for your mechanism, ALWAYS set
```

**Symptoms dictionary:**

| Symptom | Likely cause |
|---|---|
| High-pitched squeal at standstill | vel_gain too high or encoder noise → reduce gain or increase velocity LPF |
| Slow oscillation (~1 Hz hunting) | too much velocity integrator, or backlash between motor and load |
| Motor jumps then faults at enable | wrong encoder offset / wrong pole pairs / phase wires swapped after calibration |
| Runs away at full speed on enable | encoder direction inverted vs phase order — recalibrate; never "fix" by negating gains |
| Weak torque, hot motor | stale commutation offset (Id large, Iq small) — check `Iq_measured` vs total current |
| Torque ripple once per rev | magnet off-center on magnetic encoder (§4) or anticogging not calibrated |
| Works unloaded, oscillates with load | inertia mismatch — retune with load; consider lower bandwidth or add mechanical damping |
| Random encoder errors only when motor runs | EMI on encoder lines (§4 wiring) |
| `DC_BUS_OVER_VOLTAGE` on decel | regen with no sink (§6) |
| Stalls/faults only after minutes | thermal derate or winding overtemp (§5) |

**Anticogging:** low-speed smoothness on gimbal motors is limited by cogging torque. ODrive and SimpleFOC support an anticogging calibration (maps cogging vs angle, feeds forward the inverse). Run it after tuning, with the mechanism unloaded. Mandatory for camera gimbals, haptics, and slow scanning axes.

---

## 8. Safety & Bring-Up Checklist (run every time, in order)

1. Bench supply with current limit set low (2-3 A) for first power-up — a wiring error becomes a current-limit event, not smoke.
2. Set **all** limits in the drive before any calibration: phase current soft/hard, bus current ±, velocity limit, position soft stops if applicable.
3. Verify encoder counts manually (one rev by hand = expected CPR; direction consistent).
4. Calibrate with the motor **mechanically disconnected from the load**. Calibration spins the rotor; a connected gearbox/arm makes the inductance/offset measurement wrong and can be dangerous.
5. First closed-loop test in **velocity mode at low vel_limit**, not position mode (position mode with a bad config slams to a setpoint at full torque).
6. Enable the **command watchdog** (ODrive: `config.enable_watchdog`, `watchdog_timeout`; moteus: faults on CAN silence by default in position mode with `watchdog_timeout`). Verify it by killing your control process while the motor runs — the motor must stop.
7. E-stop philosophy: cutting drive enable (drives coast or actively brake to a safe state) is usually better than cutting bus power (uncontrolled coast + regen issues + arms fall). Gravity-loaded axes need either a spring/counterweight, a power-off brake, or a non-backdrivable stage — torque-off must be a safe state by design.
8. Log on every robot, always: bus voltage, Iq, motor temp (if available), drive faults, position error. Production motor failures are diagnosed from these five signals.

---

## 9. ROS2 Integration Pattern

Use `ros2_control` with a hardware interface per drive bus, not per-motor ad-hoc nodes. Loop rates: `controller_manager` at 100-500 Hz over CAN is realistic; the drive's internal loops handle the kHz-rate work — **send setpoints, don't try to close current loops over ROS topics**.

```yaml
# controllers.yaml — velocity-controlled diff drive on ODrive CAN
controller_manager:
  ros__parameters:
    update_rate: 200            # Hz — must beat the drive watchdog period comfortably
    diff_drive_controller:
      type: diff_drive_controller/DiffDriveController
```

Existing hardware interfaces worth using instead of writing your own: `odrive_ros2_control` (CAN), `moteus` + `moteus_ros2`/mjbots examples, `vesc_driver`. For arms doing torque control, mjbots' pattern is the reference: a single realtime process owns the CAN-FD bus, cycles all servos in one frame batch at 200-500 Hz, exposes state via shared memory or a ROS2 node at lower rate.

Hard rule: the safety chain (watchdog, limits, thermal) lives **in the drive firmware**, never in a ROS node. ROS process death must equal motors-safe, with zero software in between.
