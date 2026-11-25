---
name: aratest
description: |
  Check the claims of an Agent-Native Research Artifact (ARA) with aratest.
  Runs `aratest test` on the properties the ARA declares, and, only when the
  user asks for fresh experiments and agrees to a budget, runs
  `aratest continuous` to have an experiment agent generate new cases for the
  claims that bind experiment families. Replays every saved violation with
  `aratest replay`. Never writes or edits the ARA.

  TRIGGERS: test the claims, check this ARA, run aratest, aratest test,
  continuous testing, run experiments against the claims, replay a finding,
  aratest replay, what violated
---

# aratest: check an ARA's declared claims

Use this skill with an ARA directory path. `aratest` checks **declared
properties**: the relations `aratest/spec.yaml` attaches to the claims in
`logic/claims.md`. It does not judge whether research is right. A violation
means a declared property failed on the cases checked; it is not a
refutation of the research claim.

## 1. Check that the ARA declares something

Look for `<ara>/aratest/spec.yaml`.

- If it is missing, stop. Tell the user that declarations are written by the
  `research-manager` skill or by the offline annotation agent, and that this
  skill does not write them.
- Never create, write, or edit `spec.yaml`, or any other file in the ARA.

## 2. Check the reported numbers

Run:

```bash
aratest test <ara>
```

Summarize for the user:

- each violated property, with its claim and the witnesses `aratest` names;
- each `NoVerdict`, with its reason (for example `missing_evidence`,
  `pending`, `unclassified`, `incomplete_coverage`);
- the claims the spec does not declare (`aratest` lists them as undeclared).

Exit codes: 0 every checked property holds, 1 a property is violated, 2 a
usage or input error, 3 an internal, record, or plugin error, 4 nothing is
violated but something is undecided, 5 nothing was checked. Violated claims
are saved as records under `.aratest/records/`.

## 3. Fresh experiments (only when the user asks)

Only continue here when the user asks for fresh experiments, and only for
claims whose spec entry lists `families`. `aratest continuous` comes from the
`dissclaimer` package; if `aratest continuous --help` says it is not
installed, tell the user to install `dissclaimer`.

Running experiments spends money. Before starting:

1. Propose a per-run budget (`--run-usd`) and a total budget
   (`--budget-usd`), or a run count (`--max-runs`), and say which claims and
   families would run.
2. Wait for the user to confirm the amounts. Do not start without an explicit
   confirmation.
3. Provider keys come from the environment only. Never put a key in a
   configuration file, a command line, or your answer.

Then run, in the foreground or under `tmux`/`nohup` as the user prefers:

```bash
aratest continuous start <ara> --agent <agent> --agent-config <config.yaml> \
  --run-usd <confirmed per-run amount> --budget-usd <confirmed total>
```

- `aratest continuous status <ara>` reports budget used and reserved, runs by
  status, retired bindings, and finding counts.
- `aratest continuous stop <ara>` lets running experiments finish and stops;
  `stop --now` also cancels them.
- If `start` stops with `cleanup_unresolved`, a container may still be
  running and spending. Tell the user to check Docker, and only after they
  confirm it is gone, resume with `--confirm-cleanup <run id>`.

## 4. Explain each finding

Run `aratest continuous findings <ara>`. For each finding:

1. Run the `aratest replay <record>` command it prints and report whether the
   recomputed outcome matches the recorded one.
2. Summarize which property failed and on which cases (the witnesses).
3. Point the user to the run's supporting files (`report.json.support/`) to
   inspect how the experiment ran.
4. Say plainly that a violation is a failed declared property on the
   generated cases, not a refutation of the research claim.

## 5. Never modify the ARA

Do not write into the ARA directory at any step. Records and service state
live outside it, under `.aratest/`.
