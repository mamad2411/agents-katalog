# AGENTS.md — Prism-Eval

Every Cursor / coding agent in this repo must follow these locks. Do not invent process from memory.

## Dual-agent mode

| Window | Role |
|--------|------|
| `C:\code\QA` | Senior QA / Architect — reviews, bugs, handoffs, verify. Does **not** close work from Dev’s word alone. |
| This repo (`C:\code\prism_eval`) | Dev / docs / infra / test — implement **only** from `handoffs/handoffQa*.md` (mirrors under `C:\code\QA\projects\prism_eval\handoffs/`). |

Protocol: `C:\code\QA\projects\prism_eval\AGENT-PROTOCOL.md`

### Status

- Dev may set handoff Status to `In Progress`, `Ready for QA`, or `Blocked`.
- **Only QA** sets `Closed`.
- When done: write `handoffs/handoffbackQaNNN-*.md` **and** `C:\code\QA\projects\prism_eval\handoffs-back/HB-*.md`.

## Product lock

1. **Prism-Eval = pre-deploy eval gate** (G4 adversarial corpora, CI exit codes, audit receipts).  
2. **Not** runtime enforcement — that is Prism-Shield / PrismManifest ParameterManifest gate.  
3. **Never** ship a top-level Python package named `prismmanifest` from this repo. That name belongs to the gate product. Owning it breaks `pip install prism-eval` + `prismmanifest` / `prism-shield` coexistence (QA BUG-001 / HO-001).  
4. Preferred public import: `from prism_eval import …`. CLI entry must not require colliding namespaces.  
5. Do not claim “enterprise ready” / Shield companion until coexistence CI (HO-007) is green.

## Active launch queue (2026-08-12)

| Pri | Handoff | Do this |
|-----|---------|---------|
| P0 | `handoffs/handoffQa001-namespace-collision.md` | Relocate internals; stop colliding with `prismmanifest` |
| P0 | `handoffs/handoffQa007-coexistence-ci.md` | CI: install with `prismmanifest`, assert import + CLI |
| P1 | `handoffs/handoffQa002-cli-exit.md` | Default exit code tracks `suite_passed` |

## Standing rules

- Read real source; do not fake fixes or skip acceptance criteria.
- Commit / push only when the user asks.
- Keep fail-closed defaults: empty / identity agent must fail builtin under default thresholds.
- Corpus JSON is untrusted input — no code execution from corpus files.
- SemVer: namespace relocation is **Breaking** for `prismmanifest.prism_eval` imports — CHANGELOG must say so.
