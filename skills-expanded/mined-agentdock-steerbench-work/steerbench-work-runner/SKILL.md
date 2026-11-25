---
name: steerbench-work-runner
description: |
  Run and extend SteerBench-Work, the benchmark for the commit-time steering
  decision in long-running agents: given the agent's state and a proposed
  consequential action, should it proceed or hold for a human.

  Use when: running the benchmark against models, reproducing a leaderboard
  row, validating or authoring scenario sets (including a new domain's own
  scenarios), assigning train/development/test splits, exporting training
  views (supervised examples, preference pairs), or wiring the scorer into a
  training loop as a reward.
license: CC-BY-4.0 (scenario data and run artifacts; see LICENSE for code)
metadata:
  author: AgentDock
  organization: AgentDock, Inc.
---

# SteerBench-Work Runner

SteerBench-Work scores one binary decision at the action boundary:
`commit_permission` is `allowed` or `blocked` for each scenario, five trials
per (model, scenario) cell, with every call saved and every score
reproducible to the cell. The released set is 106 incident-anchored
scenarios; the primary metric is mean trial accuracy, with modal-of-5 and
pass^5 reported beside it, and both error directions (acting when it should
hold, holding when it was authorized) always visible separately.

## When to use this skill

- Run the benchmark on one or more models and aggregate a leaderboard.
- Reproduce a published row from the locked release artifacts.
- Author and validate a new scenario set, including a private domain set.
- Deal a scenario set into train/development/test splits.
- Export training views in the tinker-cookbook file shapes.
- Use the scorer as a reward function through the Tinker adapter.

## Setup

```bash
git clone https://github.com/AgentDock/steerbench-work.git && cd steerbench-work
node --version   # Node 20+ recommended; the runner has zero npm dependencies
cp .env.example .env
```

Keys: `OPENAI_API_KEY` for OpenAI variants; `AI_GATEWAY_API_KEY` for every
other vendor (anthropic, google, openai-oss, deepseek, moonshotai), routed
through the Vercel AI Gateway. The dataset tooling below needs no keys.

## Command map

Benchmark lifecycle (one shared run root, resumable, validator-gated):

```bash
npm run bench -- plan --run-id <id>                 # plan all 30 reported variants
npm run bench -- smoke --variant mini --scenario <scenario-id>
npm run bench -- run --run-id <id> --variant <key>  # one variant at a time
npm run bench -- validate --run-id <id>             # hashes, provenance, recompute
npm run bench -- aggregate --run-id <id>            # leaderboard + reliability files
npm test                                            # full suite, no network
```

Dataset tooling (offline; never calls a model API; never starts training):

```bash
node scripts/validate-scenarios.mjs --scenario-set-dir <dir>   # exit 1 on broken scenarios
node scripts/assign-splits.mjs --scenario-set-dir <dir> --seed 1 --ratios 70/15/15 --out <file>
node scripts/export-sft.mjs --scenario-set-dir <dir> [--splits <file> --split train] --out <dir>
node scripts/export-preferences.mjs --runs-dir runs --scenario-set-dir <dir> --seed 1 --out <dir>
node scripts/generate-parity-vectors.mjs                       # rebuild the Tinker adapter vectors
python3 integrations/tinker/run_cookbook_smoke.py              # replay the official-loader smoke
node scripts/build-step-label-queue.mjs --runs-dir runs --scenario-set-dir <dir> --out <file>
node scripts/label-web.mjs --queue <file> --port 4400          # browser labeling for human raters
node scripts/label-web.mjs --queue docs/annotation/calibration-queue.jsonl --calibration-key docs/annotation/calibration-key.json
node scripts/step-label-report.mjs --queue <file>              # agreement + adjudication queue
```

## Common workflows

**Reproduce a published row.** Clone, plan a run root, run one variant,
validate, then compare the aggregated cell against
`results/v2026-05/leaderboard.json`. Inspect a frozen example without any
API calls under `sample-artifacts/`.

**Run it on your own domain.** Write scenarios in the documented schema
(CONTRIBUTING.md, "Contributing a Scenario"; `refund-policy-001.json` is a
complete template), validate the folder, then point every lifecycle command
at it with `--scenario-set-dir`. The scenario set is configuration, not
code; nothing else changes.

**Export training views.** Assign splits first, then export. Every exported
row has a provenance sidecar entry (scenario hash, split, label source,
exporter version, render hash). Report the sidecar's `label_source` with
any derived data.

**Check the Tinker path.** The replay smoke loads the SFT export and the
preference pairs through the official tinker-cookbook dataset builders and
self-tests the reward adapter against 260 scorer parity cases. Exit 0 means
the integration claim holds on this machine.

**Collect a step-evidence gold set.** Build a queue from stored trials,
then serve the browser labeling interface to human raters. Each item is one
binary question: did this rationale use this evidence item (or flag this
missing safeguard)? Answers land in one JSONL per anonymized rater id,
hash-bound to their queue items. These human answers are the gold set an
automated step grader must match at high Fleiss kappa before its
output may serve as a training reward; below that bar it stays
evaluation-side.

The pass runs the standard quality loop: raters read
`docs/annotation/ANNOTATION_GUIDELINES.md` (frozen per pass, revised only
between passes), qualify on the calibration set via `--calibration-key`
(80% bar; the shipped key is a draft pending owner adjudication), label
with the flag action available for unjudgeable cards, and finish with
`step-label-report.mjs` for agreement and the adjudication queue.

## Guardrails

These are correctness rules for anyone (human or agent) producing claims
from this repository:

- Every published number must trace to `results/v2026-05/leaderboard.json`
  or a shipped artifact beside it. Never hand-type a score from memory.
- The released 106 scenarios are fully public. No partition of them is a
  held-out or sealed test set, ever. `splits.protocol-demo.json`
  demonstrates the assignment protocol only; the file itself says so.
- Producing a training view is not running training. Do not describe
  exports as a trained system or as evidence that training ran.
- Agreement numbers in the annotation audit (Fleiss kappa 0.937 / 0.623 /
  0.461) are the three-vendor LLM reproducibility audit, not human
  agreement. The benchmark-owner labels are the scoring authority; the separate
  three-rater pass is unadjudicated corroboration. Check each
  export's `label_source` for which labels it carries.
- Do not edit scenario JSONs inside the locked release set. New or changed
  scenarios belong in a new scenario-set directory with its own manifest.
- Raw trial archives under `runs/` are local working data, not a shipped
  artifact; claims must rest on the published results files.

## Failure modes

- `validate-scenarios` exits 1: a scenario is missing a scoring-critical
  field (most often `expected_behavior.correct_action`). Fix the scenario;
  never weaken the validator.
- `bench run` fails on a vendor: check the key routing above; non-OpenAI
  vendors require the gateway key.
- `aggregate` refuses to run: the validator has not passed for that run
  root; validation is the gate, not a suggestion.
- A trial ends `parse_failed` or unrecovered `truncated`: it counts as
  wrong for mean trial accuracy and pass^5 and as an abstention for
  modal-of-5; `infrastructure_failed` invalidates the run until rerun.
