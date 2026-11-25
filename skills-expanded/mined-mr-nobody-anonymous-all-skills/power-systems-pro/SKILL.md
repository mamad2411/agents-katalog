---
name: power-systems-pro
description: "Use when designing or debugging robot power systems — Li-ion battery pack design, BMS selection, precharge/inrush limiting, emergency stop power paths, power sequencing, DC-DC converter sizing, or grounding/noise problems. Provides professional-grade pack architecture math, protection circuit design, safety-rated E-stop topology, derating rules, and the grounding discipline that prevents motor noise from corrupting logic and sensors."
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


# Robot Power Systems — Professional Design

Power architecture is the most common cause of "mysterious" robot failures: brownouts that reboot the compute mid-mission, inrush that welds relay contacts, ground loops that corrupt encoder counts, packs that die at 60% of rated cycle life. This skill covers the design discipline that prevents all of these — on the first hardware revision.

**Scope:** mobile robots and manipulators from ~50 W (small AMR) to ~5 kW (industrial mobile manipulator). Voltages 12–60 V (SELV territory). Above 60 V DC you enter different regulatory territory (touch-safe limits, creepage/clearance per IEC 61010 / ISO 13849 implications) — flag that explicitly to the user.

---

## 1. System Power Architecture — The Reference Topology

Before any component selection, draw this. Every production robot converges on some variant of it:

```
                                ┌──────────────────────────────────────┐
 Battery Pack ──[Pack Fuse]──┬──┤ E-STOP POWER PATH (motor bus)        │
 (BMS inside)                │  │  Contactor/MOSFET disconnect          │
                             │  │  ├── Precharge circuit (R + relay)    │
                             │  │  └──► Motor drivers (big cap banks)   │
                             │  └──────────────────────────────────────┘
                             │
                             └──[Logic Fuse]──► ALWAYS-ON LOGIC PATH
                                                ├── DC-DC 48V→12V → compute, sensors
                                                ├── DC-DC 48V→5V  → USB peripherals, LEDs
                                                └── DC-DC 48V→24V → contactor coil, safety PLC
```

**Non-negotiable architectural rules:**

1. **Two independent paths from the pack: motor power and logic power.** They split at the battery terminals (or pack output connector), each with its own fuse. E-stop kills the motor path ONLY. Logic stays alive so you keep telemetry, logging, comms, and the ability to diagnose why the E-stop fired.
2. **The E-stop path is hardware-only.** No microcontroller, no software, no CAN message in the chain that removes motor power. Software may *request* a stop; hardware *guarantees* it (Section 5).
3. **Precharge before connecting any capacitor bank > ~500 µF to the bus** (Section 4).
4. **Logic comes up before motors are enabled, and motors are disabled before logic goes down** (Section 6).
5. **One star ground point, at the pack negative terminal or main power distribution board** (Section 8).

If a design violates any of these, fix the architecture before optimizing anything else.

---

## 2. Li-ion Pack Design (Series/Parallel)

### 2.1 Cell chemistry selection

| Chemistry | Nominal V/cell | Max V/cell | Min V/cell | Energy density | Cycle life | Notes |
|---|---|---|---|---|---|---|
| NMC/NCA (Li-ion) | 3.6–3.7 V | 4.2 V | 2.5 V (use 3.0 V) | 200–260 Wh/kg | 500–1000 | Default for mobile robots. Thermal runaway risk — needs real BMS. |
| LiFePO4 (LFP) | 3.2 V | 3.65 V | 2.5 V | 90–160 Wh/kg | 2000–5000 | Safer, flat discharge curve (SoC-by-voltage is nearly useless), heavier. Good for AGVs charged daily. |
| Li-ion high-drain (e.g., Molicel P42A/P45B, Samsung 40T) | 3.6 V | 4.2 V | 2.5 V | ~230 Wh/kg | 300–500 | When peak current matters: 30–45 A continuous per 21700 cell. |

