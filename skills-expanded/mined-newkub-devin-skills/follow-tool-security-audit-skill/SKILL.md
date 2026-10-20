---
name: follow-tool-security-audit-skill
description: Cloudflare security-audit skill — multi-phase agent security audits with verified findings.json
argument-hint: "[target-path-or-scope]"
related:
  - follow-tool-deepsec
  - deep-review-codebase
  - analyze-attack-surface
  - check-secrets
  - follow-my-techstack
---

## Goal

Run structured, evidence-verified security audits with Cloudflare's `security-audit` coding-agent skill (MIT, `cloudflare/security-audit-skill`) — six phases (recon → coverage-led hunting → adversarial validation → structured output → independent record verification → reporting), producing machine-readable `findings.json` with `confirmed` / `needs_validation` / `rejected` verdicts

## Scope

Use for on-demand full-codebase or focused security review executed by the coding agent — the single-repo starting point of Cloudflare's vulnerability harness

- CI-style recurring scan pipeline → `/follow-tool-deepsec` instead; general code review with a security slice → `/deep-review-codebase`
- Full audit mode for explicit audits/pen-test requests; guidance mode for security questions unless report artifacts are asked for
- Requires: agent with tool use + parallel sub-agents, Node.js (validators), and an OS-enforced sandbox for anything the target controls

## Execute

### 1. Install

> Goal: get the skill into the agent store

1. `npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit` (add `--global` for user-level)
2. For Devin: keep it available per `/follow-devin-global-skills`; verify the validators run: `node validate-findings.cjs` / `node validate-coverage-ledger.cjs` exist in the skill dir

### 2. Recon (Phase 1)

> Goal: map the target deterministically before hunting

1. Point the audit at a repo/dir; the skill writes `architecture.md` (trust boundaries, input surfaces, prior evidence) and `coverage-ledger.json` (deterministic coverage units)
2. Run `validate-coverage-ledger.cjs` after ledger creation and every later update — invalid ledger = stop, fix scope first
3. Attack classes load per target: native/memory, web protocol/auth, client-side, supply-chain/release, cloud/deploy, RPC/messaging, resource-exhaustion, data-isolation, AI/LLM

### 3. Hunt And Validate (Phases 2–3)

> Goal: gap-free coverage, adversarial proof

1. Isolated hunters are assigned from ledger units; coverage critics find gaps — multiple runs are additive (a single run finds ~half of what repeats find)
2. Every unique candidate goes to a fresh verifier that tries to disprove it — finder never validates its own finding
3. Only boundary failures with a complete source trace + bounded observed result become `confirmed`; unresolved exact fact → `needs_validation` (no severity); disproved → `rejected`

### 4. Output And Report (Phases 4–6)

> Goal: verified records, target-neutral prose

1. Records go to `findings.json` validated against `report-schema.json` (`validate-findings.cjs` in Phase 4 and after every Phase 5 replacement)
2. Fresh agents verify final source claims; material replacements get another independent pass
3. `REPORT.md`, `FINDINGS-DETAIL.md`, `NEEDS-VALIDATION.md` derive only from verified records + ledger
4. Output dir defaults outside the repo (`~/security-audit-skill/<repo>/run-<N>`); write inside the target only when the chosen dir is git-ignored — severity = likelihood × impact, checklist deviations are hardening notes, not vulns

## Rules

### 1. Sandbox Or Stay Unconfirmed

- Executing target-controlled builds/tests/fuzzers without an OS-enforced sandbox (no egress, sanitized env, resource limits, scratch-only writes) is forbidden — keep such leads as `needs_validation` with the exact blocking fact

### 2. Verdicts Are Distinct, Never Blend

- No severity on `needs_validation`; no "probably fine" on `rejected` — the schema is the contract, validators must pass before delivery

### 3. Boundaries With Other Skills

- Recurring/CI scans → `/follow-tool-deepsec`; defense-in-depth absence where another layer prevents the attack → hardening note in the report, not a finding
- Persist confirmed outcomes via `/update-devin-project-rules` / `/update-astgrep-rules` so the next audit builds on them

## Expected Outcome

- `findings.json` + reports with independently verified, schema-valid records
- Coverage ledger proving what was examined — repeat runs target gaps instead of re-scanning everything
- No unsafe target execution and no severity attached to unverified claims
