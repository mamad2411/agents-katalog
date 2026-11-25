---
name: blueprint-adopt-survey
description: "Measure what chaff reports on the named documents today, as the kind the person chose, and propose the setup — changing nothing yet."
---

# Measure what is there today

`.blueprint/answers.json` names the places chaff will watch (`places`, a folder or a file a line), what kind of
documents they are (`kind`) and whether a GitHub workflow is wanted (`ci`). The person may not be an engineer: say
what you do in plain words.

Change nothing in the repository: this step only measures. The person approves the setup before anything is
written.

## Measure

The kind maps to a genre in `<usecase pack>/kinds.json`. For each place, run
`sh <base pack>/checks/chaff.sh <place> --genre <genre> --compact` and count the warnings and errors, by rule. Read a
few of them: a rule that reports mostly what the documents do on purpose may be worth turning down in `chaff.yaml`
rather than shelving — say which, and why, for the person to decide at the gate.

## Write `.blueprint/adopt.json`

```json
{ "genre": "docs/manual", "findings": 2, "proposal": "chaff.yaml に genre と language を書き、今の 2 件を棚に上げる。" }
```

`findings` is the number of warnings and errors chaff reports on all the places together, as that genre, now; the
check measures it again. If the folder already has a `chaff.yaml` or a `.chaff-baseline.json`, say so in
`proposal`: the next step keeps what they hold.

## Done when

`node <usecase pack>/checks/adopt.mjs survey` (with `BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set to the pack folders
from your prompt) passes. It writes `.blueprint/adopt.txt`, what the person reads before anything changes.
