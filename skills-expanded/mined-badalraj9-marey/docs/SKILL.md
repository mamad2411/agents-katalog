# SKILL.md — Marey Architecture Guide for Coding Agents

## What You Are Building

Marey is a **pixel-primary, event-driven perceptual infrastructure layer for AI agents** that need to control a computer. It replaces brute-force screenshot loops with a hierarchical sentinel pipeline modelled on biological vision.

Read this entire file before writing a single line of code. Then read `docs/interfaces.md` for exact method signatures, `docs/dependencies.md` for import rules, and `docs/config.md` for all configuration.

---

## The Golden Rules

These are absolute. Never violate them.

1. **No module reaches into another module's internals.** All inter-module communication flows through defined interfaces or the nerve/ event bus.
2. **All shared types live in `marey/types/` only.** Never define ROI, Frame, Region, ActionPlan, or any shared dataclass in any other module.
3. **Import rules are law.** See `docs/dependencies.md`. A module that imports above its layer is wrong.
4. **Pixel pipeline is primary. spine/ only enriches.** spine/ never decides, never leads, never gates.
5. **Agents never receive a full screenshot.** Ever. Only deltas and ROI crops.
6. **Every threshold and tunable value lives in `marey/config.py`.** No magic numbers in module code.
7. **iris/ runs across all layers.** Blacklisted regions never enter the pipeline at any point.
8. **The sentinel loop must never block.** All extraction is async, off-thread, fire-and-forget.
9. **nerve/ queue is always bounded.** Never use an unbounded queue anywhere in the codebase.
10. **VerificationContract is always machine-readable.** Never a natural language string.

---

## Module Naming Convention

All modules use biological naming. Do not rename them. Do not create new top-level modules without explicit instruction.

```
retina/     raw pixel capture
sentinel/   peripheral vision loop
cortex/     salience scoring
fovea/      high-res extraction
atlas/      world model
nerve/      event bus
lobe/       reasoning backends
reflex/     action executor
spine/      accessibility enrichment
iris/       privacy layer
lens/       public agent SDK
types/      shared dataclasses — no logic, only definitions
```

---

## File Naming Convention

- Interfaces / abstract base classes: `base.py`
- Platform-specific implementations: `{platform}_backend.py`
- Main logic class for a module: name matches the module concept (e.g. `loop.py` for sentinel loop, `model.py` for world model)
- No `utils.py` dumping grounds. If utility functions exist, they belong in the module that uses them.

---

## Build Order — NEVER Skip Ahead

Build strictly in this sequence. Each phase depends on the previous.

```
Phase 1:  types/          shared dataclasses
Phase 2:  retina/         capture backend
Phase 3:  sentinel/       frame diff pipeline
Phase 4:  cortex/         salience scoring
Phase 5:  fovea/          high-res extraction
Phase 6:  atlas/          world model
Phase 7:  nerve/          event bus
Phase 8:  spine/          accessibility enrichment
Phase 9:  iris/           privacy layer
Phase 10: lobe/           reasoning backends
Phase 11: reflex/         action executor
Phase 12: lens/           public SDK
Phase 13: bench/          benchmark harness
```

Do not start Phase 3 until Phase 2 has passing unit tests. Do not start Phase 6 until Phase 5 has passing unit tests.

---

## Types — The Most Important Module

`marey/types/` is the shared vocabulary of the entire system. Get this right before everything else.

Every type is a frozen dataclass or Enum. No logic. No methods beyond `__post_init__` validation.

Core types to define in Phase 1:

```python
# Enums
ChangeType      # appeared | disappeared | modified | moved
ContentType     # text | table | image | form_field | button | unknown
ActionType      # click | type | scroll | hotkey | wait
BackendType     # claude_api | local_vlm | hybrid

# Dataclasses
MonitorInfo     # id, width, height, scale_factor, is_primary
Frame           # id, monitor_id, window_id, pixels, resolution, timestamp, scale_factor
ROI             # id, frame_id, x, y, w, h, change_type, sentinel_score, salience_score, pixel_hash, timestamp, consecutive_frames
Region          # id, roi_id, content, content_type, confidence, label, role, coords, precise_coords, last_changed, history, is_blacklisted
ActionStep      # action, target, value, delay_ms, description
VerificationContract  # region_coords, expected_content, expected_role, disappeared, appeared, timeout_ms
ActionPlan      # goal_id, analysis, confidence, steps, expected_result, verify_region, fallback, created_at
```

---

## Sentinel Loop — Critical Constraints

The sentinel loop runs on its own thread. It must:

- Never block on extraction — fire extraction off-thread via ThreadPoolExecutor
- Cap at adaptive FPS — 30Hz max when active, 2Hz when idle
- Process frames at 10–15% resolution for diff only
- Apply temporal gate: ROI must show sustained change for N consecutive frames before propagating
- Classify change type correctly: appeared / disappeared / modified / moved

The sentinel loop must NOT:
- Import from fovea/, atlas/, nerve/, lobe/, reflex/
- Do any extraction, OCR, or semantic analysis
- Block on any downstream operation

