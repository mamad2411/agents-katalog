---
name: code-archaeology
description: Subsystem comprehension and historical intent analysis (/how and /why) before editing code. Maps runtime execution, ownership boundaries, load-bearing quirks, and blast radius.
---

# Code Archaeology (`/code-archaeology`, `/how`, `/why`)

> **Role**: Staff Systems Archaeologist  
> **Philosophy**: *Never modify code you cannot trace end-to-end. Separate intentional load-bearing invariants from accidental debt before writing a single line.*

This skill implements the `/how` and `/why` comprehension workflows before editing unfamiliar modules, preventing speculative rewrites and subtle regression cascades.

---

## 1. Quick Navigation & References

| Resource | Purpose |
| :--- | :--- |
| [references/how-and-why-protocol.md](references/how-and-why-protocol.md) | Step-by-step execution trace (`/how`), git/ADR intent mining (`/why`), and blast-radius checklist. |

---

## 2. The Two-Pass Archaeology Protocol

### Pass 1: `/how` (Runtime Flow & Ownership)
1. **Locate Entrypoints**: Find routes, CLI commands, event handlers, or UI triggers.
2. **Trace the Call Chain**: Follow `Entrypoint -> Boundary Validation -> Domain Service -> Repository/Store -> External Side Effects`.
3. **Map State Ownership**: Identify where state lives, who mutates it, and whether concurrent actors share keys, files, or caches.
4. **Identify Blast Radius**: Search all callers (`rg`) and existing test suites exercising this boundary.

### Pass 2: `/why` (Intent & Load-Bearing Quirks)
1. **Inspect History**: Run `git log -n 10 --oneline -- <file>` and `git log -S "<symbol>" -p` on strange conditionals or workarounds.
2. **Classify Constraints**:
   - **Load-Bearing Invariant**: Required by upstream APIs, browser quirks, race mitigation, or legal/data boundaries — **preserve**.
   - **Accidental Debt**: Dead flags, one-caller wrappers, or obsolete shims — **candidate for subtraction**.

---

## 3. Mandatory Subsystem Brief Format

Before proposing edits to an unfamiliar subsystem, emit a concise brief:
1. **Entrypoint & Data Flow**: Exact file paths and symbol chain (`[measured]` from files read).
2. **State & Side Effects**: Persisted stores, caches, network calls, or cleanup hooks.
3. **Load-Bearing Invariants**: Quirks or constraints that must not break.
4. **Blast Radius & Existing Tests**: Callers and test commands covering the path.
