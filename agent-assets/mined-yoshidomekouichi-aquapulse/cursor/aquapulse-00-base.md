---
description: AquaPulse Project Base Rules
alwaysApply: true
metadata:
  environments: cloud
---

# AquaPulse Base Rules

## Project Overview

AquaPulse: Freshwater aquarium monitoring system

## Language Policy (STRICTLY ENFORCED)

### ⚠️ MANDATORY - Absolutely NO Exceptions

**ALWAYS write in English:**

```
✅ All code (Python, MicroPython, JavaScript, etc.)
✅ All comments in code (inline comments, docstrings, function descriptions)
✅ All commit messages
✅ All ADRs (docs/decisions/*)
✅ All agent rules (.cursor/rules/*)
✅ All API documentation
✅ All technical reference documents
```

**Before writing ANY file, check:**

```
[ ] Is this code? → MUST be English
[ ] Is this a comment in code? → MUST be English
[ ] Is this a commit message? → MUST be English
[ ] Is this an ADR (docs/decisions/*)? → MUST be English
[ ] Is this a rule file (.cursor/rules/*)? → MUST be English
```

### ✅ MANDATORY - With Documented Exceptions Only

**Documentation (docs/*): English by default**

**Approved exceptions (Japanese allowed):**

```
1. README.ja.md
   - Japanese version of main README
   
2. docs/guides/aquarium-thermostat-complete-manual.md
   - User explicitly requested "超初心者向け" Japanese guide
   - Exception approved: 2026-07-11
```

**Adding new exceptions:**

```
To add a new Japanese document:
1. User MUST explicitly request Japanese
2. Document reason in this rule file
3. Use -ja.md suffix for new files (e.g., guide-ja.md)
4. English version should exist or be planned
```

**Before writing documentation, check:**

```
[ ] Is this in docs/*? → Default: English
[ ] Is this README.ja.md? → Japanese OK
[ ] Is this aquarium-thermostat-complete-manual.md? → Japanese OK
[ ] Is this a new file? → English unless user explicitly requests Japanese
```

### ✅ ALWAYS Allowed in Japanese

```
User communication (this chat): Japanese OK
```

### ❌ Common Mistakes to Avoid

```
✗ Writing Japanese comments in Python code
✗ Writing Japanese in new documentation without approval
✗ Mixing English and Japanese in same file (except bilingual docs)
✗ Assuming "user-facing" means Japanese is OK (still need approval)
```

### 🔍 Self-Verification Process

**Before every file write/edit:**

1. Check file path
2. Check approved exceptions list above
3. If not in exception list → MUST be English
4. If uncertain → Ask user for clarification

## Architecture Decision Records (ADR)

**MANDATORY: Always check ADRs before major decisions**

```
1. Read docs/decisions/README.md
2. Search existing ADRs by keyword
3. Verify no contradictions with existing ADRs
```

**MUST create new ADR when:**

✅ **Schema changes** (database, API contracts, data models)
   - Example: BigQuery schema redesign → ADR-0006

✅ **Technology/library selection** (languages, frameworks, major dependencies)
   - Example: python-kasa vs tapo library selection

✅ **Architecture changes** (system design, component structure, data flow)
   - Example: ESP32+GCP migration → ADR-0001

✅ **Infrastructure decisions** (deployment strategy, CI/CD, storage tiers)
   - Example: Git working_directory strategy → ADR-0003

✅ **Decisions with 3+ alternatives considered** (clear trade-offs)
   - Example: Single table vs dual table design → ADR-0006

**MUST NOT create ADR for:**
- Reversible changes in <1 week (code refactoring, variable naming)
- Obvious choices (standard library selection)
- Personal preferences (code formatting, style)

**Process (mandatory in PR):**

```
1. Create ADR file: docs/decisions/YYYY-MM-DD-title.md
2. Use template.md structure (Status, Context, Alternatives, Decision, Consequences)
3. Add to docs/decisions/README.md "Active Decisions" list
4. Include ADR in same PR as implementation
5. Update docs/architecture/snapshots/ if architecture changes
```

**Self-check before creating PR:**

```
[ ] Did I change a schema (database/API)? → ADR required
[ ] Did I select/replace a library/technology? → ADR required
[ ] Did I modify system architecture? → ADR required
[ ] Did I compare 3+ alternatives? → ADR required
[ ] Is this decision hard to reverse? → ADR required
```

If any checkbox is checked, create ADR proactively without user request.

### Tech Stack

```
Hardware:
  - ESP32 (MicroPython)
  - DS18B20 temperature sensor
  - Tapo T310/P300

Cloud:
  - GCP (Pub/Sub, Cloud Functions, BigQuery)
  - Grafana Cloud

Infrastructure:
  - Terraform
  - GitHub Actions

Languages:
  - Python (see 30-python-coding.mdc for standards)
  - MicroPython (see 31-micropython.mdc for standards)
```

**Note:** Detailed coding standards moved to language-specific rule files (30-python-coding.mdc, 31-micropython.mdc)

### Directory Structure

```
aquapulse/
├─ esp32/              # ESP32 MicroPython code
├─ cloud-functions/    # GCP Cloud Functions
├─ terraform/          # Infrastructure code
├─ docs/               # Documentation
└─ .cursor/rules/      # This directory
```

## Project-Specific Constraints

### Hardware Constraints

```
Raspberry Pi:
  - Assumed "dead" (no SSH, unrecoverable)
  - Do not use

ESP32:
  - Sensors fixed to aquarium
  - USB physical connection required (initial development)
  - IP issues cannot be fully avoided
  - Expect 3-5 code rewrites
```

### Development Constraints

```
Avoid overly optimistic estimates:
  - Clarify limitations of mock testing
  - Sensor reading requires real hardware
  - Clearly separate "can do" from "cannot do"

Prioritize proven implementations:
  - Adopt battle-tested technology
  - Provide reference links
```

## Absolute Rules

```
1. No direct commits to main branch
2. No skipping PRs
3. No force push to main
4. Always consider sensor physical constraints
5. Avoid optimistic estimates
```