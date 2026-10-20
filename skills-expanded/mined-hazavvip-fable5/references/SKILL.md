---
name: fable-5-recon
description: >-
  Recon v4 agent-first: archaeology → engine → pre-triage → surface_probe →
  verify_signal → agent triage. PRIMARY only from verified_signals.json.
version: 4.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Agent, WebSearch, WebFetch]
---

# Reconnaissance v4 — READ ORDER

0. **`Workflow/pre-engagement/TARGET_INTAKE.md`** — Step 0 gate (any target)
1. **`Workflow/reconnaissance/RECON_V3.md`** (canonical)
2. **`references/agent-triage-deep.md`**
3. **`references/cred-gather-greybox.md`** — default greybox (Hephaestus pattern)
4. **`references/cred-gather-on-login.md`** — supplemental single-host gather

**FORBIDDEN:** manual subfinder/crt.sh/httpx enum; bulk `quick_scan` as truth; PRIMARY from unverified candidates.

---

## Step 0 — Target intake (before engine)

```bash
python3 tools/pre-engagement/target_intake.py {target}
```

Read `evidence/TRANSCRIPT_BRIEF.md` + `dead_ends.json` — **never raw JSONL**.

See `Workflow/pre-engagement/TARGET_INTAKE.md`.

---

## Automation (after intake)

```bash
python3 tools/reconnaissance/recon_pipeline.py \
  --target {domain} --campaign campaigns/{domain} --stage all
```

Stages: `engine` → `pre-triage` → `greybox-cred` → `surface` (tier 1) → `verify`

Greybox runs automatically when `greybox_cred_gather: true` in `fable/FEATURE_FLAGS.json`.

**Do NOT** spawn subagent only to run `quick_scan_wrapper.py`. Use pipeline stages or parallel agent tracks (archaeology ‖ pre-triage analysis).

---

## Agent triage (mandatory)

Read:
- `verified_signals.json` — **only source for PRIMARY**
- `recon_engine.json`, `pre_triage.json`

Write: `triage_decision.json`, `fingerprint.json`

Reject: `surface_candidates.json` / legacy `quick_scan.json` for PRIMARY promotion.

---

## Cred gather — dual mode

**Greybox (default, pipeline):** LR broad + NX — see `references/cred-gather-greybox.md`

```bash
python3 tools/reconnaissance/recon_pipeline.py \
  --target {domain} --campaign campaigns/{domain} \
  --stage greybox-cred
```

**Login-host (supplemental):** when agent confirms NEW login surface

```bash
python3 tools/reconnaissance/recon_pipeline.py \
  --target {domain} --campaign campaigns/{domain} \
  --stage cred-gather --login-host {exact_subdomain}
```

---

## Close recon

`reconnaissance/state.json` → `completed`, `recon_version: "4.0"`