**Rule:** For robots that opportunity-charge at dock multiple times per day, LFP cycle life usually wins total-cost. For weight-constrained platforms (legged, aerial, manipulator payload budgets), NMC 21700 cells.

### 2.2 Series count (S) — set by voltage

`V_nominal = S × V_cell_nominal`, `V_max = S × V_cell_max`, `V_min = S × V_cell_cutoff`

Worked example — "48 V" NMC pack, 13S:
- Nominal: 13 × 3.6 = 46.8 V
- Full charge: 13 × 4.2 = **54.6 V**
- Empty (3.0 V cutoff): 13 × 3.0 = 39.0 V

**Critical consequence:** every downstream component must tolerate the FULL range 39–54.6 V, plus regenerative braking transients (Section 2.5). A "48 V input" DC-DC rated 36–60 V is fine; one rated 40–56 V is a field failure waiting for a cold day at full charge + regen spike. Also: 14S (58.8 V max) crowds the 60 V SELV limit — 13S is the standard choice for "48 V" robots for exactly this reason.

### 2.3 Parallel count (P) — set by capacity AND current

Two independent constraints; satisfy both:

1. **Energy:** `P ≥ E_required / (S × V_nom_cell × C_cell)`
2. **Current:** `P ≥ I_peak / I_cell_max_continuous` — and apply a 0.7 derating on the cell datasheet continuous rating for packs without forced-air cooling (cells in the middle of a pack run hot; capacity and life collapse above 45 °C).

Worked example — mobile manipulator, 48 V (13S), 600 Wh usable, 60 A peak (stall + dynamic), using 21700 NMC cells (5.0 Ah, 15 A continuous):

- Usable energy at 85% DoD: need 600/0.85 ≈ 706 Wh nameplate → P ≥ 706 / (13 × 3.6 × 5.0) = 706/234 = 3.02 → P = 4 (round up, never down)
- Current: P ≥ 60 / (15 × 0.7) = 5.7 → **P = 6**

Current wins: 13S6P, 30 Ah, 1.40 kWh nameplate. The pack is sized by peak current, not energy — extremely common in robotics and frequently missed. If you sized by energy alone (13S4P) the pack would sag hard under peak load, trip BMS overcurrent, and age 3–5× faster.

### 2.4 Voltage sag and why it reboots your compute

Pack source resistance: `R_pack = R_cell × S / P`. For 25 mΩ cells at 13S6P: 25 × 13/6 ≈ 54 mΩ. At a 60 A transient: **3.2 V sag** — plus harness and connector resistance (budget 10–20 mΩ for a typical robot harness; measure it). A pack near empty (39 V) minus 4 V total sag = 35 V at the DC-DC input. If your DC-DC's undervoltage lockout is 36 V, **the robot reboots every time the arm lifts a payload at low battery.** This exact failure has killed more robot demos than any software bug.

Mitigations, in order of preference: (1) DC-DC with wide input (e.g., 18–75 V), (2) raise the software low-battery cutoff to keep margin, (3) bulk capacitance at DC-DC input (electrolytic, 470–1000 µF per 100 W of converter), (4) more P.

### 2.5 Regenerative braking transient

Motors decelerating pump energy back into the bus. If the BMS opens the charge path (e.g., pack full, charge FET off) the bus has nowhere to put it and voltage spikes until something clamps or dies.

- Budget transient bus voltage = `V_max_pack + 10–15%`. For 13S: design downstream for ≥ 63 V transient tolerance.
- For drives > ~200 W, fit a **brake chopper / regen clamp**: comparator + MOSFET + power resistor that turns on at e.g. 57 V and dumps regen into the resistor. Size the resistor for worst-case kinetic energy: `E = ½mv²` for the platform; a 50 kg robot at 1.5 m/s = 56 J — a 100 W aluminum-shell resistor handles this with huge margin for repeated stops.
- A TVS diode is NOT a regen clamp. TVS handles microsecond inductive spikes (fit one anyway, e.g., SMDJ58A on a 48 V bus); it cannot absorb joules of regen.

