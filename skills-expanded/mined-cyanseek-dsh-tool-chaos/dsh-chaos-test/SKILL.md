---
name: dsh-chaos-test
description: Design, install, run, and report deterministic DeepSeek Harness tool-failure experiments. Use when a user wants to prove retry or fallback behavior, timeout or cooperative cancellation, policy-denial handling, blocked-result recovery, Code Mode nested-call resilience, or CI evidence for a DSH agent/plugin. Complete the baseline → dry-run → real-injection flow with minimal questions and return PASS, FAIL, or INCONCLUSIVE evidence.
license: MIT
metadata:
  author: cyanseek
  version: "0.1.0-next.1"
---

# DSH Chaos Test

Turn a resilience requirement into a real, isolated experiment. Do not stop at a plan when the local environment permits execution.

Requires Node.js 22.19+ and a usable `dsh` CLI. The wrapper can install the published `dsh-tool-chaos` npm package when it is not already present.

## Recognize these requests

- “验证第一次工具失败后 Agent 会不会自动重试。”
- “Prove the fallback works when GitHub/web/database fails once.”
- “测试 timeout 是否真正取消了工作，不能留下孤儿进程。”
- “Verify a blocked tool result is not trusted.”
- “Test a nested Code Mode tool call.”
- “Generate reproducible DSH resilience evidence for CI.”

Do not use this skill for production infrastructure chaos, load testing, penetration testing, or generic security scanning.

## Default operating mode

Act autonomously. Resolve repository paths, project instructions, tool names, current Git state, local versions, and existing tests by inspection. Ask at most one concise question only when a fact is both undiscoverable and safety-critical.

Use these defaults unless repository evidence requires a narrower choice:

- current repository as the workspace;
- a disposable profile derived from the workspace path;
- one exact or narrowly globbed tool rule;
- `probability: 1`, `afterMatches: 0`, `every: 1`, `maxInjections: 1`;
- baseline first, then `dryRun: true`, then `dryRun: false` only after the dry-run proves the intended match;
- all artifacts under `.dsh-chaos/runs/<run-id>/`;
- no push, publish, credential change, permission escalation, production target, or out-of-workspace mutation.

Missing evidence is `INCONCLUSIVE`, never `PASS`.

## Use the bundled command wrapper

Set `<skill-root>` to this skill directory. Run:

```bash
node <skill-root>/scripts/dsh-chaos.mjs doctor --json
```

The wrapper prefers an already installed `dsh-tool-chaos` binary and otherwise uses `npx -y dsh-tool-chaos`.

## Workflow

### 1. Diagnose and choose the smallest experiment

Read applicable `AGENTS.md`/contribution rules, inspect the protected behavior and its tests, and run the doctor. Select one primary fault:

| User need | Action | Expected evidence |
|---|---|---|
| retry/fallback after transient failure | `error` | one injected error, autonomous retry/fallback, correct final result |
| bounded cancellation | `abort` | derived signal aborts, delegated work settles, no orphan remains |
| slow dependency tolerance | `delay` | declared time budget is enforced and behavior remains correct |
| approval/policy denial | `deny` | side effect does not run; agent chooses a safe route or explains the block |
| invalid/untrusted result | `block` | result is withheld and never used as trusted evidence |
| Code Mode sub-call resilience | any + `scope: nested` | outer program handles the inner failure without corrupting the turn |

Prefer `error` for the first public demonstration.

Read `references/scenario-design.md` only when the exact rule or oracle is unclear.

### 2. Install into an isolated profile

Run the idempotent setup command:

```bash
node <skill-root>/scripts/dsh-chaos.mjs setup --profile <isolated-profile> --json
```

Use `--source /trusted/local/path` or a trusted tarball during local development. Verify the effective composition:

```bash
dsh --profile <isolated-profile> --dump-config
```

Both `tool-chaos` and `tool-chaos-reporter` must be present. Stop as `INCONCLUSIVE` if composition cannot be verified.

### 3. Define a falsifiable oracle

Create `.dsh-chaos/runs/<run-id>/hypothesis.md` with:

- protected user need;
- steady state and baseline assertion;
- exact tool, call scope, action, and deterministic seed;
- expected retry/fallback/bounded failure;
- forbidden side effects;
- measurable pass/fail criteria;
- environment versions and assumptions.

Never use exit code alone as the oracle.

### 4. Create three complete DSH overlays

Generate a starter:

```bash
node <skill-root>/scripts/dsh-chaos.mjs init <run-dir>/dry-run.patch.yml --preset retry
```

Create:

- `baseline.patch.yml`: full `tool-chaos` config with `enabled: false`;
- `dry-run.patch.yml`: full config with `enabled: true`, `dryRun: true`;
- `experiment.patch.yml`: identical to dry-run except `dryRun: false`.

DSH row patches replace the complete `config`; do not write partial overrides. Keep the reporter row enabled in all three overlays. Never broaden to exact `tool: '*'` as a shortcut.

Read `references/safety-policy.md` before any rule that can touch external systems or non-workspace paths.

### 5. Execute baseline

```bash
node <skill-root>/scripts/dsh-chaos.mjs run \
  --mode baseline \
  --profile <isolated-profile> \
  --patch <run-dir>/baseline.patch.yml \
  --task "<same deterministic task>" \
  --expect "<stable output regex>" \
  --output <run-dir>/baseline \
  --no-install \
  --json
```

A failed baseline makes the final experiment `INCONCLUSIVE`.

### 6. Execute and validate dry-run

Run the identical task with `--mode dry-run` and `dry-run.patch.yml`. Require:

- at least one machine-readable `DSH_TOOL_CHAOS_EVENT` decision;
- `dryRun: true` and `injected: false`;
- the intended rule, tool, and root/nested scope only;
- unchanged successful behavior.

If the intended call is not observed, refine the exact tool name or `argumentsPattern` automatically, at most three attempts. Do not proceed to real injection until this passes.

### 7. Execute real injection

Run the identical task with `--mode experiment` and `experiment.patch.yml`. Do not manually help the tested agent. Its own retry, fallback, safe explanation, or bounded failure must satisfy the oracle.

### 8. Evaluate and report

Compare baseline, dry-run, and experiment reports. Return exactly one final verdict:

- `PASS`: intended fault occurred and every required recovery criterion has evidence;
- `FAIL`: fault occurred and at least one recovery criterion failed;
- `INCONCLUSIVE`: baseline, installation, matching, safety, or evidence was incomplete.

Read `references/report-contract.md` before assembling the final report. Preserve the CLI-generated JSON/Markdown artifacts and add:

```text
hypothesis.md
scenario.yml
baseline.patch.yml
dry-run.patch.yml
experiment.patch.yml
report.md
report.json
reproduce.sh
reproduce.ps1
cleanup.sh
cleanup.ps1
```

## Hard stops

Stop before real injection when any of these is true:

- isolated profile or effective config cannot be verified;
- target cannot be matched narrowly;
- dry-run does not prove the intended match;
- experiment would affect production, secrets, external systems, or paths outside the authorized workspace;
- required authentication or explicit human approval is unavailable;
- local DSH interfaces materially differ from the documented tool-pipeline contract.

## Final response format

Lead with:

1. **Verdict** — PASS / FAIL / INCONCLUSIVE;
2. **Protected need**;
3. **Injected fault** — rule, action, tool, scope, seed;
4. **Decisive evidence**;
5. **Artifact path**;
6. **One-command reproduction**;
7. **Remaining limitation**.

Do not dump raw logs unless the user asks. Never include secrets in reports.
