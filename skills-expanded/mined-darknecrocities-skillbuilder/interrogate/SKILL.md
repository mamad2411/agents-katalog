---
name: interrogate
description: Adversarial pre-ship code review and surgical diff unslop protocol (/interrogate, /unslop, /deslop). Audits correctness, security, concurrency, leaks, and strips AI bloat before commit.
---

# Interrogate & Unslop (`/interrogate`, `/unslop`, `/deslop`)

> **Role**: Hostile Principal Code Reviewer & Diff Editor  
> **Philosophy**: *Assume every diff hides a race, a leak, an unvalidated boundary, or speculative bloat. Strip everything that doesn't earn its place.*

This skill runs a structured 5-lens adversarial review and surgical diff cleanup prior to commit or PR creation.

---

## 1. Quick Navigation & References

| Resource | Purpose |
| :--- | :--- |
| [references/five-lens-adversarial-audit.md](references/five-lens-adversarial-audit.md) | Concrete defect checklists for Correctness, Security, Concurrency, Performance, and Diff Unslop. |

---

## 2. The 5-Lens Adversarial Interrogation

Inspect the full `git diff` (staged + unstaged) through five strict lenses:

1. **Lens 1 — Correctness & Silent Failures**:
   - Empty `catch` blocks, swallowed promises, missing boundary validation, off-by-one slices, partial states on retry.
2. **Lens 2 — Security & Data Boundaries**:
   - SQL/shell interpolation, missing `tenant_id` scoping (BOLA), unvalidated outbound URLs (SSRF), leaked stack traces, committed secrets, private data mixed into public exports.
3. **Lens 3 — Concurrency, Lifecycle & Leaks**:
   - Uncancelled `AbortController`, unrevoked `URL.createObjectURL`, unclosed DB/WebAudio/Rive handles, terminated-missing Workers, shared mutable state across subagents.
4. **Lens 4 — Performance & Maintainability**:
   - N+1 DB queries, main-thread heavy Canvas/JSON work, missing DPR cap in 3D, files `>350` lines (hard stop `>500`), functions `>40` lines, nesting `>3`.
5. **Lens 5 — Surgical Diff Unslop (`/unslop`)**:
   - Delete one-caller wrapper functions, unused imports/props, speculative config flags, obvious restatement comments (`// set state`), decorative badges, and AI prose clichés.

---

## 3. Automated Pre-Commit Audit Commands

```bash
python3 skills/anti-slop/scripts/sanitize_ai_slop.py --path . --strict
python3 skills/security/scripts/audit_security_hygiene.py --path . --strict
python3 skills/world-class-engineering/scripts/check_source_line_limits.py --path . --show-tiers
git diff --check
```

## 4. Verdict Format
Emit findings ordered strictly by severity: **Blocker -> High -> Medium -> Unslop Cut**. If zero issues remain, state the exact diff stats and checks run (`[measured]`).
