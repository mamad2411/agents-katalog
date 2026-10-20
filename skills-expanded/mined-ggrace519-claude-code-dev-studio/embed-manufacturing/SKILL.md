---
name: embed-manufacturing
description: Factory provisioning, test fixtures, yield, traceability, and RMA workflow for embedded products. Auto-invoked when designing manufacturing test, debugging DFx issues, or preparing for a CM handoff.
---

# Embedded Manufacturing

Firmware that works on the bench and fails in the factory is still a product
failure. The bridge between engineering and mass production — test coverage,
serialization, key injection, yield, and the field-return loop — has to be
designed, not improvised at the CM.

## When to reach for this

- Designing factory test stations, fixtures, or the factory-mode firmware path
- Setting up serialization, per-device key injection, or traceability
- Preparing a CM handoff packet, or running yield/CAPA cycles with the CM
- Building RMA intake and field-return failure analysis

## Principles

1. **Design test coverage alongside features.** Every external interface gets a
   factory-test hook before board layout freezes; retrofitting test points after
   layout is how untested units ship. Target ≥95% fault coverage at functional
   test.
2. **Serialization has one source of truth.** A single system issues every
   serial, MAC, IMEI, and per-device key; the CM reads from it and the cloud
   validates against it. Ad-hoc CSV handoffs are the origin of most
   traceability disasters.
3. **Inject keys at the fixture, not in firmware.** Keys come from an HSM at the
   production line, burn once into the secure element, and attest upward.
   Factory images carry no embedded secrets — a leaked factory image must not be
   a fleet compromise.
4. **Track yield like a product metric.** First-pass yield, retest yield, and
   final yield, broken out by station and by day. A 2% drop on one station is
   usually fixture wear or a component-lot change — catch it in days, not weeks.
5. **Build the recall lookup on day one.** "Which shipped units contain this
   component lot?" must answer in minutes: component lot → sub-assembly → unit →
   customer order, as queryable joins.
6. **Make RMA intake automatic.** Every return goes onto a diagnostic fixture
   that pulls crash logs, firmware version, sensor state, and uptime before a
   human touches it. Without captured state, root cause is guesswork.

## Factory test flow — station template

| Station | Verifies | Typical gate |
|---|---|---|
| ICT / flying probe | solder, opens/shorts, passives | per-net pass |
| Program + boot | flash image, secure-boot fuses | boots to factory mode |
| Functional test | every interface via test hooks | ≥95% fault coverage |
| RF / calibration | TX power, sensitivity, sensor cal | within cal limits, values logged |
| Key injection + serialize | HSM-signed identity, label print | attestation verifies against issuer |
| Final / pack-out | cosmetic, accessories, factory-mode locked | factory unlock disabled |

Every station logs unit ID, station ID, measurements (not just pass/fail), and
firmware/fixture versions — that record is the traceability spine.

## CM handoff checklist

- [ ] Test spec per station with numeric pass/fail limits (no "verify it works")
- [ ] Fixture BOM + maintenance/calibration schedule
- [ ] Golden units and known-bad units for fixture validation
- [ ] AVL/BOM under ECN control; substitution requires sign-off
- [ ] Yield thresholds and stop-ship criteria agreed in writing
- [ ] Factory-mode unlock protocol documented — and how it is permanently
      disabled at pack-out

## Pitfalls

- Factory mode reachable on shipped units (or unlockable with a shared secret)
- Pass/fail recorded without measured values — no drift detection, no Pareto
- Calibration data stored only on the unit, not mirrored to the factory DB
- Test fixtures running a different firmware build than production units
- Yield reported as a single aggregate number — station-level drift invisible
- Key injection logs without an audit trail tying each cert to a unit and time
- New cryptographic design (key hierarchy, attestation chain) standing up a
  line without a security review — re-provisioning a built fleet is rarely
  possible

---
*Related: `embed-ota` (post-ship firmware delivery), `embed-connectivity`
(provisioned-credential consumers), `embed-driver` (board bring-up under test)
· domain agent: `embed-architect` · output/ADR format: `playbook-conventions`*
