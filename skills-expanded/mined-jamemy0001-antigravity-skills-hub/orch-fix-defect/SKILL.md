---
name: orch-fix-defect
description: Orchestrate fixing a bug — reproduce it as a failing regression test, fix to green, review, and gated commit — by delegating each phase to the matching ECC agent. Use when existing behavior is broken or wrong.
metadata:
  origin: ECC
aliases:
  - orch-fix-defect
  - fix-defect
  - bug-fix
category: "02 - Bug Fixing & Defect Resolution"
tags:
  - agent-skill
  - debugging
  - defect-fixing
  - stage-2
---

# orch-fix-defect

Actor · action · target: **orch · fix · defect**. Rigorous workflow for defect resolution and regression prevention.

## When to Use

- Something is **broken**: wrong output, an error, a crash, a regression.
- Distinguish from siblings:
  - behavior is correct but you want it different → feature modification.
  - the capability does not exist yet → new feature development.

## Operation settings

- **Phase 1: Root Cause Investigation:**
  - Route non-obvious root causes directly to [[Skills/systematic-debugging/SKILL|systematic-debugging]].
  - Investigate logs, trace data flows, and form a testable hypothesis before touching application code.
- **Phase 2: Failing Test Reproduction (Red):**
  - Route test reproduction to [[Skills/tdd-workflow/SKILL|tdd-workflow]].
  - Reproduce the bug as a **new failing regression test** (RED). Proving the bug exists first is what separates an engineering fix from guesswork.
- **Phase 3: Surgical Fix (Green):**
  - Implement minimal, targeted fix to turn the regression test green.
  - Apply [[Skills/error-handling/SKILL|error-handling]] patterns with typed exceptions.
- **Phase 4: Quality Gate & Verification:**
  - Invoke [[Skills/verification-before-completion/SKILL|verification-before-completion]] before claiming completion.
  - Run full test suite, verify clean git diff, and run [[Skills/review/SKILL|review]].

## Example

```
orch-fix-defect: poller crashes on empty NWS response
→ systematic-debugging isolates null pointer in payload unmarshaling
→ write failing regression test reproducing the crash (RED)
→ surgical fix to handle empty payload safely (GREEN)
→ verification-before-completion runs full suite
→ commit fix: handle empty NWS response
```

---

## 🔗 Connected Skills (ทักษะที่เกี่ยวข้อง)
- [[Skills/systematic-debugging/SKILL|systematic-debugging]] — วินิจฉัยหาสาเหตุรากเหง้าอย่างเป็นระบบ 4 ขั้นตอน
- [[Skills/tdd-workflow/SKILL|tdd-workflow]] — วงจรเขียน Test ยืนยันบั๊กก่อนแก้โค้ดจริง
- [[Skills/error-handling/SKILL|error-handling]] — จัดการข้อผิดพลาดและ Exception Hierarchy
- [[Skills/verification-before-completion/SKILL|verification-before-completion]] — ตรวจสอบและรันเทสต์ครบถ้วนก่อนปิดงาน
- [[Skills/review/SKILL|review]] — ตรวจทานโค้ดหลังแก้ไข

<!-- v1.1.0 synchronized: 2026-09-29 -->