---

## 3. BMS — Functions, Selection, Integration

A BMS is a safety device first and a fuel gauge second. Minimum functions for any production robot:

| Function | Typical setting (NMC) | Why it matters |
|---|---|---|
| Cell overvoltage cutoff | 4.25 V/cell (alarm 4.20) | Overcharge → lithium plating → thermal runaway |
| Cell undervoltage cutoff | 2.8–3.0 V/cell | Over-discharge → copper dissolution → internal shorts on next charge |
| Overcurrent (discharge) | 1.2–1.5× design peak, with delay 100–500 ms | Below this and the BMS trips on normal motor stall transients |
| Short-circuit protection | ~3–5× rated, < 1 ms, usually FET turn-off | Last line before the fuse |
| Overtemperature | Charge: 0–45 °C window; discharge: −20–60 °C | **Charging below 0 °C plates lithium permanently.** Heated packs or charge inhibit for cold environments. |
| Cell balancing | Passive, 50–150 mA typical, top-balance during CV phase | See below |
| SoC/SoH reporting | Coulomb counting + OCV correction | Mission planning needs real SoC, not voltage-as-SoC |

**Balancing reality check:** passive balancers bleed 50–150 mA through resistors. A pack with one weak parallel group drifting 100 mAh per cycle needs ~1–2 h of balancing per charge; if the robot fast-charges in 45 min, the pack walks out of balance over weeks and the BMS starts cutting discharge early (lowest group hits undervoltage first). Symptoms: "battery dies at 30% SoC." Fix: longer balance dwell at dock, or replace the weak group. Active balancing is rarely worth it below 2 kWh.

**BMS FETs vs. contactor:** Most COTS BMS use back-to-back MOSFETs to interrupt the pack. Check the FET path's continuous current rating against your derated peak — many "60 A BMS" boards are 60 A for 30 s with a fan. For packs > ~30 A continuous or where the BMS disconnect is part of the safety case, prefer a BMS that drives an external contactor.

**Integration musts:**
- Wire the BMS alarm/fault output (usually open-drain) into your robot's state machine. A BMS disconnect must be *observed* by software, not discovered as a mystery power loss.
- CAN-based smart BMS (e.g., implementing a CANopen or proprietary protocol) is strongly preferred ≥ 500 Wh: per-cell-group voltages and temps in telemetry catch a degrading group months before it strands a robot.
- The BMS protects the *pack*. It does not protect your *harness*. Fuse every branch (Section 7).

**Never** build a pack without a BMS "temporarily for testing." Test benches burn down.

---

## 4. Inrush Limiting — Precharge Circuits

### 4.1 The problem, quantified

Motor drivers have DC-link capacitor banks: 470 µF–10,000 µF total across a multi-axis robot. Connecting a discharged capacitor bank directly to a 50 V pack:

`I_peak = V / R_loop` — with ~50 mΩ total loop resistance, that's **1000 A** for hundreds of microseconds. Consequences, all observed in real robots:
- Welded contactor/relay contacts (E-stop now does nothing — a safety failure)
- Pitted XT90/Anderson connector contacts → rising resistance → heat → melted connector weeks later
- BMS short-circuit trip on every power-up
- Latch-up or reset of logic sharing the bus during the dip

**Threshold:** precharge anything > ~500 µF on buses ≥ 24 V. Below that, an NTC inrush limiter or connector with built-in precharge resistor (XT90-S) is acceptable for non-safety paths.

### 4.2 Reference precharge circuit

```
 Pack + ──┬───────[Main Contactor K1]───────┬──► Motor bus (+)
          │                                 │
          └──[R_pre]───[Precharge Relay K2]─┘
                                              C_bus (e.g., 4700 µF)
 Sequencing (hardware or supervised µC):
   1. Close K2 → bus charges through R_pre
   2. Wait until V_bus ≥ 90–95% of V_pack (measure it — do not just time it)
   3. Close K1
   4. Open K2
```

