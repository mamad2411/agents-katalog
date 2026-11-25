---
name: publish-benchmark-observation
description: Configure, smoke-test, run, submit, and report an Explicit Edit Benchmark observation to Hugging Face.
compatibility: Linux, Node.js 24+, authenticated target harness, Hugging Face CLI, and this repository's installed dependencies.
---

# Publish a benchmark observation

## Read first

- `README.md`
- `docs/contributing-results.md`
- `docs/running.md`, when the agent needs a provider route or a custom config

If the agent has no ready adapter, use `add-benchmark-harness` first.

For a verified community result, prefer the public [official run template](https://github.com/alexshpunt/explicit-edit-benchmark-run-template). It accepts only registered official inputs, supports partial runs, attests the exact result, and is accepted automatically. Use the local flow below for development or an unverified contribution.

## Ask for three things

1. the harness family: `pi-default`, `pi-agent-ide`, `codex-cli-default`, `opencode-default`, `oh-my-pi-default`, `github-copilot-cli-default`, `dsh-standard`, or `dsh-code`;
2. the exact model id;
3. the reasoning level.

Everything else is automatic. A custom adapter or a config you already have uses `--config FILE` instead of `--harness`, and then you do not need these three answers.

## Check before you start

Make sure the agent CLI is installed and logged in, and that the user has run `hf auth login`.

The command writes its own temporary configuration into the system temp folder and deletes it at the end, so nobody prepares or commits a config file for a ready adapter.

Never copy credentials, local paths, prompts, raw commands, or command output into configuration or metadata.

## Know what the smoke task does

`benchmark:submit` runs one exact task (`replace-all-10-plain`) for every selected profile and compares the resulting files byte for byte. If any profile fails, it stops before the paid full run.

Do not ask the user to run a separate smoke, and do not set `ready: true`. That flag only gates a direct `npm run benchmark -- run`. The submit command authorizes its own run once the smoke passes.

Ask the user before starting, because a passing smoke goes straight into a paid full run. Tell them the model, the harness, the task count, and the concurrency.

## Run and submit

Make sure the user has run `hf auth login`, then run:

```sh
npm run benchmark:submit -- --harness HARNESS --model MODEL --thinking LEVEL --concurrency 10
```

`--concurrency` is how many tasks run at once. It changes how long the run takes, not the result. Add provider flags only when the agent needs a local route, for example `--provider-file provider.json --env-file private-env.json`. Run `npm run benchmark:submit -- --help` for every option.

The command prepares the config, checks the agent and the Hugging Face login, smoke-tests every profile, runs all 226 tasks, exports and validates the bundle, builds safe submission metadata, and opens a pull request against the Hugging Face Dataset `alexshpunt/explicit-edit-benchmark`.

It always uses five Oracle recovery attempts and a 120-second timeout.

Keep failures, timeouts, and recovery rounds. Never edit normalized rows to improve a result. After submission, give the user the report below.

## Acceptance

Official candidates are verified and accepted automatically by the repository workflow. Do not ask for manual approval based on score. If delivery fails after inference, use the template's submit-only recovery with the original run ID and attempt.

Ordinary local candidates remain unverified and follow the contribution review process. Code, adapter, task, workflow, and policy changes always require normal review.

## Report the observation

Do not finish with a PASS count alone. A final exact pass can hide first-attempt misses and expensive recovery. Give the user the following tables after each new observation is submitted. No narrative analysis is required.

Read [Methodology](../../../docs/methodology.md) for the current formula and comparison rules. Use the existing run artifacts and normalized bundle; do not rerun inference to fill a reporting gap. Keep raw logs, credentials, local paths, and model prose out of public comments and uploads.

### Grades and usage

Start with the run ID, submission URL, and acceptance status. Submitted is not the same as accepted.

Give one row per configuration, identified by model, provider, harness version, and reasoning level:

| Field | What to report |
| --- | --- |
| First exact | Passes / trials and rate before Oracle recovery |
| Final exact | Passes / trials and rate after Oracle recovery |
| Coverage | Distinct observed tasks / full benchmark task count |
| Quality and Score | Both values using the current canonical formula |
| Recovery | Tasks that recovered to exact success and total extra rounds |
| Cost and tokens | Totals across all benchmark rounds, including recovery |

For scoring version 2, quality is `0.75 × first exact rate + 0.25 × final exact rate`, and Score is `quality × coverage`. Use the task-weighted rates from the methodology when task observation counts differ. When trial rates and task-weighted scoring rates differ, show both and label them. Label these as this observation's values, not the aggregated Explorer score. Use the full task count from the benchmark definition, not the selected subset, as the coverage denominator.

Sum `costUsd` and `totalTokens` from the normalized rounds for each configuration. State how many rounds expose each metric. If any are missing, label the known sum as partial; if none are known, report unknown, not zero. Keep smoke usage separate from benchmark totals.

### First-attempt misses

Join failed-first trials to their first rounds by trial ID. Show one row per missed task with the observed timeout, exit status, event errors, failed or invalid tool calls, and byte mismatch when known. Include trials that never started or have no round evidence. Summarize misses with execution-error signals, tool-error signals only, byte mismatches without error signals, and insufficient evidence. Count a timeout, nonzero exit, positive event-error count, confirmed provider failure, or recorded infrastructure failure as an execution-error signal. Count positive failed or invalid tool-call counts as tool-error signals. Call a mismatch error-free only when all relevant error metrics were observed and show no errors. Show the total tool-error miss count separately because it can overlap execution errors.

Use normalized fields such as `infrastructureFailure`, `timedOut`, `exitCode`, `eventErrors`, `failedToolCalls`, `invalidToolCalls`, and `providerFailure`. Check the local run summary for byte-comparison details when the normalized `difference` is unknown. Missing error fields are unknown, not evidence that no error happened.

Keep observed failure types separate from confirmed causes. A generic timeout or process error does not prove a provider failure. A tool error does not prove a harness defect. Wrong bytes without an error do not prove a model defect. Report a confirmed provider cause only when the adapter supplied a machine-readable `providerFailure`; otherwise leave the cause unknown unless separate evidence establishes it.

### Comparable-route results

Query the accepted Dataset views for eligible configurations on the same model route and reasoning level, with compatible benchmark and recovery rules. State the Dataset revision, comparison filters, peer count, ties, and coverage. Exclude partial and quarantined configurations from a full-benchmark rank.

Show the aggregated configuration's rank, first exact, final exact, Score, and gap to the best comparable configuration. Keep that row separate from the new observation: repeated observations can change the aggregate. Describe a score gap through its measured first/final-exact components, not a claim about which model, provider, or harness caused it. Compare cost only when both sides have complete usage data on the same scope.

If acceptance is pending, label the comparison as pre-acceptance and do not invent a rank that includes the new observation. If the Dataset or suitable peers are unavailable, keep the section and state why the comparison is unavailable. Reporting or comparison failures do not undo a submitted observation, authorize another paid run, or justify changing its evidence.