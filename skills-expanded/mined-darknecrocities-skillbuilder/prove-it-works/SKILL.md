---
name: prove-it-works
description: Mandatory runtime verification and evidence protocol (/prove-it-works, /prove, /show-me-your-work). Bans "it compiles" completions, requires bug repro-first, enforces benchmark Explain-the-Number checks, and mandates honest unverified disclosure.
---

# Prove It Works (`/prove-it-works`, `/prove`, `/show-me-your-work`)

> **Role**: Verification & Reliability Gatekeeper  
> **Philosophy**: *Compilation is not proof. Typecheck is not proof. Never hand the human a check you could run yourself. Every claim carries its evidence.*

This skill enforces strict runtime proof across code, UI, mascots, brand assets, data pipelines, and benchmarks.

---

## 1. Quick Navigation & References

| Resource | Purpose |
| :--- | :--- |
| [references/verification-and-evidence-contract.md](references/verification-and-evidence-contract.md) | Proof hierarchy, repro-first rules, `Explain the Number` benchmark audit, and evidence tags. |

---

## 2. The Five Non-Negotiable Proof Laws

1. **Real Artifact Over Proxy**:
   - Run the actual test suite, CLI command, server endpoint, build, or browser/asset validator on the modified target — never claim pass from reading code or mocking out the system under test.
2. **Repro-First for Bug Fixes**:
   - Before fixing a bug, run or author a failing test/probe demonstrating the failure. After the fix, run the exact same check and observe it turn green.
3. **Never Hand the Human Your Check**:
   - If a test, build, curl, linter, or browser check can run locally, execute it yourself and inspect the full output.
4. **Explain the Number (`benchmark-checklist`)**:
   - Any reported latency, speedup, bundle KB, or token saving must specify baseline vs after, sample size, bottleneck isolated, and artifact exclusions (no warm-cache illusions).
5. **Honest Unverified Disclosure + Documentation Impact**:
   - Disclose any surface not executed (e.g., missing credentials, native device hardware) and state either the docs updated or `Documentation impact: none — <reason>`.

---

## 3. Evidence Labeling Standard in Replies

- **`[measured]`**: Directly observed in tool output run *after* the final edit.
- **`[inferred]`**: Derived from inspected code/math without live execution.
- **`[guess]`**: Unverified hypothesis (must be flagged explicitly, never stated as fact).

---

## 4. Verification Receipt Template & Trail Logger

For long or multi-phase tasks, record proof rows to `.agents/memory/decision_trail.tsv`:
```bash
python3 skills/darknecrostack/scripts/log_decision_trail.py \
  --step "verify-phase" \
  --hypothesis "All skills pass depth and anti-slop checks" \
  --action "python3 scripts/skill_linter.py --all --strict-depth" \
  --result "PASS" \
  --evidence "48/48 passed, 0 violations"
```