### 4.3 Sizing R_pre — worked example

48 V (54.6 V max) pack, C_bus = 4700 µF, want precharge ≤ 500 ms.

- Time constant: charge to 95% takes 3τ → τ = 167 ms → `R = τ/C = 0.167/0.0047 ≈ 35 Ω` → pick **33 Ω**.
- Peak current: 54.6/33 = 1.65 A — fine for a small relay.
- **Energy dissipated in R equals energy stored in C**: `E = ½CV² = ½ × 0.0047 × 54.6² = 7.0 J` per precharge event. A 5 W wirewound resistor absorbs 7 J fine *once*; check the resistor's single-pulse energy rating (wirewound ~5–10× rated power for 1 s). If software can retry precharge in a loop (failed precharge → retry → failed → retry), the resistor WILL burn open. **Limit precharge retries to 2–3 with cooldown, and alarm on failure.**
- Failure detection: if V_bus hasn't reached 90% in 5τ, there's a short on the motor bus or a stuck load — abort, open K2, alarm. This check is free and catches dead-short motor driver failures before the main contactor welds itself trying.

### 4.4 Solid-state alternative

For < ~30 A buses, a high-side P-FET or N-FET+driver with controlled gate ramp (soft-start) replaces both relays. Use a dedicated hot-swap controller IC (e.g., LTC4368, TPS2490 class) — they integrate dV/dt-limited turn-on, current limit, and SOA-aware fault timing. Do NOT hand-roll an RC-on-the-gate soft-start for production: FET SOA at 50 V partial-conduction is unforgiving, and a FET stuck in linear region during an overload fails in milliseconds. Hot-swap controllers exist because this problem is harder than it looks.

---

## 5. Emergency Stop — Power Cut Path Separate From Logic

### 5.1 Principles (aligned with ISO 13849 / IEC 60204-1 thinking)

1. **E-stop removes motor power via hardware.** The chain is: E-stop button (mechanical, latching, direct-opening contacts) → safety relay or direct contactor coil → main motor contactor opens. No firmware in the chain.
2. **Logic power is NOT cut.** Compute, sensors, comms, and the BMS stay up. You want the robot to report *that* and *why* it E-stopped.
3. **Stop category** (IEC 60204-1):
   - **Category 0:** immediate power removal. Simple, but a heavy arm freefalls and a fast base coasts. Use for small/light platforms.
   - **Category 1:** controlled deceleration under drive power, THEN power removal (timed, e.g., 500 ms, enforced by a safety relay with delayed output). Standard for arms and larger mobile bases. The delay timer is in the safety relay, not in software.
   - Mechanical brakes on gravity-loaded joints must be **spring-applied, power-released** — power loss engages the brake. Wire brake release power on the motor bus side so E-stop also drops the brakes.
4. **Dual-channel for anything that can hurt a person:** two contacts in the E-stop button, two relay channels, cross-monitored by a safety relay (Pilz PNOZ, SICK Flexi, Phoenix PSR class). Single-channel is acceptable only for small hobby/lab platforms with no human-injury potential.
5. **Software E-stop ≠ E-stop.** A UI stop button or CAN quick-stop is a *functional* stop. It complements, never replaces, the hardware chain.

### 5.2 Reference E-stop wiring

```
 24V_logic ──[E-stop ch1 NC]──[Interlock chain NC]──► Safety relay A1
 24V_logic ──[E-stop ch2 NC]──[Interlock chain NC]──► Safety relay A2 (channel 2)
 Safety relay safe output ──► Main contactor K1 coil (and STO inputs on drives)
 Safety relay aux (NO) ──► GPIO to compute: "E-stop status" (monitoring only)
 Reset: momentary button → safety relay reset input (manual, deliberate re-arm)
```

