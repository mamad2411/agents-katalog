---
name: rh-sync
description: >-
  Sync the consolidated RH workspace rh/ after each RH round: INVENTORY row,
  run_rh.py probe list, README status table, and on [E] promotion the RH paper
  and Lean layer. Use when an RH round finished, a PRIME contract or PRIME.*
  ledger row changes, the rh folder needs updating, or a Lean proof RH task
  comes up.
---

# RH sync

After every RH round, `rh/` must reflect it. `rh/` **references** artefacts (path + SHA-256), it never duplicates them. Probes keep living in `experiments/tfpt-discovery/`; the firewall is unchanged.

## Procedure (follow in order)

### 1. Probe sealed?

Before syncing, confirm the round's probe is frozen: `SPEC_SHA` recorded, all gates pass, deterministic (two runs → identical output). Not sealed ⇒ no sync.

### 2. Append INVENTORY row

```bash
shasum -a 256 experiments/tfpt-discovery/<probe>.py
```

Add row to `rh/INVENTORY.json`: path, SHA-256, round, verdict/status type (helper: `rh/verification/make_inventory.py`). Never edit existing rows silently.

### 3. Extend `run_rh.py` + run the suite

Add the probe to the sealed probe list (smoke) in `rh/verification/run_rh.py`, then:

```bash
python rh/verification/run_rh.py   # must end: RH SUITE: ALL CHECKS PASSED
```

The suite covers v9xx RH modules by path, the sealed probe list, the SHA drift detector, and optionally `lake build`. Red suite ⇒ fix before anything else.

### 4. Update README status table

`rh/README.md`: round, verdict, open-edge status. Keep the claim boundary line intact. Then write `rh/catalog/fragments/part_new_<round>.json` and run `python3 rh/catalog/build_catalog.py` (skill **`rh-corpus-search`**).

### 5. On [E] promotion (with `promote-to-verification`)

- Update `rh/paper/rh_program.tex` section 2 (certified results) / section 7 (roadmap); certification box: ledger ID + module + SPEC_SHA.
- Lean layer, three criteria:
  - **Exactly provable finite identity** → prove for real (RH/Recursion.lean style, no `sorry`)
  - **Matrix/inertia theorem** → statement in Inertia.lean (`sorry` with reference comment: round / ledger ID / probe)
  - **Open edge** → entry in Open.lean

### 6. On no-go

Extend the no-go catalog in `rh/paper/rh_program.tex` section 4 (what was excluded, by which probe, at which round).

### 7. Claim-boundary check

Every touched `rh/` artefact still states the boundary: **no RH claim** — conditional/finite results only.

## What NOT to do

- **No probe copies into `rh/`** — INVENTORY references by path + SHA-256.
- **No `next.txt` replacement** — `experiments/next.txt` stays the running research log (German OK); `rh/` is the consolidated view.
- No verification/ledger/paper (main docset) edits from here — that is `promote-to-verification` territory.