---

## Cortex — Salience Scoring Constraints

cortex/ must score each ROI in under 2ms on CPU. This is a hard constraint.

Scoring stack (apply in order, stop early if score is definitive):
1. Hardcoded rules first — known noise patterns get score 0.0 immediately
2. CLIP zero-shot cosine similarity — semantic salience
3. ONNX classifier — if available and CLIP is insufficient

Known noise to suppress in rules.py (score = 0.0):
- Circular/oscillating bounding boxes over time → animation
- Very small ROIs (area < MIN_ROI_AREA from config) → cursor artifacts
- Regions matching known clock/ticker positions if configured
- Regions with zero text content after extraction attempt

---

## Fovea — Extraction Constraints

fovea/ always does 2-pass coordinate resolution:
1. Pass 1: sentinel-derived bbox (approximate, ±5px)
2. Pass 2: re-capture at native resolution within that bbox, detect precise element boundaries

Pass 2 coordinates are what get stored in Region.precise_coords and what reflex/ uses for actions. Never use Pass 1 coordinates for action targeting.

Extractor auto-selection logic:
```
region content_type == table   → table.py extractor
region has clean text contrast  → tesseract with PSM 6
region has styled/mixed text    → easyocr
confidence < 0.6 after OCR     → vision model fallback
```

---

## Atlas — World Model Constraints

atlas/ is a cache, not ground truth. Treat it as such.

- Every region entry has a confidence score
- Low confidence entries (< ATLAS_MIN_CONFIDENCE from config) are flagged, not committed
- reconciler.py runs a full-frame ground truth check every RECONCILER_INTERVAL seconds
- When reconciler detects drift, emit WorldModelDrift event via nerve/
- History list is capped at REGION_HISTORY_CAP entries (from config)
- delta() must return only what changed since the given timestamp, never the full state

---

## Nerve — Event Bus Constraints

nerve/ queue is always bounded. Use NERVE_QUEUE_MAX_DEPTH from config.

Drop policy: drop newest (incoming event dropped if queue full, not oldest — oldest events are more likely to still be relevant).

Staleness TTL: if an ROI event sits in queue longer than NERVE_STALENESS_TTL_MS, discard it — the screen has changed again.

WebSocket server binds to 127.0.0.1 only by default. Never 0.0.0.0 unless MAREY_WS_PUBLIC=true is explicitly set in config.

All events carry: timestamp, source_module, session_id alongside their payload.

---

## Lobe — Reasoning Backend Constraints

lobe/ never receives a full screenshot. It receives:
- delta from atlas/ since last action
- world snapshot (structured, not pixels) for relevant regions
- ROI crop images only for regions flagged as ambiguous

ActionPlan must be validated against ActionPlan schema before returning. Reject any plan where coordinates are not from fovea/ 2-pass resolution.

Hybrid routing logic:
```
local VLM confidence >= HYBRID_LOCAL_THRESHOLD → execute local plan
local VLM confidence < HYBRID_LOCAL_THRESHOLD  → escalate to Claude API
```

---

## Reflex — Executor Constraints

reflex/ executes the full ActionPlan without re-engaging lobe/ per step.

After plan execution:
1. Take verification snapshot of verify_region at native resolution
2. Compare against VerificationContract
3. Match → emit ActionPlanExecuted event
4. Mismatch → emit VerificationFailed event with delta between expected and actual

reflex/ never invents coordinates. All coordinates come from ActionPlan which got them from fovea/ 2-pass resolution.

---

## Iris — Privacy Constraints

iris/ is always-on. It runs at every layer that touches pixel data.

Blacklist check must happen:
- At retina/ before a frame is passed to sentinel/
- At fovea/ before any crop is extracted
- At lobe/ before any image is sent to a model

Secure field detection:
- Check accessibility role first: AXSecureTextField, PasswordField, password type input
- If role unavailable, check pixel heuristics: asterisk/dot character patterns in text fields
- If either matches: mark region is_blacklisted=True, never extract, emit PrivacyBlocked event

Audit log: append-only, local file, records window_id + action_type + timestamp. Never records content.

---

## Testing Expectations

Every module gets a unit test file in `tests/unit/test_{module_name}.py`.

Fixtures live in `tests/fixtures/`:
- Sample screen crops as PNG files
- Mock frame objects as pickle files
- Mock ROI lists for testing salience and extraction

Integration tests in `tests/integration/` test the full path across layers.

Use pytest. No other test framework.

---

## What Not To Do

- Do not use `print()` for debugging. Use Python `logging` with the marey logger.
- Do not catch bare `Exception`. Catch specific exceptions.
- Do not hardcode any threshold, interval, or size value. Use config.py.
- Do not write synchronous blocking code in the sentinel loop.
- Do not import from a higher layer than your current module.
- Do not define types outside types/.
- Do not expose raw pixel arrays to lobe/ or lens/.
- Do not write to the audit log from anywhere except iris/.
- Do not bind WebSocket server to 0.0.0.0 by default.
- Do not send full screen images to any reasoning backend.
