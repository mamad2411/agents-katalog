---
description: Reconcile docs/specs (REQUIREMENTS.md REQ-* IDs) against the codebase and report drift. Read-only — never edits code.
---

# /spec-reconcile

Reconcile the spec-driven requirements against the actual implementation and produce a
**drift report**. This command is **read-only**: it inspects and reports; it must not
modify code, specs, or tests.

## Inputs

- `docs/specs/REQUIREMENTS.md` — the authoritative list of `REQ-*` IDs, each with a
  one-line requirement and a `→ file` implementation pointer. Prefixes: `SD` sidecar,
  `RM` register map/decode, `HA` MQTT/Home Assistant, `SC` scheduling, `CF` config,
  `LC` lifecycle/health, `TS` testing, `DP` deployment.
- The other `docs/specs/*.md` for detail behind each requirement, and
  `docs/phase0/findings.md` for the confirmed register facts behind every `RM-*`.
- The Go source tree (`cmd/`, `internal/`), the Python `sidecar/`, `features/`,
  the Dockerfiles, `go.mod`, `.claude/`.

## Procedure

1. **Parse requirements.** Extract every `REQ-*` ID, its text, and its `→` target(s)
   from `REQUIREMENTS.md`.
2. **Locate implementations.** For each requirement, check the pointed-to file exists
   and contains code plausibly satisfying it (function/type/const, endpoint path, env
   var, topic, register address — grep for the concrete tokens named in the
   requirement). Note whether a corresponding test exists.
3. **Scan for untraceable code.** Walk the source tree for significant units
   (exported types/functions, HTTP handlers, endpoints, env-var reads, MQTT topics,
   register constants) and check each maps to at least one `REQ-*`. Flag anything with
   no traceable requirement.
4. **Detect mismatches.** Where a requirement names a specific constant, path, default,
   scale, or behaviour, verify the code matches (e.g. sidecar HTTP on `:8081`; amps
   encoding `round(amps,1)*10` / decode `÷10`; work-mode `35`/`33` toggling bit 1;
   grid power decoded as one S32 not two U16s; the read-before-write guard skips a write
   when the value already matches). Flag divergences, cross-checking `RM-*` against
   `docs/phase0/findings.md`.

## Output — reconciliation report

Print a Markdown report with these sections (omit empty ones):

- **Summary** — counts: total requirements, implemented, missing, partial; untraceable
  code units; mismatches.
- **Missing** — `REQ-*` with no plausible implementation. Include the pointer and what
  was searched for.
- **Partial / untested** — implemented but no test, or only partially satisfied.
- **Untraceable code** — code units with no `REQ-*`; suggest either a new requirement
  or that the code is dead/out-of-scope.
- **Mismatches** — requirement says X, code does Y (with `file:line`).
- **Verified** — a compact checklist of `REQ-*` confirmed implemented (+ test).

## Rules

- Do **not** edit code, specs, tests, or config. Reporting only.
- Cite `file:line` for every finding so items are actionable.
- Prefer concrete grep evidence over assumptions; if uncertain, mark **partial** and say
  what to check manually rather than guessing.
- A register fact is only "correct" if it traces to `docs/phase0/findings.md`; trust no
  unconfirmed register.
- If `REQUIREMENTS.md` and code disagree on an intentional design change, recommend
  updating the spec — but leave the change to the human.
