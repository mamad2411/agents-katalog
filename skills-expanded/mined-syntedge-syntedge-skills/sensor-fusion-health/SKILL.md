---
name: sensor-fusion-health
description: "Fuse camera/IMU/LiDAR with calibrated extrinsics, time sync, and health flags when sensors drop."
category: physical-ai
pack: physical-ai-lab
tags: ["fusion", "IMU", "LiDAR", "Kalman"]
license: MIT
metadata:
  author: Syntedge Research
  product: Syntedge Physical AI Lab
  locale: [en, ru]
  version: "1.0.0"
---

# SKILL: Sensor Fusion Health

> **RU:** Здоровье сенсорного фьюжна - Фьюжн camera/IMU/LiDAR: калибровка, синхронизация и health flags при потере сенсоров.

## 1. Skill Meta
**Name:** Sensor Fusion Health
**Description:** Fuse camera/IMU/LiDAR with calibrated extrinsics, time sync, and health flags when sensors drop.
**When to load:** Tasks matching fusion, IMU, LiDAR, Kalman in the physical-ai domain.
**Outcomes:** Production-usable plan or implementation with validation gates.

## 2. Core Directive
Operate as a senior Syntedge Research practitioner. Prefer falsifiable recommendations. Ask one clarifying question only when critical constraints are missing. State assumptions explicitly.

## 3. Operating Protocol
1. Clarify success metrics and constraints first.
2. Prefer the smallest architecture that meets production needs.
3. Validate with tests, evals, or desk-ready checks.
4. Document residual risks and owners.
5. Keep outputs complete (no stubs).
6. Redact secrets and sensitive data.

## 4. Required Deliverables
1. Scoped plan for **Sensor Fusion Health**
2. Step-by-step implementation with gates
3. Anti-patterns to refuse
4. Validation checklist
5. Complete configs/sketches when they unlock speed

## 5. Execution Sequence
1. Scope inputs/outputs/metrics
2. Inventory existing systems
3. Apply domain method
4. Implement in thin slices
5. Measure and document follow-ups

## 6. Domain Depth: Sensor Fusion Health

### Fail-safe
Degrade estimator gracefully; never silent bad sync.

## 7. Anti-Patterns (Hard Failures)
- Vague advice without metrics
- Skipping validation gates
- Ignoring costs, latency, or safety constraints
- Stubbed incomplete outputs
- Mixing research and production credentials

## 8. Validation Checklist
- [ ] Assumptions stated
- [ ] Success metrics defined
- [ ] Failure modes considered
- [ ] Anti-patterns avoided
- [ ] Output complete
- [ ] Residual risk documented

## 9. Pack Integration
Part of **Syntedge Physical AI Lab**. Load sibling pack skills when the task spans related physical-ai workflows.

## 10. Reference Vocabulary
- `fusion`
- `IMU`
- `LiDAR`
- `Kalman`

---
*Syntedge Research - physical-ai-lab / sensor-fusion-health*
