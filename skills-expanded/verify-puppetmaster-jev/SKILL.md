---
name: verify-puppetmaster-jev
description: >-
  Prove the Puppetmaster Jev transition oracle: unset never networks,
  opt-in may skip the conflict-auditor, V2–V4 stay observe unless ACT.
disable-model-invocation: true
---

# Verify Puppetmaster Jev

Library plus CLI. Isolated temp store. Never use the user's live
`.puppetmaster/` state. Never print an OpenRouter key.

## Launch

Ready: `python -m unittest tests.test_jev_transition -q` exits 0 from
the Jev worktree (`Puppetmaster-jev-oracle` or the product checkout
that contains `puppetmaster/jev/`).

```bash
cd "$REPO"
.venv/bin/python -m unittest tests.test_jev_transition -q
```

Use the repo venv if present; otherwise `python3` on PATH. Teardown is
the process exit. Helpers write under `/tmp/verify-this/puppetmaster-jev/`
and must not delete prior receipts.

## Doctor

```bash
.cursor/skills/verify-puppetmaster-jev/scripts/doctor.py
```

Must report:

- `opted_in=false` and `acting=false` in a cleared env
- `test_jev_transition` importable
- no `PUPPETMASTER_JEV` / `PUPPETMASTER_JEV_ACT` leak from the host
  after `hermetic_env` import

If doctor fails, fix the tree. Do not drive live Decisions.

## Drive

Prefer the helper, then unittest, then an optional live observe.

```bash
.cursor/skills/verify-puppetmaster-jev/scripts/prove_observe.py
```

Mapped features: [features/README.md](features/README.md).

## Evidence

A pass is:

1. Helper JSON at `/tmp/verify-this/puppetmaster-jev/observe.json`
2. `v1_acts_on_opt_in=true` (auditor skipped without `JEV_ACT`)
3. `v234_match_today=true` (launch / admit / enqueue unchanged)
4. Unittest exit 0
5. `show` / stitcher preview contains `## Jev` only when a
   `jev_transition` GATE exists

Live Decisions are optional and only when the user named a key source.
Load the key in-process. Never write it to evidence.

## Cleanup

Kill only the helper/unittest PIDs this run started. Leave
`/tmp/verify-this/puppetmaster-jev/` in place.

## Helpers

- `.cursor/skills/verify-puppetmaster-jev/scripts/doctor.py`
- `.cursor/skills/verify-puppetmaster-jev/scripts/prove_observe.py`
