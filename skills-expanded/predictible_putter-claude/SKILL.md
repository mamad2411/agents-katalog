# Predictible Putter

## 1. Purpose of this document
This file is the shared source of truth for the project's vision, constraints, and
working method. It is read at the start of every session. It is **not** a specification
of the software itself — specifications live in `specs/` (see §5). When the two disagree,
the relevant spec wins for implementation details, and this file wins for process and vision.

## 2. Project vision
Build a device and companion software that measures a golf putting stroke in order to help
the user **train repeatable putting force** (so the ball rolls a consistent, predictable
distance) and to **detect club-face rotation** through impact.

The core insight driving the hardware approach: at ball impact there is a measurable spike
in accelerometer data. From the stroke's motion and that impact signature we aim to derive:
- **Impact power / stroke strength** — a proxy for how fast the ball will roll.
- **Club-face rotation** — whether the face is opening/closing through the stroke and at impact.

The long-term training goal: give the user real-time or post-stroke feedback so they can
learn to reproduce a target force on demand.

## 3. Hardware (known facts)
- **MCU / board:** ESP32-WROOM-32 module on a generic ESP32 DevKit board (DOIT DevKit V1 /
  ESP32 DevKitC family). Has BLE. Selected in firmware tooling as a generic "ESP32 Dev Module".
- **USB-serial:** CP2102 (Silicon Labs CP210x driver on Windows; built into Linux/WSL kernel).
- **Flashing port:** Micro-USB (requires a data-capable Micro-USB cable).
- **Sensor:** MPU-6050 6-axis IMU (3-axis accelerometer + 3-axis gyroscope), I²C.
  - Note: the MPU-6050 has a gyroscope in addition to the accelerometer. Face rotation is
    fundamentally an angular-motion measurement, so the gyroscope is likely central to the
    rotation feature, not just the accelerometer.
- **Mounting:** in the rear cavity/indent of a **mallet-style putter head** (behind, not on,
  the face). The sensor is rigidly coupled to the head, so the gyro measures face rotation
  directly and impact transmits with little damping. The sensor sits behind/offset from the
  face center, so impact readings include rotational (lever-arm) effects that the analysis
  must account for. Exact axis orientation to be fixed and calibrated once physically mounted.

## 4. Guiding principles
1. **Spec-driven development.** No feature is built without an agreed spec first (see §5).
2. **Nothing is guessed.** If something is ambiguous and material, we stop and ask. If the
   ambiguity is small and low-risk, best judgment is used and the decision is recorded in
   the relevant spec so it can be reviewed.
3. **Good software design.** Clear separation of concerns, well-defined interfaces between
   layers (firmware ↔ transport ↔ analysis ↔ UI), testability, and readable code that
   matches its surroundings.
4. **Physical grounding.** This is a physics measurement problem. Claims about "force" or
   "speed" must be tied to what the sensors can actually measure and how we derive the value,
   with stated assumptions and limits.

## 5. Spec-driven workflow
Specs are the contract; code follows the spec.

- Specs live in `specs/` as Markdown, one file per capability (e.g. `specs/0001-impact-detection.md`).
- Recommended spec structure:
  1. **Context & goal** — what problem this solves and why.
  2. **Requirements** — numbered, testable statements (functional + non-functional).
  3. **Assumptions & constraints** — including physics assumptions and hardware limits.
  4. **Design** — chosen approach, interfaces/data contracts, alternatives considered.
  5. **Acceptance criteria** — how we know it's done and correct.
  6. **Open questions** — anything unresolved, with a decision or a "needs answer" flag.
- Lifecycle: draft → review together → agree → implement → verify against acceptance criteria.
- Changes to agreed behavior go through the spec first, then the code.

## 6. Architecture (decided; details to be ratified in a spec)
Decided layering:
- **Firmware (on ESP-32):** sample the IMU at a fixed rate, timestamp samples, and stream
  them over **BLE**. Keep it dumb and reliable; analysis lives off-device. (Whether the
  firmware also buffers a short window around impact is TBD.)