- **NC (normally closed) contacts throughout**: a broken wire = stop. NO contacts in a stop chain are a design error, full stop.
- Modern servo drives offer **STO (Safe Torque Off)** inputs — dual-channel, kills gate drive power inside the drive. Wiring the safety relay to STO instead of (or in addition to) a bus contactor gives Category 0/1 stops without breaking DC under load, and avoids contactor arcing. For multi-drive robots: safety relay → all STO inputs in parallel, contactor as the second/backup channel.
- The contactor must be rated for **DC at your bus voltage** (DC arcs don't self-extinguish; an AC-rated contactor at 48 VDC under load will arc and weld). Look for DC-rated contactors (e.g., TE Kilovac EV200 class for high current, or DC-rated IEC contactors) and check the *break* rating, not just carry.
- Verify the whole chain in commissioning: press E-stop at full speed, with a payload, at low battery. Log bus voltage during the event — regen with the pack disconnected (Section 2.5) shows up here.

---

## 6. Power Sequencing

**Rule: logic up → sensors up → drives powered → drives enabled. Reverse on shutdown.** Violations cause: motor twitch at boot (gate driver inputs floating while compute boots), corrupted SD cards / filesystems (logic loses power while writing), CAN bus errors from half-powered nodes, USB enumeration failures.

Practical implementation:

1. **Key switch / soft power button** energizes logic DC-DCs only.
2. Compute boots, runs self-test, verifies BMS comms, E-stop chain healthy, no faults.
3. Software commands motor-bus power: precharge sequence (Section 4) → main contactor closes. This command path goes through the safety relay's enable, so it can't override an active E-stop.
4. Drives initialize on a powered bus, software clears faults, *then* enables torque — explicitly, last.
5. **Shutdown:** disable torque → open motor contactor → `shutdown -h` the compute → a supervisor circuit (small always-on µC or PMIC with e.g. 30 s timeout) cuts logic power after the OS halts. Never let the key switch directly cut compute power — use it as a *request* GPIO; this single decision eliminates the entire class of corrupted-filesystem field returns. Use read-only root filesystems or journaling + sync discipline as defense in depth.
6. **Brownout behavior:** define what happens at every voltage. e.g., < 42 V: software low-battery warning; < 40 V: torque off + return to dock disabled, request shutdown; < 39 V: BMS cuts discharge (hard). Software thresholds must trigger BEFORE hardware ones, always.

Per-rail sequencing inside the logic domain (e.g., FPGA/SoC rails) is normally handled by the SoM/carrier — don't reinvent it; do honor the carrier's power-good outputs before releasing peripherals from reset.

---

## 7. DC-DC Conversion — Sizing and Derating

### 7.1 The derating rules that matter

- **Power: load converters to ≤ 70–80% of rating** at your real ambient. Datasheet ratings are typically at 25 °C with ideal airflow; inside a sealed robot chassis ambient is 45–60 °C. Check the derating curve: many "150 W" modules are 100 W at 60 °C. If there's no derating curve in the datasheet, assume the worst.
- **Input voltage: full pack range + transients.** For a 13S pack: spec 36–75 V input (e.g., standard "48 V telecom" range 36–75 V fits perfectly). Verify undervoltage lockout is below your worst-case sag (Section 2.4).
- **Peak vs. continuous loads:** compute modules (Jetson/NUC class) have 2–3× power spikes on GPU load steps; USB devices spike at enumeration. Size for measured peak, not TDP. Put a current probe on every rail during the heaviest software workload before freezing the design.

### 7.2 Rail budget worked example

| Rail | Loads | Continuous | Peak | Converter pick |
|---|---|---|---|---|
| 12 V | Jetson Orin carrier (60 W pk), router (10 W), lidar (15 W) | 55 W | 85 W | 150 W module (85/150 = 57% ✓) |
| 5 V | USB cameras ×3 (12 W), GPS, LEDs | 18 W | 30 W | 60 W module |
| 24 V | Contactor coil (8 W), safety relay (3 W), e-brake release (15 W) | 26 W | 40 W (coil pull-in) | 75 W module |

Add 20% future margin on top — every robot gains sensors after rev A.

### 7.3 Selection details that bite

- **Isolated vs. non-isolated:** isolated (e.g., quarter-brick, Mean Well SD/RSD, Vicor DCM) for the logic rails on robots with motor noise problems or chassis-grounded sensors — isolation breaks ground loops by construction (Section 8). Non-isolated bucks are fine for sub-rails derived from an already-clean 12 V.
- **Synchronous bucks and pre-bias:** some sync bucks sink current into a pre-biased output at startup or back-feed when disabled — matters when rails share loads. Check for monotonic pre-biased startup.
- **EMI:** switching converters near IMUs and magnetometers cause real sensor corruption. Keep converters ≥ 10 cm from magnetometers, use shielded-inductor modules, add a π-filter (LC) on converter inputs feeding sensitive analog.
- **Fusing: fuse every output branch**, sized at ~1.5–2× continuous load, with wire gauge rated above the fuse. The harness, not the converter, is what catches fire. Blade-fuse blocks or resettable breakers at the PDB; PTC polyfuses only for < 2 A convenience loads (their trip is slow and temperature-dependent).
- **Connector ratings:** derate connector current 50% for connectors that see mating cycles (Anderson PP, XT60/90 contact resistance rises with wear). Hot-unplug under load pits contacts — design so it can't happen (interlock pin or last-mate/first-break ground).

---

## 8. Grounding Architecture and Motor Noise Isolation

### 8.1 The star ground rule

All current returns meet at ONE physical point — the power distribution board's ground plane or the pack negative bus bar:

```
                      ┌── Motor driver returns (HIGH di/dt — heavy gauge, short)
 Pack (−) ── STAR ────┼── Logic DC-DC returns
  point (PDB bus bar) ├── Chassis bond (single point, deliberate)
                      └── Shield drain terminations
```

**Why:** motor phase currents are tens of amps with sharp di/dt. Any shared return conductor between motor and logic turns into a voltage source: `V = I×R + L×di/dt`. Even 5 mΩ of shared return at 40 A of switching ripple = 200 mV of ground bounce riding on every logic-level signal that crosses domains — enough to corrupt encoder edges, shift ADC readings, and cause "random" CAN errors that correlate with motor load.

**Rules:**
1. Motor power returns run directly to the star, in their own conductors, never daisy-chained through a logic board.
2. Never use the chassis as a return conductor. Bond chassis to ground at exactly one point (for ESD and EMC), with a deliberate strap.
3. Signals crossing from the motor domain to logic (encoder, current sense, hall) should be **differential** (RS-422 encoders, CAN) or **isolated** (digital isolators, isolated amps). Single-ended 3.3 V encoder signals shared with a motor driver ground are a debugging nightmare on day 30.
4. Cable shields: terminate 360° at the driver/connector backshell end; for low frequency ground-loop concerns terminate one end only, but for motor cable shields (high-frequency PWM noise) terminate **both** ends to chassis — the loop-current concern is outweighed by HF shielding effectiveness. Motor phase wires: twist or use shielded motor cable, keep them away from sensor harnesses (separate by ≥ 5 cm or cross at 90°).

### 8.2 Diagnosing power/ground problems — methodology

Symptoms → likely cause:

| Symptom | First suspect | Test |
|---|---|---|
| Compute reboots under motor load | Bus sag below DC-DC UVLO | Scope DC-DC input, DC-coupled, trigger on dip, during max-load maneuver |
| Encoder counts jump/glitch when motors run | Ground bounce on single-ended encoder | Scope encoder GND vs. logic GND (differential probe), look for PWM-correlated noise |
| CAN errors correlate with motor current | Shared return / shield termination | Error counters vs. motor load; check shield and star wiring |
| IMU/mag drift when drives enabled | Converter or motor magnetic coupling | Compare sensor output drives-off vs. drives-on, robot stationary |
| Connector warm/discolored | Worn contacts, inrush pitting | Millivolt drop across connector at known current → resistance |
| Random BMS disconnects | Overcurrent margin too tight, or one weak P-group | Pull BMS logs; per-group voltages under load |

**Tools:** a current probe (Hantek CC-65 minimum, Tektronix TCP class properly) and a differential voltage probe are not optional for power bring-up. Scope ground clips across domains create the very ground loops you're hunting — use differential probes or battery-powered scopes for cross-domain measurements. Log bus voltage and current at ≥ 1 kHz in the robot's own telemetry permanently; the field failure you can't reproduce will be in that log.

---

## 9. 48 V — Why It's the Industry Default and What Changes

The robotics industry (AMRs, humanoids, mobile manipulators) has converged on 48 V-class buses (13S Li-ion):

- **I²R:** power loss scales with 1/V² for the same power. 1 kW at 48 V is 21 A; at 12 V it's 83 A — 16× the conduction loss in the same copper. Harness mass and connector cost drop dramatically.
- **Safety boundary:** 54.6 V max stays under the 60 V DC SELV threshold — no high-voltage training, simpler enclosure requirements, touch-safe.
- **Ecosystem:** telecom 36–75 V DC-DC bricks, 48 V BLDC drives (ODrive/moteus/Solo class through industrial), 48 V e-bike/LEV cells and chargers are all commodity.

Design changes vs. 12/24 V systems: precharge becomes mandatory (energy in caps scales with V²), DC arc behavior on contactors is much more serious (DC-rated breaking devices only), FET selection moves to 80–100 V parts (60 V FETs have zero margin over a 54.6 V pack + regen), and TVS/clamp strategy must be explicit. Above 48 V-class (e.g., 800 V automotive practices) is out of scope here — different discipline entirely.

---

## 10. Design Review Checklist

Run this before any power PCB or harness goes to fab/build:

**Pack & BMS**
- [ ] S×P sized for *current* with 0.7 cell derating, not just energy
- [ ] Downstream tolerates V_min(sag) to V_max + regen (≈ 1.15 × V_charge)
- [ ] BMS fault output wired to compute; BMS data in telemetry
- [ ] Charge inhibit below 0 °C (NMC/LFP)
- [ ] Pack fuse at pack terminals; rated DC, interrupt rating > worst-case short current

**Inrush & E-stop**
- [ ] Precharge on any cap bank > 500 µF; resistor pulse-energy checked; retry-limited; precharge *verified by voltage measurement* before main close
- [ ] E-stop chain: NC contacts, hardware-only, dual-channel if human-injury potential, Category 0/1 decided deliberately
- [ ] E-stop cuts motor bus only; logic survives; status visible to software
- [ ] Contactor DC break rating ≥ bus voltage at max load current; STO used where drives support it
- [ ] Spring-applied brakes on gravity axes, released by motor-bus-side power

**Sequencing & conversion**
- [ ] Boot order: logic → checks → precharge → contactor → drive enable; shutdown is the exact reverse with supervised compute halt
- [ ] Every DC-DC ≤ 80% loaded at real chassis ambient; UVLO below worst-case sag
- [ ] Every branch fused; wire gauge > fuse rating; measured (not estimated) peak currents
- [ ] Brownout thresholds: software warns before software stops before BMS cuts

**Grounding**
- [ ] Single star point; motor returns never share conductors with logic
- [ ] Chassis bonded once; signals crossing motor↔logic domains differential or isolated
- [ ] Converters ≥ 10 cm from magnetometer; motor cables shielded and segregated from sensor harness

**Verification (commissioning)**
- [ ] Scope bus during: power-up, E-stop at speed, max-acceleration, stall, regen at full charge
- [ ] Thermal survey of connectors, fuses, converters after 30 min at duty-cycle load
- [ ] E-stop functional test under worst-case load; verify brakes engage
- [ ] Telemetry logging bus V/I at ≥ 1 kHz, retained across reboots
