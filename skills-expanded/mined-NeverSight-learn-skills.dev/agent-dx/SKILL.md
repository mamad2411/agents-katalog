---
name: agent-dx
description: "Use for AGENT DX — the surface an AI agent consumes as a developer. DO — keep SDK/tool/structured-output/error/telemetry changes agent-consumable. REVIEW — audit agent-facing surfaces for stable contracts, recovery, trust-boundary safety. DESIGN — shape new agent-facing surfaces. Triggers: 'design our Agent SDK', 'are our tool schemas agent-safe', 'review MCP surface', 'is telemetry leaking PII'. Do NOT use for human developer surfaces (use dx-audit / dx-design), agent-readable docs (use agent-docs), or repo agent-hardening (use harden-repo-for-coding-agents)."
license: MIT
---

# Agent DX

The developer experience of a surface where an **AI agent is the developer** — an SDK, tool,
structured output, error envelope, or telemetry an agent consumes to build with or act
through. Provenance lives in `skill.json`; this file is runtime routing only.

**Produces:** a `change-plan.md` (DO), an `audit-report.md` plus a findings-ledger +
workflow-state when tracked (REVIEW), or a `design-doc.md` / `refactor-runbook.md` /
`explanation.md` (DESIGN).

## Core principle

**An agent consumes the surface alone, at machine speed, with no tooltip to fall back on.** So
the bar for any SDK, tool, error, or span is whether a stochastic consumer can parse it,
recover from it, and not be harmed by it: typed contracts over prose; recovery designed in,
not hoped for; the trust boundary closed by default. It sits *atop* the HTTP-client floor that
`dx-audit` / `dx-design` own, never replacing it.

## Activation

- **Bare invocation** (`"use agent-dx"`, `"start"`): show a compact menu: mode choice (guided / autopilot / grill me?) and numbered intents from the router. Wait. No file inspection, no network calls, no writes.
- **Concrete invocation** with intent and surface inferable: skip to step 3.
- **Ambiguous invocation**: ask one — e.g., *"Are you auditing an SDK, tool schema, structured-output envelope, or telemetry surface?"* or *"Is this a contract/recovery review or a trust-boundary audit?"*

## Workflow

1. **Pick intent.** Load `references/intent-router.csv`; match to `do`, `review`, or `design`.
   Ambiguous → ask once.
2. **Pick surface.** Load `references/intents/<intent>.csv`; match one or more of `sdk-design`,
   `tools-and-mcp`, `structured-output`, `errors-and-retry`, `sdk-telemetry` — or `all` for a
   REVIEW fan-out. Ambiguous → ask once with the menu.
3. **Load grounded context.** Load only the chosen row's `playbook` plus its `core_refs`. Do
   not load other playbooks (the `review`/`all` row carries none — each surface agent loads its
   own; see step 6).
4. **Identify the target persona** from `references/core/personas.md`.
5. **Then calibrate to project scale** (REVIEW / DESIGN) per `references/calibration.md`: below
   Load-bearing, narrow scope, collapse same-mechanism gaps into one systemic finding, and
   split **Now** vs **Later (as it grows)**. The tier feeds emission, never severity.
6. **Dispatch lenses in parallel** (REVIEW default when permitted): one surface per agent for
   `all`; otherwise the three lenses below. Sequential fallback if no delegation primitive.
7. **Apply the playbook.** Use the heuristics tagged for the intent. For REVIEW, score each
   surface 0–10 (`references/core/score-rubric.md`); synthesize lens findings, preserving
   disagreements as open questions. Apply severity and stable `AGENT-DX-<surface>-NNN` IDs
   (`references/core/severity-rubric.md`): `AGENT-DX-SDK`, `AGENT-DX-TOOL`, `AGENT-DX-OUT`,
   `AGENT-DX-ERR`, `AGENT-DX-TEL`.
8. **Emit.** DO → `templates/change-plan.md`. REVIEW → `templates/audit-report.md`. DESIGN →
   `templates/design-doc.md` (shape), `templates/refactor-runbook.md` (sequence a hardening),
   or `templates/explanation.md` (explain a principle).
9. **Create, resume, or close tracking state** (REVIEW). For an audit with 7+ findings, any
   severity 3–4, or a save/track/closeout request, load `references/trackable-findings.md`. If
   the request names an existing ledger, workflow-state, PR, or `AGENT-DX-*` ID, read
   saved state first; update statuses only after each verification rule passes. Otherwise write the
   ledger at `docs/audits/agent-dx-findings-ledger-<YYYY-MM-DD>-<scope-slug>.md` and workflow
   state at `docs/audits/agent-dx-workflow-state-<YYYY-MM-DD>-<scope-slug>.json` (fall back to
   `audit-artifacts/agent-dx-...` if `docs/audits/` is unwritable). Report both paths; keep
   roadmaps, issues, and non-tracking edits opt-in.

> **Wrong direction?** If the user says this isn't what they meant, go back to step 1 (Pick intent) — do not patch in the wrong direction. Restate the corrected understanding and re-plan.

## Modes

Guided Draft (default), Autopilot, Grill Me — see `references/modes.md`. Offer at bare
invocation; default to Guided Draft on concrete invocations.

## Output requirements

Every output names the intent, surface(s), persona, playbook(s) applied, and grounding sources
from `skill.json`; REVIEW adds severity + verification per finding and the project tier.
**Name the agent-consumability guarantees you are deliberately NOT adding (YAGNI), not only
the ones you are.**

## Subagent dispatch

Default for REVIEW when delegation is permitted; skip tiny or secret-bound work. Spawn three
lenses in parallel — **contract-and-schema** (typed schemas from code, stable error envelope,
validated output), **agent-recovery** (stop+verify, retry-shaped errors, semantic retry,
bounded loop), **trust-and-isolation** (tool-metadata injection, guardrail checkpoints,
credential walls, content redaction) — per `references/subagent-dispatch.md`, then synthesize,
ordering by severity.

## Reference map

- `references/intent-router.csv` + `references/intents/<intent>.csv` — the two routing layers.
- `references/playbooks/<surface>.md` — sdk-design, tools-and-mcp, structured-output,
  errors-and-retry, sdk-telemetry.
- `references/subagent-dispatch.md` — three-lens prompts and synthesis.
- `references/core/*.md` — severity, score, personas, glossary.
- `references/{calibration,trackable-findings,modes}.md` — shared (symlinks).
- `templates/*.md` — change-plan, audit-report, design-doc, refactor-runbook, explanation, plus
  the shared tracking artifacts.
- `evals/`, `skill.json` — gates and provenance.