- **Transport: BLE.** The device is untethered (battery-powered) and streams to a nearby host.
- **Analysis (off-device, on a desktop host):** stroke segmentation, impact detection,
  force/speed estimation, rotation estimation. **v1 exposes this via a command-line program**
  — no GUI yet.
- **Presentation/feedback:** a **desktop/web app comes later**; for v1, feedback is CLI output.
  The analysis layer must be cleanly separated from the interface so a GUI can be added without
  rewriting the analysis.

## 7. Scope for v1 (decided)
- **Untethered, indoors.** Battery-powered device streaming over BLE, used for indoor putting
  practice (controlled surface, host computer nearby). Outdoor/on-green use is a later goal.
- Primary v1 outcome: detect a putt's impact and report a **repeatable force/strength measure**
  and **club-face rotation** through the CLI, good enough to train consistency.

## 8. Open questions (resolve before/within the first specs)
Hardware & signal:
- MPU-6050 target sample rate and accel/gyro full-scale ranges (to be *specified*, not found:
  proposed 1 kHz sampling, buffered around impact; ranges TBD in the architecture spec).
- Exact axis orientation of the sensor once mounted in the mallet cavity, and calibration
  procedure to map physical axes (target line / vertical / face-normal) to MPU axes.

Analysis & feedback semantics:
- DECIDED: strength is a **relative, unit-less repeatability score** (no physical units in v1).
- DECIDED: trainer supports **both** target+tolerance and session-consistency modes.
- Real-time (per-stroke, immediately) vs. post-session review for v1 feedback? (still open)
- Is per-stroke data logging/history needed in v1, or live output only? (Spec 0001 requires raw
  windows be recordable for replay/testing; user-facing history beyond a session is out of scope.)

## 9. Toolchain & repo
- **Firmware:** PlatformIO + Arduino-ESP32 framework (board = generic "esp32dev"). Lives in `firmware/`.
- **Desktop:** Python — `bleak` (BLE), numpy/scipy (signal), matplotlib (plots). Lives in `desktop/`.
- **Specs:** `specs/NNNN-*.md`. **This file:** process + vision source of truth.

## 10. Current status
- Repo initialized. This CLAUDE.md seeds project context and the working agreement.
- Hardware confirmed (§3): ESP32-WROOM-32 DevKit + CP2102/Micro-USB; MPU-6050 in mallet rear cavity.
- Architecture decided: ESP-32 → BLE → desktop CLI analysis; untethered indoors for v1;
  desktop/web GUI deferred.
- `specs/0001-system-architecture.md` **AGREED (v1)**: window-around-impact capture model;
  desktop stack is Python (bleak/numpy/scipy). Remaining spec items are bring-up tuning (trigger
  threshold, ranges) or a pre-firmware follow-up (firmware framework).
- `specs/0002-analysis-and-scoring.md` **drafted** — strength = relative repeatability score;
  both target+tolerance and session-consistency modes; physics via candidate metrics selected by
  empirical validation. Awaiting review.
- Firmware framework decided: PlatformIO + Arduino-ESP32 (Spec 0001 Q5 closed).
- **Build order (spec-driven):** (1) firmware sensor bring-up — stream raw IMU over USB serial to
  observe a real impact and set ranges/trigger threshold (closes Spec 0001 Q2/Q3, 0002 empirical);
  (2) firmware BLE windowed capture; (3) Python BLE client + recorder; (4) analysis on recorded
  strokes to select/validate the strength metric (Spec 0002).
- Slice 1 built: `firmware/` PlatformIO project + register-level `Mpu6050` driver + serial CSV
  streamer. **Compiles clean** (`pio run` succeeds; not yet flashed to hardware).
- **Next step (needs hardware):** wire the MPU-6050, flash via WSL/usbipd (see `firmware/README.md`),
  capture a real putt, and use that data to set accel/gyro ranges + impact trigger threshold
  (closes Spec 0001 Q2/Q3). Then build Slice 2 (BLE windowed capture).
